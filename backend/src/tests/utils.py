import uuid
from typing import Union


def add_authorization_header(
    token: Union[str, uuid.UUID],
    headers: dict[str, str] = None,
) -> dict[str, str]:

    header = {}
    header['Authorization'] = 'Bearer {}'.format(token)

    if headers:
        header = header | headers

    return header

