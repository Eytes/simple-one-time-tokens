from datetime import datetime
from typing import Literal

from pydantic import BaseModel, IPvAnyAddress


class TokenCreateRequest(BaseModel):
    """Схема запроса на создание одноразовой токена."""

    user_ip: IPvAnyAddress
    device_ip: IPvAnyAddress


class TokenCreateResponse(BaseModel):
    """Схема ответа при создании токена."""

    token: str


class TokenValidationResponse(BaseModel):
    """Схема успешного ответа при валидации токена."""

    status: Literal["success"] = "success"
    message: str = "Token validated successfully"


class TokenData(BaseModel):
    """Схема данных об одноразовой ссылке"""

    user_ip: str
    device_ip: str
    expires_at: datetime
