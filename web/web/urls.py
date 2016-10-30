# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""projectb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


from api.fanlitou import views as fanlitou_api
admin.autodiscover()

urlpatterns = [
    url(r'^_admin/', include(admin.site.urls)),
]

# fanlitou api
urlpatterns += [
    url(r'^api/flt/auto_register/$', fanlitou_api.Register.as_view()),
    url(r'^api/flt/register_query/$', fanlitou_api.RegisterQuery.as_view()),
    url(r'^api/flt/get_login_token/$', fanlitou_api.LoginToken.as_view()),
    url(r'^api/flt/auto_login/$', fanlitou_api.AutoLogin.as_view(), name='fanlitou_auto_login'),
    url(r'^api/flt/user_bind/$', fanlitou_api.UserBind.as_view(), name='fanlitou_user_bind'),
    url(r'^api/flt/get_invest_records/$', fanlitou_api.GetInvestRecord.as_view()),
]
