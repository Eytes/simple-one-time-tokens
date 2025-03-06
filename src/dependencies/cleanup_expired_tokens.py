import asyncio
import logging
from datetime import UTC, datetime

from routes.tokens import tokens  # Импорт временного хранилища ссылок
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def cleanup_expired_tokens(interval: int = settings.cleanup_interval) -> None:
    """
    Фоновая задача для периодического удаления просроченных одноразовых ссылок.

    Args:
        interval (int): Интервал проверки (в секундах).
    """
    while True:
        now = datetime.now(UTC)
        expired_keys = [
            token for token, token_data in tokens.items() if token_data.expires_at < now
        ]

        if expired_keys:
            for token in expired_keys:
                del tokens[token]
                logger.info(f"Удален просроченный токен: {token}")

        # Ждём заданный интервал перед следующей проверкой
        await asyncio.sleep(interval)
