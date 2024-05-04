import re

from passlib.hash import pbkdf2_sha256

from app import settings
from auth.utils import (
    generate_authorization_token,
    hash_password,
    check_password
)


def test_generate_authorization_token():
    pattern = r'^[0-9a-f]{48}$'     # settings.TOKEN_SIZE = 48

    token = generate_authorization_token()
    assert len(token) == settings.TOKEN_SIZE

    match_token = re.fullmatch(pattern, token)
    assert isinstance(match_token, re.Match)
    assert match_token[0] == token


def test_hash_password():
    raw_password1 = 'YG2f728dg-id9'
    password1 = hash_password(raw_password1)
    assert raw_password1 != password1
    assert pbkdf2_sha256.verify(raw_password1, password1) == True


def test_check_password():
    raw_password1 = 'YG2f728dg-id9'
    password1 = hash_password(raw_password1)
    assert check_password(raw_password1, password1)

