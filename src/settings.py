import os
from datetime import datetime, timedelta

from pydantic import BaseModel, IPvAnyAddress


class Settings(BaseModel):
    """
    Класс настроек, который используется для загрузки конфигурации из переменных окружения.

    **Атрибуты:**
    - `trusted_ips`: Список доверенных IP-адресов, получаемых из переменной окружения `TRUSTED_IPS`. Эти IP-адреса разрешены для выполнения операций с сервисом.
    - `token_ttl_seconds`: Время жизни токена (TTL), установленное с помощью переменной окружения или по умолчанию равное 30 сек. Определяет, сколько времени будет действительна одноразовый токен после создания.
    - `cleanup_interval`: Время запуска фоновой задачи для очистку токенов, устанновленного с помощью переменной окрежения или по умолчанию равное 10 сек. Определяет время, спустя которое будет запущен фоновый процесс для очистки истекших токенов.
    """

    trusted_ips: list[IPvAnyAddress] = list(
        set(os.getenv("TRUSTED_IPS", "").split(","))
    )
    token_ttl_seconds: datetime = timedelta(
        seconds=int(os.getenv("TOKEN_TTL_SECONDS", default=30))
    )
    cleanup_interval: int = int(os.getenv("CLEANUP_INTERVAL", default=10))
    api_v1_prefix: str = "/api/v1"


settings = Settings()
