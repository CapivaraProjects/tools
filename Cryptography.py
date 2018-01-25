import os
import json
import base64
from sjcl import SJCL


class Crypto:
    """
    Cryptography class
    """

    def __init__(self, keySize=24):
        self.keySize = keySize

    def generateRandomSalt(self):
        """
        () -> String
        Generates random salt
        """
        return base64.b64encode(os.urandom(self.keySize)).decode('utf-8')

    def encrypt(self, salt, plainText):
        """
        (String, String) -> String
        Encrypt a text
        """

        ciphred = SJCL().encrypt(plainText.encode('utf-8'), salt)
        ciphred['ct'] = base64.b64encode(ciphred.get('ct')).decode('utf-8')
        ciphred['salt'] = base64.b64encode(ciphred.get('salt')).decode('utf-8')
        ciphred['iv'] = base64.b64encode(ciphred.get('iv')).decode('utf-8')

        return base64.b64encode(bytes(json.dumps(ciphred), 'utf-8')).decode()

    def decrypt(self, salt, ciphredText):
        """
        (String, String) -> String
        Decrypt a text
        """
        ciphred = json.loads(base64.b64decode(
                    ciphredText.encode('utf-8')).decode(
                        'utf-8'))
        ciphred['ct'] = base64.b64decode(ciphred.get('ct'))
        ciphred['salt'] = base64.b64decode(ciphred.get('salt'))
        ciphred['iv'] = base64.b64decode(ciphred.get('iv'))
        return SJCL().decrypt(ciphred, salt).decode('utf-8')
