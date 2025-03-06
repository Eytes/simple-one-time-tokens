import secrets
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from db.tokens import TOKENS
from dependencies.ip import get_client_ip, is_trusted_ip
from dependencies.tokens import token_validate
from dependencies.get_client_ip import get_client_ip
from docs.responses import CREATE_LINK_RESPONSES, VALIDATE_LINK_RESPONSES
from exceptions.access import AccessDeniedHTTPException
from schemas.token import (
    TokenCreateRequest,
    TokenCreateResponse,
    TokenData,
    TokenValidationResponse,
)
from settings import settings

router = APIRouter()


@router.post(
    path="/create",
    response_model=TokenCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_LINK_RESPONSES,
)
async def create_token(
    data: TokenCreateRequest,
    trusted_ip: Annotated[str, Depends(is_trusted_ip)],
):
    """Создает одноразовый токен, если запрос поступает от доверенного IP."""
    api_token = secrets.token_urlsafe(16)

    TOKENS[api_token] = TokenData(
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
    token: Annotated[str, Depends(token_validate)],
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    """Проверяет валидность одноразовой ссылки и удаляет ее при успешном использовании."""
    token_data = TOKENS.get(token)
    if client_ip not in [token_data.user_ip, token_data.device_ip]:
        raise AccessDeniedHTTPException()

    del TOKENS[token]
    return TokenValidationResponse()


@router.get(path="/get")
def get_tokens():
    return TOKENS
