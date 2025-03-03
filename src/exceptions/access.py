from fastapi import HTTPException, status


class AccessDeniedHTTPException(HTTPException):
    """Исключение для отказа в доступе (403)."""

    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
