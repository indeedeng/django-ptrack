import json
from django.conf import settings
from Crypto.Cipher import AES
import base64

# Cipher block size
BLOCK_SIZE = 16

# Padding character
PADDING = '{'

def pad(msg):
    return msg + (BLOCK_SIZE - len(msg) % BLOCK_SIZE) * PADDING

def decrypt(encrypted_data):
    '''
        returns a tuple of (args,kwargs)
    '''
    cipher = AES.new(pad(settings.PTRACK_SECRET),AES.MODE_ECB)
    data = cipher.decrypt(base64.b64decode(encrypted_data)).rstrip(PADDING)
    return json.loads(data)
    
def encrypt(*args, **kwargs):
    data = json.dumps((args, kwargs))
    cipher = AES.new(pad(settings.PTRACK_SECRET),AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(data)))