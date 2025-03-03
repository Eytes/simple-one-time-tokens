import os
from datetime import timedelta, datetime

from pydantic import BaseModel, IPvAnyAddress, HttpUrl


class Settings(BaseModel):
    """
    Класс настроек, который используется для загрузки конфигурации из переменных окружения.

    **Атрибуты:**
    - `trusted_ips`: Список доверенных IP-адресов, получаемых из переменной окружения `TRUSTED_IPS`. Эти IP-адреса разрешены для выполнения операций с сервисом.
    - `http_host_url`: URL хоста сервиса, который извлекается из переменной окружения `HTTP_HOST_URL`. Используется для формирования ссылок и настройки подключения.
    - `link_ttl`: Время жизни ссылки (TTL), установленное с помощью переменной окружения или по умолчанию равное 30 сек. Определяет, сколько времени будет действительна одноразовая ссылка после ее создания.
    """

    trusted_ips: list[IPvAnyAddress] = list(
        set(os.getenv("TRUSTED_IPS", "").split(","))
    )
    http_host_url: HttpUrl = os.getenv("HTTP_HOST_URL")
    link_ttl: datetime = os.getenv("LINK_TTL") or timedelta(seconds=30)
    api_v1_prefix: str = "/api/v1"


settings = Settings()
