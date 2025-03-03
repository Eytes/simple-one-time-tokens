from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

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
