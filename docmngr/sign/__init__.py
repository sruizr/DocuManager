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


class PdfSigner:
    def __init__(self, signer_jar, signature_file, sign_img_path,
                 reason=None, location=None, key_file=None):
        self.signer_jar = signer_jar
        self.signature_file = signature_file
        self.reason = reason
        self.location = location
        self.encoded_psw = None
        if key_file:
            with open(key_file, 'rb') as f:
                self.encoded_psw = f.read()

        self.number_of_images = len(os.listdir(sign_img_path))
        self.img_path = sign_img_path

    def _get_out_filename(self, in_file):
        return in_file[:-4] + '_out.pdf'

    def paste_signature(self, input_fn, position, output_fn=None):
        "Paste a png signature into the pdf"

        if output_fn is None:
            output_fn = self._get_out_filename(input_fn)
        page_number = 0 if len(position) == 2 else position[2]

    def _get_password(self, key):
        if self.encoded_psw:
            return Crypter(key).decrypt(self.encoded_psw)

        return key

    def sign_digitally(self, key, input_filename, output_filename):
        psw = ['-p', self._get_password(key)]

        sign_cmd = ['java', '-jar', self.signer_jar, '-n']
        input_file = ['-t', in_file]
        output_file = ['-o', self._get_out_filename(in_file)]
        reason = ['-r', self.reason] if self.reason else []
        location = ['-l', self.location] if self.location else []
        signature_file = ['-s', self.signature_file]

        all_command = sign_cmd + input_file + output_file + psw + reason + \
            location + signature_file

        subprocess.call(all_command)

    def sign_many(self, key, in_dir, out_dir=None):
        psw = ['-p', self._get_password(key)]
        sign_cmd = ['java', '-jar', self.signer_jar, '-n']
        reason = ['-r', self.reason] if self.reason else []
        location = ['-l', self.location] if self.location else []
        signature_file = ['-s', self.signature_file]

        for filename in os.listdir(in_dir):
            _, ext = os.path.splitext(filename)
            if ext == '.pdf':
                input_file = ['-t', os.path.join(in_dir, filename)]
                if out_dir:
                    output_file = ['-o', os.path.join(out_dir, filename)]
                else:
                    output_file = ['-o', self._get_out_filename(filename)]
                all_command = sign_cmd + input_file + output_file + psw + reason + \
                    location + signature_file

                subprocess.call(all_command)
