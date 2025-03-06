import secrets
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.get_client_ip import get_client_ip
from docs.responses import CREATE_LINK_RESPONSES, VALIDATE_LINK_RESPONSES
from exceptions.access import AccessDeniedHTTPException
from exceptions.links import LinkExpiredHTTPException, LinkNotFoundHTTPException
from schemas.token import (
    TokenCreateRequest,
    TokenCreateResponse,
    TokenData,
    TokenValidationResponse,
)
from settings import settings

router = APIRouter()

# Временное хранилище ссылок
tokens: dict[str, TokenData] = {}


@router.post(
    path="/create",
    response_model=TokenCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_LINK_RESPONSES,
)
async def create_token(
    data: TokenCreateRequest,
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    """Создает одноразовую ссылку, если запрос поступает от доверенного IP."""
    if client_ip not in settings.trusted_ips:
        raise AccessDeniedHTTPException()

    api_token = secrets.token_urlsafe(16)

    tokens[api_token] = TokenData(
        user_ip=str(data.user_ip),
        device_ip=str(data.device_ip),
        expires_at=datetime.now(UTC) + settings.link_ttl_seconds,
    )

    return TokenCreateResponse(token=api_token)


@router.post(
    path="/validate",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK,
    responses=VALIDATE_LINK_RESPONSES,
)
async def validate_token(
    token: str,
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    """Проверяет валидность одноразовой ссылки и удаляет ее при успешном использовании."""
    token_data = tokens.get(token)

    if not token_data:
        raise LinkNotFoundHTTPException()

    if datetime.now(UTC) > token_data.expires_at:
        del tokens[token]
        raise LinkExpiredHTTPException()

    if client_ip not in [token_data.user_ip, token_data.device_ip]:
        raise AccessDeniedHTTPException()

    del tokens[token]
    return TokenValidationResponse()
