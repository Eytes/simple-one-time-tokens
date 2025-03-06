from fastapi import Depends, Request
from typing_extensions import Annotated

from exceptions.access import AccessDeniedHTTPException
from settings import settings


def get_client_ip(request: Request) -> str:
    """
    Извлекает IP-адрес клиента из объекта запроса.

    **Параметры:**
    - `request`: Объект запроса FastAPI, содержащий информацию о клиенте.

    **Возвращаемое значение:**
    - Строка, представляющая IP-адрес клиента, сделавшего запрос.

    Используется для получения IP-адреса клиента, который отправил запрос, что полезно для проверки и авторизации доступа, а также для логирования.
    """
    return request.client.host


def is_trusted_ip(ip: Annotated[str, Depends(get_client_ip)]) -> str:
    """Проверка, что ip адрес является доверенным"""
    if ip not in settings.trusted_ips:
        raise AccessDeniedHTTPException()
    return ip
