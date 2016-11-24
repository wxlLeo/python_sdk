#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from ..base import ApiResponse, parse_get_request_para, parse_post_request_para, ApiBase

import logging
from api.view import Base as CoreViewBase
from django.http.response import HttpResponseRedirect
from rest_framework.renderers import JSONRenderer
from .fanlitou import Fanlitou

logger = logging.getLogger(__name__)

class Register(APIView, ApiBase):
    """
    注册
    """
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        logger.info("Auto register api got request data: %s" % request.data)
        fcode = parse_post_request_para(request, "fcode")
        phone_num = parse_post_request_para(request, "phone_num")
        time_stamp = parse_post_request_para(request, "t")
        uid = parse_post_request_para(request, "uid")
        sign = parse_post_request_para(request, "sign")

        register = Fanlitou()

        is_success, result = register.validate_request_datas(phone_num, fcode, time_stamp, uid, sign)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, time_stamp)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        phone_num = register.decrypt_data(phone_num)
        uid = register.decrypt_data(uid)

        register_result = register.auto_register(phone_num, uid)
        logger.info("Auto register api return result is: %s" % register_result)
        return ApiResponse(data=register_result)

class RegisterQuery(APIView, ApiBase):
    """
    注册查询
    """
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        logger.info("Register query api got request data: %s" % request.data)
        uid = parse_post_request_para(request, "uid")
        fcode = parse_post_request_para(request, "fcode")
        time_stamp = parse_post_request_para(request, "t")
        sign = parse_post_request_para(request, "sign")

        register = Fanlitou()

        is_success, result = register.validate_request_datas(uid, fcode, time_stamp, sign)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, time_stamp)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        uid = register.decrypt_data(uid)

        result = register.register_query(uid, fcode)
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
        uid = parse_post_request_para(request, "uid")
        time_stamp = parse_post_request_para(request, "t")
        register_token = parse_post_request_para(request, "register_token")
        sign = parse_post_request_para(request, "sign")

        register = Fanlitou()

        is_success, result = register.validate_request_datas(fcode, uid, time_stamp, register_token, sign)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        is_success, result = register.validate_sign(sign, time_stamp)

        if not is_success:
            logger.info("Auto register api return result is: %s" % result)
            return ApiResponse(data=result)

        fcode = register.decrypt_data(fcode)
        uid = register.decrypt_data(uid)
        register_token = register.decrypt_data(register_token)

        result = register.get_user_login_token(fcode, register_token, uid)
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
        uid = request.GET.get('uid', "")
        time_stamp = request.GET.get('t', "")
        bid_url = request.GET.get('bid_url', "")
        source = request.GET.get('source', "")
        register_token = request.GET.get('register_token', "")
        login_token = request.GET.get('login_token', "")
        sign = request.GET.get('sign', "")

        register = Fanlitou()

        is_success, result = register.validate_request_datas(fcode, uid, time_stamp, source, register_token, login_token, sign)

        if not is_success:
            logger.info("Login token api return result is: %s" % result)
            return HttpResponseRedirect(bid_url)

        if register.decrypt_data(source) == "mobile":
            bid_url = "https://m.fanlitou.com"
        else:
            bid_url = "https://www.fanlitou.com"

        is_success, result = register.validate_sign(sign, time_stamp)

        if not is_success:
            logger.info("Login token api return result is: %s" % result)
            return HttpResponseRedirect(bid_url)

        register.do_auto_login(register.decrypt_data(uid),
                               register.decrypt_data(fcode),
                               register.decrypt_data(register_token),
                               register.decrypt_data(login_token),
                               register.decrypt_data(time_stamp),
                               bid_url,
                               register.decrypt_data(source))

        return HttpResponseRedirect(bid_url)

class UserBind(CoreViewBase):
    """
    老账户绑定
    """
    http_method_names = {'get'}

    def get(self, request, *args, **kwargs):
        logger.info("User bind api got request data: %s" % request.GET)
        fcode = request.GET.get('fcode', "")
        uid = request.GET.get('uid', "")
        time_stamp = request.GET.get('t', "")
        bid_url = request.GET.get('bid_url', "")
        source = request.GET.get('source', "")
        sign = request.GET.get('sign', "")

        register = Fanlitou()

        if register.decrypt_data(source) == "mobile":
            bind_login_url = "https://m.fanlitou.com/login/"
        else:
            bind_login_url = "https://www.fanlitou.com/login/"

        is_success, result = register.validate_request_datas(fcode, uid, time_stamp, source, sign)

        if not is_success:
            logger.info("User bind api return result is: %s" % result)
            return HttpResponseRedirect(bind_login_url)

        is_success, result = register.validate_sign(sign, time_stamp)

        if not is_success:
            logger.info("User bind api return result is: %s" % result)
            return HttpResponseRedirect(bind_login_url)

        bind_login_url = "%s?uid=%s&fcode=%s&bid_url=%s" % (bind_login_url, uid, fcode, bid_url)

        # TODO:用户成功登录之后，将返利投用户号uid与用户登录的账号做绑定
        return HttpResponseRedirect(bind_login_url)


class GetBidList(APIView, ApiBase):
    """
    获取标列表
    """
    renderer_classes = (JSONRenderer, )

    def process_bid_list(self, page_count, page_index, time_stamp, sign):
        register = Fanlitou()

        validate_sign_result = register.validate_sign_for_bid_list(sign, time_stamp)

        if not validate_sign_result["success"]:
            logger.info("Get bid list api return result is: %s" % validate_sign_result)
            return validate_sign_result

        result = register.get_bid_list(page_count, page_index)
        logger.info("Get bid list api return result is: %s" % result)
        return result

    def get(self, request):
        logger.info("Get bid list api got request data: %s" % request.query_params)
        page_count = parse_get_request_para(request, "pageCount")
        page_index = parse_get_request_para(request, "pageIndex")
        time_stamp = parse_get_request_para(request, "t")
        sign = parse_get_request_para(request, "sign")
        result = self.process_bid_list(page_count, page_index, time_stamp, sign)
        return ApiResponse(data=result)

    def post(self, request):
        logger.info("Get bid list api got request data: %s" % request.data)
        page_count = parse_post_request_para(request, "pageCount")
        page_index = parse_post_request_para(request, "pageIndex")
        time_stamp = parse_post_request_para(request, "t")
        sign = parse_post_request_para(request, "sign")
        result = self.process_bid_list(page_count, page_index, time_stamp, sign)
        return ApiResponse(data=result)

class GetInvestRecord(APIView, ApiBase):
    """
    获取渠道用户投资记录
    """
    renderer_classes = (JSONRenderer, )

    def process_invest_records(self, time_stamp, sign, start_time, end_time):
        register = Fanlitou()

        validate_sign_result = register.validate_sign_for_invest_record(sign, time_stamp)

        if not validate_sign_result["success"]:
            logger.info("Get invest record api return result is: %s" % validate_sign_result)
            return validate_sign_result

        validate_start_end_time_result = register.validate_start_end_time(start_time, end_time)
        if not validate_start_end_time_result["success"]:
            logger.info("Get invest record api return result is: %s" % validate_start_end_time_result)
            return validate_start_end_time_result

        result = register.get_invest_record(start_time, end_time)
        return result

    def get(self, request):
        logger.info("Get invest record api got request data: %s" % request.query_params)
        start_time = parse_get_request_para(request, "start_time")
        end_time = parse_get_request_para(request, "end_time")
        time_stamp = parse_get_request_para(request, "t")
        sign = parse_get_request_para(request, "sign")
        result = self.process_invest_records(time_stamp, sign, start_time, end_time)
        logger.info("Get invest record api return result is: %s" % result)
        return ApiResponse(data=result)

    def post(self, request):
        logger.info("Get invest record api got request data: %s" % request.data)
        start_time = parse_post_request_para(request, "start_time")
        end_time = parse_post_request_para(request, "end_time")
        time_stamp = parse_post_request_para(request, "t")
        sign = parse_post_request_para(request, "sign")
        result = self.process_invest_records(time_stamp, sign, start_time, end_time)
        logger.info("Get invest record api return result is: %s" % result)
        return ApiResponse(data=result)
