from fastapi import HTTPException, status


class LinkNotFoundHTTPException(HTTPException):
    """Исключение, когда ссылка не найдена (404)."""

    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")


class LinkExpiredHTTPException(HTTPException):
    """Исключение, когда ссылка истекла (410)."""

    def __init__(self):
        super().__init__(status_code=status.HTTP_410_GONE, detail="Link expired")
