from secrets import token_hex

from passlib.hash import pbkdf2_sha256

from app import settings


def generate_authorization_token() -> str:
    return token_hex(settings.TOKEN_SIZE // 2)


def hash_password(raw_password: str) -> str:
    return pbkdf2_sha256.hash(raw_password)


def check_password(raw_pasword: str, hash_password: str) -> bool:
    return pbkdf2_sha256.verify(raw_pasword, hash_password)

