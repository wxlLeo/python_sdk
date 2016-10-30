# -*- coding: utf-8 -*-

from api.fanlitou.fanlitou import Fanlitou

clazz = Fanlitou()
result = clazz.user_bind_notify("13012345678", "02", "user_name")
print result
