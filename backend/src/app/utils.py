from app import settings


def _get_backend_address(host: str, port: str) -> str:
    return '{0}://{1}:{2}'.format(
        settings.HTTP_PROTOCOL,
        host,
        port
    )


def get_backend_address() -> str:
    return _get_backend_address(
        settings.HOST,
        settings.PORT
    )


def get_external_backend_address() -> str:
    return _get_backend_address(
        settings.EXTERNAL_HOST,
        settings.EXTERNAL_PORT
    )


def get_external_url_to_route(path: str = '/') -> str:
    return '{0}{1}'.format(
        get_external_backend_address(),
        path
    )

