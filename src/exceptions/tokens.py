from fastapi import HTTPException, status


class TokenNotFoundHTTPException(HTTPException):
    """Исключение, когда токен не найден (401)."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )


class TokenExpiredHTTPException(HTTPException):
    """Исключение, когда токен истек (410)."""

    def __init__(self):
        super().__init__(status_code=status.HTTP_410_GONE, detail="Token expired")
