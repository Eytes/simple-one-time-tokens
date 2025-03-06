from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    path="/health",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Проверка состояния сервиса.
    Возвращает успешный статус, если сервис работает корректно.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=status.HTTP_200_OK)
