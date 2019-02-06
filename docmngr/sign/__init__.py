# -*- coding: utf-8 -*-
# @Author: sruiz
# @Date:   2017-11-09 16:08:55
# @Last Modified by:   sruiz
# @Last Modified time: 2017-12-15 10:41:59
import os
import subprocess
import math
import random
from Crypto.Cipher import DES
from jinja2 import Environment, FileSystemLoader
import pdb


class Crypter:
    char_set = [chr(i) for i in range(1, 256)]
    BLOCK_SIZE = 8

    def __init__(self, key, seed=10):
        key = key.encode()
        if len(key) > 8:
            self.key = key[:8]
        else:
            random.seed(seed)
            filling = bytearray(random.getrandbits(8) for i in range(8))
            self.key = key + filling[len(key):]

        self._crypter = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, message):
        message = message.encode()
        length = math.ceil(len(message) / self.BLOCK_SIZE) * self.BLOCK_SIZE
        padded_msg = message + b'\x00' * (length - len(message))
        return self._crypter.encrypt(padded_msg)

    def decrypt(self, message):
        padded_msg = self._crypter.decrypt(message)
        message = padded_msg[:padded_msg.find(b'\x00')]
        return message.decode()
