from fastapi import status

from schemas.token import TokenCreateResponse, TokenValidationResponse

CREATE_TOKEN_RESPONSES = {
    status.HTTP_201_CREATED: {
        "description": "Токен успешно создан",
        "model": TokenCreateResponse,
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Доступ запрещен",
        "content": {
            "application/json": {
                "example": {"detail": "Access denied"},
            },
        },
    },
}

VALIDATE_TOKEN_RESPONSES = {
    status.HTTP_200_OK: {
        "description": "Токен успешно валидирована",
        "model": TokenValidationResponse,
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Токен не найден",
        "content": {
            "application/json": {
                "example": {"detail": "Token not found"},
            },
        },
    },
    status.HTTP_410_GONE: {
        "description": "Срок действия токена истек",
        "content": {
            "application/json": {
                "example": {"detail": "Token expired"},
            },
        },
    },
}
