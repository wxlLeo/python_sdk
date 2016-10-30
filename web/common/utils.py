# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from decimal import Decimal
from django.utils import timezone
from django.utils.timezone import make_naive, is_aware, is_naive
from datetime import datetime, date

import decimal

def datetime_to_str_full(dt, formt='%Y-%m-%d %H:%M:%S'):
    if isinstance(dt, datetime):
        if is_aware(dt):
            dt = to_naive_datetime(dt)
        return dt.strftime(formt)
    elif isinstance(dt, date):
        return dt.strftime(formt)
    else:
        return None


def to_aware_datetime(dt):
    tp = dt.timetuple()
    stamp = time.mktime(tp)
    dt = datetime.fromtimestamp(stamp, timezone.utc)
    return dt


def to_naive_datetime(dt):
    return make_naive(dt)


def datetime_str_to_aware_datetime(datetime_str, formt='%Y-%m-%d %H:%M:%S'):
    '''
    create by zhaopengfei at 16/05/29 15:52
    将抓取过来的时间字符串转换成可以入库的时间形式
    '''
    timetuple = time.strptime(datetime_str, formt)
    stamp = time.mktime(timetuple)
    aware_datetime = datetime.fromtimestamp(stamp, timezone.utc)
    return aware_datetime


def datetime_to_str_short(dt, formt="%Y-%m-%d"):
    if isinstance(dt, datetime):
        if is_aware(dt):
            dt = to_naive_datetime(dt)
        return dt.strftime(formt)
    elif isinstance(dt, date):
        return dt.strftime(formt)
    else:
        return None


def fmt_two_amount(value, f=2):
    places = Decimal(10) ** -f
    return Decimal(value).quantize(places, rounding=decimal.ROUND_HALF_UP)


def format_float(num, f=2, is_separate=True):
    if isinstance(num, int) or isinstance(num, long):
        return '{:,}'.format(num) if is_separate else '{:}'.format(num)
    elif num is None:
        return "0"
    num = fmt_two_amount(num, f)
    if is_separate:
        result = '{:,}'.format(num)
    else:
        result = '{:}'.format(num)
    if "." in result:
        result = result.rstrip('0').rstrip('.')
    return result

def str_to_datetime(dt, format="%Y-%m-%d %H:%M:%S"):
    if isinstance(dt, datetime):
        if is_naive(dt):
            return to_aware_datetime(dt)
        else:
            return dt

    return to_aware_datetime(datetime.strptime(dt, format))

