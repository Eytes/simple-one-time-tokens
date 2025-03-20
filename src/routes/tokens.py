import secrets
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from db.tokens import TOKENS
from dependencies.ip import get_requesters_ip, is_trusted_ip, get_user_ip
from dependencies.tokens import token_validate
from docs.responses import CREATE_TOKEN_RESPONSES, VALIDATE_TOKEN_RESPONSES
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
    responses=CREATE_TOKEN_RESPONSES,
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
        expires_at=datetime.now(UTC) + settings.token_ttl_seconds,
    )

    return TokenCreateResponse(token=api_token)


@router.post(
    path="/validate",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK,
    responses=VALIDATE_TOKEN_RESPONSES,
)
async def validate_token(
    token: Annotated[str, Depends(token_validate)],
    device_ip: Annotated[str, Depends(get_requesters_ip)],
    user_ip: Annotated[str, Depends(get_user_ip)],
):
    """Проверяет валидность одноразового токена и удаляет его при успешной проверке."""
    token_data = TOKENS.get(token)
    if (device_ip != token_data.device_ip) and (user_ip != token_data.user_ip):
        raise AccessDeniedHTTPException()

    del TOKENS[token]
    return TokenValidationResponse()
