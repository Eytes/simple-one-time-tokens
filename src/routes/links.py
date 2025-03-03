from typing import Annotated

from fastapi import APIRouter, status, Depends
from datetime import datetime, UTC
import secrets

from dependencies.get_client_ip import get_client_ip
from settings import settings
from schemas.link import (
    LinkCreateRequest,
    LinkCreateResponse,
    LinkValidationResponse,
    LinkData,
)
from exceptions.links import LinkNotFoundHTTPException, LinkExpiredHTTPException
from exceptions.access import AccessDeniedHTTPException
from docs.responses import CREATE_LINK_RESPONSES, VALIDATE_LINK_RESPONSES

router = APIRouter()

# Временное хранилище ссылок
links: dict[str, LinkData] = {}


@router.post(
    "/",
    response_model=LinkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_LINK_RESPONSES,
)
async def create_link(
    data: LinkCreateRequest,
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    """Создает одноразовую ссылку, если запрос поступает от доверенного IP."""
    if client_ip not in settings.trusted_ips:
        raise AccessDeniedHTTPException()

    api_token = secrets.token_urlsafe(16)
    expires_at = datetime.now(UTC) + settings.link_ttl_seconds

    links[api_token] = LinkData(
        user_ip=str(data.user_ip),
        device_ip=str(data.device_ip),
        expires_at=expires_at,
    )

    return LinkCreateResponse(
        link=f"{settings.http_host_url}/{settings.api_v1_prefix}/links/{api_token}",
        expires_at=expires_at,
    )


@router.get(
    "/{token}",
    response_model=LinkValidationResponse,
    status_code=status.HTTP_200_OK,
    responses=VALIDATE_LINK_RESPONSES,
)
async def validate_link(
    token: str,
    client_ip: Annotated[str, Depends(get_client_ip)],
):
    """Проверяет валидность одноразовой ссылки и удаляет ее при успешном использовании."""
    link_data = links.get(token)

    if not link_data:
        raise LinkNotFoundHTTPException()

    if datetime.now(UTC) > link_data["expires_at"]:
        del links[token]
        raise LinkExpiredHTTPException()

    if client_ip != link_data.user_ip:
        raise AccessDeniedHTTPException()

    del links[token]
    return LinkValidationResponse(
        status="success",
        message="Link validated successfully",
    )
