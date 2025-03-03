from fastapi import status
from ..schemas.link import LinkCreateResponse, LinkValidationResponse

CREATE_LINK_RESPONSES = {
    status.HTTP_201_CREATED: {
        "description": "Ссылка успешно создана",
        "model": LinkCreateResponse,
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

VALIDATE_LINK_RESPONSES = {
    status.HTTP_200_OK: {
        "description": "Ссылка успешно валидирована",
        "model": LinkValidationResponse,
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Ссылка не найдена",
        "content": {
            "application/json": {
                "example": {"detail": "Link not found"},
            },
        },
    },
    status.HTTP_410_GONE: {
        "description": "Срок действия ссылки истек",
        "content": {
            "application/json": {
                "example": {"detail": "Link expired"},
            },
        },
    },
}
