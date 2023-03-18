import sys

import win32crypt
from pydantic import SecretStr



class Win32Crypt:
    """Custom type that automatically decrypts a password encrypted with
    `win32crypt.CryptProtectData`."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: int | str) -> SecretStr:
        v = int(v)
        _, decrypted = win32crypt.CryptUnprotectData(
            v.to_bytes(
                (v.bit_length() + 7) // 8,
                byteorder=sys.byteorder
            )
        )
        return SecretStr(decrypted.decode())
