# -*- coding: utf-8 -*-

# from __future__ import unicode_literals
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import logging
import traceback

logger = logging.getLogger("django")


class Cryption(object):

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, self.key)
            # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
            length = 16
            text = str(text)
            count = len(text)
            add = length - (count % length)
            text = text + ('\0' * add)
            self.ciphertext = cryptor.encrypt(text)
            # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
            return b2a_hex(self.ciphertext)
        except:
            logger.error("Encrypt error for data: %s" % text)
            print "***", type(text)
            logger.error(traceback.format_exc())
            return False

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, self.key)
            plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text.rstrip('\0')
        except:
            logger.error("Decrypt error for data: %s" % text)
            return False

if __name__ == '__main__':
    pc = Cryption('1234567890123456')      # 初始化密钥，长度必须为16位
    phone_num = "测试"
    print "phone_num is ", phone_num
    phone_num_after_encrypt = pc.encrypt(phone_num)
    print "phone_num_after_encrypt is ", phone_num_after_encrypt
    phone_num_after_decrypt = pc.decrypt(phone_num_after_encrypt)
    print "phone_num_after_decrypt is ", phone_num_after_decrypt
    print pc.decrypt("69a658b08a6035fe80ea53867a57d1a3")
    print pc.encrypt("pc")
