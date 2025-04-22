import os
from datetime import datetime, timedelta

from pydantic import BaseModel, IPvAnyAddress


class Settings(BaseModel):
    """
    Класс настроек, который используется для загрузки конфигурации из переменных окружения.

    **Атрибуты:**
    - `trusted_ips`: Список доверенных IP-адресов, получаемых из переменной окружения `TRUSTED_IPS`. Эти IP-адреса разрешены для выполнения операций с сервисом.
    - `http_host_url`: URL хоста сервиса, который извлекается из переменной окружения `HTTP_HOST_URL`. Используется для формирования ссылок и настройки подключения.
    - `token_ttl_seconds`: Время жизни токена (TTL), установленное с помощью переменной окружения или по умолчанию равное 30 сек. Определяет, сколько времени будет действительна одноразовый токен после создания.
    """

    trusted_ips: list[IPvAnyAddress] = list(
        set(os.getenv("TRUSTED_IPS", "").split(","))
    ) + ["127.0.0.1"]
    token_ttl_seconds: datetime = timedelta(
        seconds=int(os.getenv("TOKEN_TTL_SECONDS", default=30))
    )
    cleanup_interval: int = int(os.getenv("CLEANUP_INTERVAL", default=10))
    api_v1_prefix: str = "/api/v1"


settings = Settings()
