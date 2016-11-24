#-*- coding: utf-8 -*-
# from __future__ import division, unicode_literals

import logging

from .base import AutoRegisterBase
from common.crypt import Cryption



logger = logging.getLogger(__name__)

class Fanlitou(AutoRegisterBase):

    def __init__(self):
        super(Fanlitou, self).__init__()
        self.fcode = "fanlitou"
        self.secret_key = "1234567890123456"
        self.cryption_key = "1234567890123456"  # 初始化密钥，长度必须为16位
        self.cryption = Cryption(self.cryption_key)
