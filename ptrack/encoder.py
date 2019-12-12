"""Ptrack Default Encoder"""
import json
import base64
from typing import Any, Dict, Tuple, Union

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
    def decrypt(encoded_data: Union[bytes, str]) -> Tuple[Tuple[Any], Dict[str, Any]]:
        """Return args and kwargs decrypted from base64 url string."""
        if isinstance(encoded_data, str):
            encoded_data = encoded_data.encode('utf8')

        key = pad(settings.PTRACK_SECRET).encode('utf8')
        box = nacl.secret.SecretBox(key)

        encrypted = base64.urlsafe_b64decode(encoded_data)
        data = box.decrypt(encrypted)
        # json.loads expects a str, so we convert bytes to str
        data = data.decode('utf8')
        return json.loads(data)

    @staticmethod
    def encrypt(*args, **kwargs) -> bytes:
        """Encrypt args and kwargs into an encoded base64 url string."""
        key = pad(settings.PTRACK_SECRET).encode('utf8')
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

        data = json.dumps((args, kwargs))
        # box expects bytes, so we convert here
        bytes_data = data.encode('utf8')
        encrypted = box.encrypt(bytes_data, nonce)
        encoded_data = base64.urlsafe_b64encode(encrypted)
        return encoded_data
