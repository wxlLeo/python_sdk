#-*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import logging
import requests
import hashlib

import random
import string
import traceback
import time
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from common import utils
from django.conf import settings
from common.crypt import Cryption
import json

logger = logging.getLogger(__name__)


class AutoRegisterBase(object):
    name = None

    def __init__(self):
        self.platform = None

        if settings.ENV != settings.ENV_WWW:
            self.pc_url_prefix = "http://test.fanlitou.com"
            self.mobile_url_prefix = "http://m.test.fanlitou.com"
            self.notify_url = "http://test.fanlitou.com/api/user_bound/notify/"
        else:
            self.pc_url_prefix = "https://www.fanlitou.com"
            self.mobile_url_prefix = "https://m.fanlitou.com"
            self.notify_url = "https://www.fanlitou.com/api/user_bound/notify/"

        self.fcode = "fanlitou"
        self.secret_key = "1234567890123456"
        self.cryption_key = "1234567890123456"  # 初始化密钥，长度必须为16位
        self.cryption = Cryption(self.cryption_key)

        self.session = requests.session()
        self.status_mapping = {
            "REGISTER_SUCCESS": "01",  # 注册成功
            "BIND_SUCCESS": "02",  # 绑定成功
            "REGISTER_SUCCESS_BIND_FAIL": "03",  # 注册成功,绑定失败
            "BIND_SUCCESS_NOT_FLT_USER": "04",  # 绑定成功,但非返利投用户
            "GET_TOKEN_SUCCESS": "05",  # 获取token成功
            "NOT_PASS_VALIDATION": "41",  # 未通过安全校验
            "USER_ALREADY_EXIST": "42",  # 注册失败,该用户已存在,不可重复注册
            "REGISTER_FAIL": "43",  # 注册失败,注明其他详细原因
            "BIND_FAIL": "44",  # 绑定失败
            "OTHER_FAIL_STATUS": "45",  # 其他错误
        }
        self.query_status = {
            "NOT_REGISTER": "10",  # 新用户，未注册
            "NOT_FANLITOU_USER": "11",  # 老用户，已注册，非渠道用户，但未绑定返利投账户
            "FANLITOU_USER": "12",  # 老用户，已注册，返利投渠道用户
            "OTHER_CHANNEL_USER": "13",  # 老用户，已注册，其他渠道用户
            "OLD_ACCOUNT_BIND": "14"  # 老用户，已注册，已有平台账户绑定
        }
        self.register_type = {
            "REGISTER": 0,  # 新用户注册
            "BIND": 1  # 老用户绑定
        }
        self.useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"
        self.content_type = "application/x-www-form-urlencoded; charset=UTF-8"

    def sign(self, phone_num, fcode, time_stamp):
        sign_str = "%s%s%s%s" % (phone_num, fcode, time_stamp, self.secret_key)
        return hashlib.md5(sign_str).hexdigest()

    def validate_sign(self, sign, phone_num, fcode, time_stamp, serial_num):
        flt_sign = self.sign(self.decrypt_data(phone_num), fcode, self.decrypt_data(time_stamp))
        if flt_sign == sign:
            return True, None
        return False, {
            "status": self.status_mapping["NOT_PASS_VALIDATION"],
            "phone_num": phone_num,
            "user_name": "",
            "serial_num": serial_num,
            "register_token": "",
            "err_msg": "未通过安全校验",
        }

    def validate_sign_for_bid_list(self, sign, fcode, time_stamp):
        sign_str = "%s%s%s" % (time_stamp, fcode, self.secret_key)
        flt_sign = hashlib.md5(sign_str).hexdigest()
        if flt_sign == sign:
            return {
                "success": True
            }
        return {
            "success": False,
            "message": "未通过安全校验"
        }

    def validate_sign_for_invest_record(self, sign, fcode, time_stamp):
        sign_str = "%s%s%s" % (time_stamp, fcode, self.secret_key)
        flt_sign = hashlib.md5(sign_str).hexdigest()
        if flt_sign == sign:
            return {
                "success": True
            }
        return {
            "success": False,
            "message": "未通过安全校验"
        }

    def validate_start_end_time(self, start_time, end_time):
        """
        验证请求开始、结束时间，不能超过30天
        """
        start_time = start_time.split(" ")[0]
        end_time = end_time.split(" ")[0]
        start_time = utils.str_to_datetime(start_time, format="%Y-%m-%d") + relativedelta(days=30)
        end_time = utils.str_to_datetime(end_time, format="%Y-%m-%d")

        if start_time < end_time:
            return {
                "success": False,
                "message": "请求时间跨度超过30天"
            }
        return {
            "success": True
        }

    def validate_request_data(self, data):
        if not self.decrypt_data(data):
            return {
                "success": False,
                "data": {
                    "status": self.status_mapping["OTHER_FAIL_STATUS"],
                    "err_msg": "数据解密错误",
                }
            }
        else:
            return {
                "success": True
            }

    def validate_request_datas(self, *args):
        for arg in args:
            if not self.decrypt_data(arg):
                return False, {
                    "status": self.status_mapping["OTHER_FAIL_STATUS"],
                    "err_msg": "数据解密错误",
                }
            else:
                return True, None

    def encrypt_data(self, data):
        encrypt_result = self.cryption.encrypt(data)
        return encrypt_result

    def decrypt_data(self, data):
        encrypt_result = self.cryption.decrypt(data)
        return encrypt_result

    def gen_password(self):
        random_6_num = ''.join(random.choice(string.digits) for _ in range(6))
        return random_6_num

    def gen_token(self):
        random_20_num_and_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        return random_20_num_and_str

    def auto_register(self, fcode, phone_num, uid, serial_num):
        """
        创建一个新的用户
        """
        try:

            # 如果用户已经存在
            # if "user already exists":
            #     return {
            #         "status": self.status_mapping["USER_ALREADY_EXIST"],
            #         "phone_num": self.encrypt_data(phone_num),
            #         "user_name": "",
            #         "serial_num": serial_num,
            #         "register_token": "",
            #         "err_msg": "注册失败，该用户已存在，不可重复注册",
            #     }

            password = self.gen_password()
            logger.info("Password for user %s is: %s" % (phone_num, password))
            # 创建新用户
            # self.register_user(phone_num, password)

            register_token = self.gen_token()

            # 异步发送短信告知用户密码
            # self.send_register_sms(phone_num, password)
            return {
                "status": self.status_mapping["REGISTER_SUCCESS"],
                "phone_num": self.encrypt_data(phone_num),
                "user_name": self.encrypt_data(phone_num),
                "serial_num": serial_num,
                "register_token": register_token,
                "err_msg": "注册成功",
            }
        except:
            exc = traceback.format_exc()
            logger.error("Register user error for phone_num: %s" % phone_num)
            logger.error("Register user error message: %s" % exc)
            return {
                "status": self.status_mapping["OTHER_FAIL_STATUS"],
                "phone_num": self.encrypt_data(phone_num),
                "user_name": "",
                "serial_num": serial_num,
                "register_token": "",
                "err_msg": "注册失败，系统错误",
            }

    def register_query(self, phone_num, fcode, serial_num):
        """
        注册查询
        """
        try:
            if "新用户，未注册":
                return {
                    "status": self.query_status["NOT_REGISTER"],
                    "phone_num": self.encrypt_data(phone_num),
                    "user_name": "",
                    "serial_num": serial_num,
                    "register_token": "",
                    "err_msg": "新用户，未注册",
                }
            if "老用户，已注册，非渠道用户，但未绑定渠道账户":
                return {
                    "status": self.query_status["NOT_FANLITOU_USER"],
                    "phone_num": self.encrypt_data(phone_num),
                    "user_name": "",
                    "serial_num": serial_num,
                    "register_token": "",
                    "err_msg": "老用户，已注册，非渠道用户，但未绑定渠道账户",
                }
            if "老用户绑定":
                return {
                    "status": self.query_status["OLD_ACCOUNT_BIND"],
                    "phone_num": self.encrypt_data(phone_num),
                    "user_name": self.encrypt_data(phone_num),
                    "serial_num": serial_num,
                    "register_token": "register_token",
                    "err_msg": "老用户绑定",
                }
            if "老用户，已注册，渠道用户":
                return {
                    "status": self.query_status["FANLITOU_USER"],
                    "phone_num": self.encrypt_data(phone_num),
                    "user_name": self.encrypt_data(phone_num),
                    "serial_num": serial_num,
                    "register_token": "register_token",
                    "err_msg": "老用户，已注册，渠道用户",
                }

            if "老用户，已注册，其他渠道用户":
                return {
                    "status": self.query_status["OTHER_CHANNEL_USER"],
                    "phone_num": self.encrypt_data(phone_num),
                    "user_name": "",
                    "serial_num": serial_num,
                    "register_token": "",
                    "err_msg": "老用户，已注册，其他渠道用户",
                }

        except:
            exc = traceback.format_exc()
            logger.error("Register query error for phone_num: %s" % phone_num)
            logger.error("Register query error message: %s" % exc)
            return {
                "status": self.status_mapping["OTHER_FAIL_STATUS"],
                "phone_num": self.encrypt_data(phone_num),
                "user_name": "",
                "serial_num": serial_num,
                "register_token": "",
                "err_msg": "注册查询失败，系统错误",
            }

    def get_user_login_token(self, phone_num, fcode, register_token, uid):
        """
        获取用户自动登录token
        """
        try:
            # if "新用户，未注册":
            #     return {
            #         "status": self.query_status["NOT_REGISTER"],
            #         "login_token": "",
            #         "err_msg": "新用户，未注册",
            #     }
            # if "老用户，已注册，其他渠道用户":
            #     return {
            #         "status": self.query_status["NOT_FANLITOU_USER"],
            #         "login_token": "",
            #         "err_msg": "老用户，已注册，其他渠道用户",
            #     }
            # if "老用户，已注册，其他渠道用户":
            #     return {
            #         "status": self.query_status["NOT_FANLITOU_USER"],
            #         "login_token": "",
            #         "err_msg": "老用户，已注册，其他渠道用户",
            #     }
            # if "register token错误":
            #     return {
            #         "status": self.status_mapping["OTHER_FAIL_STATUS"],
            #         "login_token": "",
            #         "err_msg": "register token错误",
            #     }

            login_token = self.gen_token()
            # self.save_login_toke(fcode, phone_num, login_token)
            return {
                "status": self.status_mapping["GET_TOKEN_SUCCESS"],
                "login_token": login_token,
                "err_msg": "获得login token成功",
            }

        except:
            exc = traceback.format_exc()
            logger.error("Register query error for phone_num: %s" % phone_num)
            logger.error("Register query error message: %s" % exc)
            return {
                "status": self.status_mapping["OTHER_FAIL_STATUS"],
                "login_token": "",
                "err_msg": "获得login token失败，系统错误",
            }

    def do_auto_login(self, request, phone_num, fcode, register_token, login_token, time_stamp, bid_url, source):
        """
        用户自动登录
        """
        try:
            phone_num = self.cryption.decrypt(phone_num)
            # user = self.get_user(phone_num)
            user = "query user"

            if not user:
                logger.info("User not exist %s" % phone_num)
                return False
            # login_token_record = self.get_login_token_record(fcode, phone_num, login_token, register_token)

            login_token_record = "login_token_record"

            if not login_token_record:
                logger.info("Can't find login token for user %s by register token %s" % (phone_num, register_token))
                return False
            if login_token != "login_token_record.login_token":
                logger.info("Login token for user %s is incorrect" % phone_num)
                return False
            time_date = time.localtime(int(time_stamp))
            time_date = time.strftime('%Y-%m-%d %H:%M:%S', time_date)
            token_date = timezone.now()  # login_token_record.create_time
            token_date_after_ten_minutes = token_date + relativedelta(minutes=10)
            token_date_after_ten_minutes = utils.datetime_to_str_full(token_date_after_ten_minutes)
            if time_date > token_date_after_ten_minutes:
                logger.info("Login token for user %s is invalid. Valid duration is 10 minutes." % phone_num)
                return False
            if "user is not login or login user is not current user":
                # do login for user
                logger.info("Auto login for user %s" % phone_num)
                return True
        except:
            exc = traceback.format_exc()
            logger.error("Auto login error for phone_num: %s" % phone_num)
            logger.error("Auto login error message: %s" % exc)
            return False

    def user_bind_notify(self, phone_num, status, user_name):
        timestamp = int(time.time())
        data = {
            "phone_num": self.encrypt_data(phone_num),
            "status": status,
            "t": self.encrypt_data(timestamp),
            "user_name": self.encrypt_data(user_name),
            "sign": self.sign(phone_num, self.fcode, timestamp),
            "serial_num": "serial_num",
            "register_token": "register_token",
            "is_already_invest_before_user_bind": False,
            "err_msg": ""
        }

        headers = {
            'content-type': "application/json",
            }

        response = requests.request("POST", self.notify_url, data=json.dumps(data), headers=headers)

        return response.text

    def get_invest_record(self, fcode, start_time, end_time):
        try:
            start_time = "%s %s" % (start_time.split(" ")[0], "00:00:00")
            end_time = "%s %s" % (end_time.split(" ")[0], "23:59:59")
            start_time = utils.str_to_datetime(start_time, format="%Y-%m-%d %H:%M:%S")
            end_time = utils.str_to_datetime(end_time, format="%Y-%m-%d %H:%M:%S")

            # get invest records between start_time and end_time

            invest_records = []

            view = {
                "phoneNum": "13012345678",
                "bidId": "1",
                "bidName": "test",
                "bidStatus": "还款中",
                "isFirstInvest": True,
                "investAmount": 10000,
                "investTime": "2015-10-10 01:02:03",
                "isAdvancedRepay": False,
                "advancedRepayDate": "",
                "isAssign": False,
                "assignDate": "",
            }
            invest_records.append(view)
            return {
                "success": True,
                "orders": invest_records,
            }
        except:
            logger.error("Get invest records error for tunnel %s" % fcode)
            return {
                "success": False,
                "message": "获取投资记录失败"
            }



