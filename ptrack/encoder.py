"""Ptrack Default Encoder"""
import json
import base64
import nacl.secret
import nacl.utils
from django.conf import settings


BLOCK_SIZE = 32
# Padding character
PADDING = '{'


def pad(msg):
    """Padding for keys on 32 byte blocks."""
    return msg + (BLOCK_SIZE - len(msg)) * PADDING


class PtrackEncoder(object):
    """PtrackEncoder class."""

    @staticmethod
    def decrypt(encoded_data):
        """Decrypt a base64 url string into a dictionary."""
        key = pad(settings.PTRACK_SECRET).encode('utf8')
        box = nacl.secret.SecretBox(key)

        encrypted = base64.urlsafe_b64decode(encoded_data.encode('utf8'))
        data = box.decrypt(encrypted)
        # json.loads expects a str, so we convert bytes to str
        data = data.decode('utf8')
        return json.loads(data)

    @staticmethod
    def encrypt(*args, **kwargs):
        """Encrypt args and kwargs into an encoded base64 url string."""
        key = pad(settings.PTRACK_SECRET).encode('utf8')
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

        data = json.dumps((args, kwargs))
        # box expects bytes, so we convert here
        data = data.encode('utf8')
        encrypted = box.encrypt(data, nonce)
        encoded_data = base64.urlsafe_b64encode(encrypted)
        return encoded_data
