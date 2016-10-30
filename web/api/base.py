#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

class ApiBase(object):

    USER_VALIDATION_FAILED_RESULT = {
        "success": False,
        "error_msg": "User does not have this operation permission!"
    }

    def validate_user(self, action_username, login_user):
        """
        验证被操作的用户和登录用户
        如果登录用户和被操作用户相同，则验证通过
        若不同，如果登录用户为管理员，则有权限操作，验证通过
        否则验证不通过
        """
        if not action_username:
            # 如果查询用户为空，则通过验证
            return True
        if action_username:
            if not login_user or not login_user.is_authenticated():
                # 如果查询用户不为空，并且用户未登录，则验证不通过
                raise PermissionDenied(detail='User not login')
        if login_user and action_username:
            action_user = get_user_by_name(action_username)
            if not action_user:
                raise PermissionDenied(detail='User does not exist')
            if action_user.username == login_user.username:
                return True
            elif login_user.is_superuser:
                return True
            else:
                raise PermissionDenied(detail='Login user is not same as operate user')
        return True

class ApiResponse(Response):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type="application/json; charset=UTF-8"):
        super(ApiResponse, self).__init__(data=data, status=status,
                 template_name=template_name, headers=headers,
                 exception=exception, content_type=content_type)

def parse_get_request_para(request, para_name):
    para_value = request.query_params[para_name] if para_name in request.query_params.keys() else None
    return para_value

def parse_post_request_para(request, para_name):
    para_value = request.data[para_name] if para_name in request.data.keys() else None
    return para_value

def get_user_by_name(user_name):
    if user_name:
        user = User.objects.filter(username=user_name).first()
    else:
        user = None
    return user


