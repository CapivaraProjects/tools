from .Cryptography import Crypto


def test_generateRandomSalt():
    """
    () -> None
    Tests if salt have length of 32 chars
    """
    crypto = Crypto(keySize=24)
    assert len(crypto.generateRandomSalt()) == 32


def test_encrypt_decrypt():
    """
    () -> None
    Tests encrypt and decrypt functions
    """
    crypto = Crypto()
    salt = 'KFhukFqCnte7GiVQEgKqDM7zeNcoer0B'
    ciphredText = crypto.encrypt(salt, 'test')
    assert crypto.decrypt(salt, ciphredText) == 'test'
