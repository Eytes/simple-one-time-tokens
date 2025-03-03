from pydantic import BaseModel, IPvAnyAddress
from datetime import datetime
from typing import Literal


class LinkCreateRequest(BaseModel):
    """Схема запроса на создание одноразовой ссылки."""

    user_ip: IPvAnyAddress
    device_ip: IPvAnyAddress


class LinkCreateResponse(BaseModel):
    """Схема ответа при создании ссылки."""

    link: str
    expires_at: datetime


class LinkValidationResponse(BaseModel):
    """Схема успешного ответа при валидации ссылки."""

    status: Literal["success"]
    message: str


class LinkData(BaseModel):
    """Схема данных об одноразовой ссылке"""

    user_ip: str
    device_ip: str
    expires_at: datetime
