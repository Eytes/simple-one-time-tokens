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


def get_user_ip(request: Request) -> str | None:
    """
    Извлекает IP-адрес клиента из заголовка `X-Real-IP`.

    **Параметры:**
    - `request` (Request): Объект запроса FastAPI.

    **Возвращаемое значение:**
    - `str | None`: IP-адрес клиента, если заголовок `X-Real-IP` присутствует, иначе `None`.

    **Описание:**
    Функция проверяет заголовок `X-Real-IP` и возвращает IP-адрес клиента,
    который был передан через прокси-сервер. Если заголовок отсутствует, возвращает `None`.
    """
    return request.headers.get("X-Real-IP")


def is_trusted_ip(ip: Annotated[str, Depends(get_requesters_ip)]) -> str:
    """
    Проверяет, является ли IP-адрес клиента доверенным.

    **Параметры:**
    - `ip` (str): IP-адрес клиента, полученный через `get_requesters_ip()`.

    **Возвращаемое значение:**
    - `str`: IP-адрес клиента, если он находится в списке доверенных.

    **Исключения:**
    - `AccessDeniedHTTPException`: Вызывается, если IP-адрес не является доверенным.

    **Описание:**
    Функция проверяет, содержится ли переданный IP-адрес в списке доверенных `settings.trusted_ips`.
    Если адрес не является доверенным, вызывается исключение `AccessDeniedHTTPException()`.
    """
    if ip not in settings.trusted_ips:
        raise AccessDeniedHTTPException()
    return ip
