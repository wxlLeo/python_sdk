#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from ..base import ApiResponse, parse_get_request_para, parse_post_request_para, ApiBase

import factory
import logging
from api.view import Base as CoreViewBase
from django.http.response import HttpResponseRedirect
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)

class Register(APIView, ApiBase):
    """
    注册
    """
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        logger.info("Auto register api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)
        register = factory.CLS_CONFIG[fcode]["register_cls"]()
        phone_num = parse_post_request_para(request, "phone_num")
        time_stamp = parse_post_request_para(request, "t")
        serial_num = parse_post_request_para(request, "serial_num")
        uid = parse_post_request_para(request, "uid")
        sign = parse_post_request_para(request, "sign")

        is_success, result = register.validate_request_datas(phone_num, time_stamp, uid)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, phone_num, fcode, time_stamp, serial_num)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        phone_num = register.decrypt_data(phone_num)
        uid = register.decrypt_data(uid)

        register_result = register.auto_register(fcode, phone_num, uid, serial_num)
        logger.info("Auto register api return result is: %s" % register_result)
        return ApiResponse(data=register_result)

class RegisterQuery(APIView, ApiBase):
    """
    注册查询
    """
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        logger.info("Register query api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Register query api return result is: %s" % result)
            return ApiResponse(data=result)
        register = factory.CLS_CONFIG[fcode]["register_cls"]()
        phone_num = parse_post_request_para(request, "phone_num")
        time_stamp = parse_post_request_para(request, "t")
        serial_num = parse_post_request_para(request, "serial_num")
        sign = parse_post_request_para(request, "sign")

        is_success, result = register.validate_request_datas(phone_num, time_stamp)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, phone_num, fcode, time_stamp, serial_num)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        phone_num = register.decrypt_data(phone_num)

        result = register.register_query(phone_num, fcode, serial_num)
        logger.info("Register query api return result is: %s" % result)
        return ApiResponse(data=result)

class LoginToken(APIView, ApiBase):
    """
    自动登录token
    """
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        logger.info("Login token api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Login token api return result is: %s" % result)
            return ApiResponse(data=result)
        register = factory.CLS_CONFIG[fcode]["register_cls"]()
        phone_num = parse_post_request_para(request, "phone_num")
        uid = parse_post_request_para(request, "uid")
        time_stamp = parse_post_request_para(request, "t")
        register_token = parse_post_request_para(request, "register_token")
        sign = parse_post_request_para(request, "sign")

        is_success, result = register.validate_request_datas(phone_num, uid, time_stamp, register_token)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, phone_num, fcode, time_stamp, "")

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        phone_num = register.decrypt_data(phone_num)
        uid = register.decrypt_data(uid)

        result = register.get_user_login_token(phone_num, fcode, register_token, uid)
        logger.info("Login token api return result is: %s" % result)
        return ApiResponse(data=result)

class AutoLogin(CoreViewBase):
    """
    自动登录
    """
    http_method_names = {'get'}

    def get(self, request, *args, **kwargs):
        request.GET.get('bid_id', "")
        logger.info("Login token api got request data: %s" % request.GET)
        fcode = request.GET.get('fcode', "")
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Login token api return result is: %s" % result)
            return ApiResponse(data=result)
        register = factory.CLS_CONFIG[fcode]["register_cls"]()
        phone_num = request.GET.get('phone_num', "")
        uid = request.GET.get('uid', "")
        time_stamp = request.GET.get('t', "")
        bid_url = request.GET.get('bid_url', "")
        source = request.GET.get('source', "")
        register_token = request.GET.get('register_token', "")
        login_token = request.GET.get('login_token', "")
        sign = request.GET.get('sign', "")

        if source == "mobile":
            bid_url = "https://www.fanlitou.com"
        else:
            bid_url = "https://www.fanlitou.com"

        is_success, result = register.validate_request_datas(phone_num, uid, time_stamp, register_token)

        if not is_success:
            logger.info("Login token api return result is: %s" % result)
            return HttpResponseRedirect(bid_url)

        is_success, result = register.validate_sign(sign, phone_num, fcode, time_stamp, "")

        if not is_success:
            logger.info("Login token api return result is: %s" % result)
            return HttpResponseRedirect(bid_url)

        phone_num = register.decrypt_data(phone_num)
        time_stamp = register.decrypt_data(time_stamp)

        register.do_auto_login(request, phone_num, fcode, register_token, login_token, time_stamp, bid_url, source)

        return HttpResponseRedirect(bid_url)

class UserBind(CoreViewBase):
    """
    老账户绑定
    """
    http_method_names = {'get'}

    def get(self, request, *args, **kwargs):
        logger.info("User bind api got request data: %s" % request.GET)
        fcode = request.GET.get('fcode', "")
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("User bind api return result is: %s" % result)
            return ApiResponse(data=result)
        register = factory.CLS_CONFIG[fcode]["register_cls"]()
        phone_num = request.GET.get('phone_num', "")
        uid = request.GET.get('uid', "")
        time_stamp = request.GET.get('t', "")
        bid_url = request.GET.get('bid_url', "")
        source = request.GET.get('source', "")
        sign = request.GET.get('sign', "")

        if source == "mobile":
            bind_login_url = "https://m.fanlitou.com/login/"
        else:
            bind_login_url = "https://www.fanlitou.com/login/"

        is_success, result = register.validate_request_datas(phone_num, uid, time_stamp)

        if not is_success:
            logger.info("User bind api return result is: %s" % result)
            return HttpResponseRedirect(bind_login_url)

        is_success, result = register.validate_sign(sign, phone_num, fcode, time_stamp, "")

        if not is_success:
            logger.info("User bind api return result is: %s" % result)
            return HttpResponseRedirect(bind_login_url)

        phone_num = register.decrypt_data(phone_num)
        uid = register.decrypt_data(uid)

        bind_login_url = "%s?uid=%s&user_name=%s&fcode=%s&bid_url=%s" % (bind_login_url, uid, phone_num, fcode, bid_url)

        return HttpResponseRedirect(bind_login_url)

class GetBidList(APIView, ApiBase):
    """
    获取标列表
    """
    renderer_classes = (JSONRenderer, )

    def process_bid_list(self, fcode, time_stamp, sign):
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Get bid list api return result is: %s" % result)
            return result
        register = factory.CLS_CONFIG[fcode]["register_cls"]()

        validate_sign_result = register.validate_sign_for_bid_list(sign, fcode, time_stamp)

        if not validate_sign_result["success"]:
            logger.info("Get bid list api return result is: %s" % validate_sign_result)
            return validate_sign_result

        validate_time_stamp_result = register.validate_timestamp_for_bid_list(fcode, time_stamp)
        if not validate_time_stamp_result["success"]:
            logger.info("Get bid list api return result is: %s" % validate_time_stamp_result)
            return validate_time_stamp_result

        result = register.get_bid_list(fcode)
        logger.info("Get bid list api return result is: %s" % result)
        return result

    def get(self, request):
        logger.info("Get bid list api got request data: %s" % request.query_params)
        fcode = parse_get_request_para(request, "fcode")
        time_stamp = parse_get_request_para(request, "t")
        sign = parse_get_request_para(request, "sign")
        result = self.process_bid_list(fcode, time_stamp, sign)
        return ApiResponse(data=result)

    def post(self, request):
        logger.info("Get bid list api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        time_stamp = parse_post_request_para(request, "t")
        sign = parse_post_request_para(request, "sign")
        result = self.process_bid_list(fcode, time_stamp, sign)
        return ApiResponse(data=result)

class GetInvestRecord(APIView, ApiBase):
    """
    获取渠道用户投资记录
    """
    renderer_classes = (JSONRenderer, )

    def process_invest_records(self, fcode, time_stamp, sign, start_time, end_time):
        if fcode not in factory.CLS_CONFIG:
            result = {
                "status": "45",  # 其他错误
                "err_msg": "渠道码错误",
            }
            logger.info("Get invest record api return result is: %s" % result)
            return result
        register = factory.CLS_CONFIG[fcode]["register_cls"]()

        validate_sign_result = register.validate_sign_for_invest_record(sign, fcode, time_stamp)

        if not validate_sign_result["success"]:
            logger.info("Get invest record api return result is: %s" % validate_sign_result)
            return validate_sign_result

        validate_start_end_time_result = register.validate_start_end_time(start_time, end_time)
        if not validate_start_end_time_result["success"]:
            logger.info("Get invest record api return result is: %s" % validate_start_end_time_result)
            return validate_start_end_time_result

        result = register.get_invest_record(fcode, start_time, end_time)
        return result

    def get(self, request):
        logger.info("Get invest record api got request data: %s" % request.query_params)
        fcode = parse_get_request_para(request, "fcode")
        start_time = parse_get_request_para(request, "start_time")
        end_time = parse_get_request_para(request, "end_time")
        time_stamp = parse_get_request_para(request, "t")
        sign = parse_get_request_para(request, "sign")
        result = self.process_invest_records(fcode, time_stamp, sign, start_time, end_time)
        logger.info("Get invest record api return result is: %s" % result)
        return ApiResponse(data=result)

    def post(self, request):
        logger.info("Get invest record api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        start_time = parse_post_request_para(request, "start_time")
        end_time = parse_post_request_para(request, "end_time")
        time_stamp = parse_post_request_para(request, "t")
        sign = parse_post_request_para(request, "sign")
        result = self.process_invest_records(fcode, time_stamp, sign, start_time, end_time)
        logger.info("Get invest record api return result is: %s" % result)
        return ApiResponse(data=result)
