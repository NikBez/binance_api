from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    # API settings
    BINANCE_API: SecretStr
    BINANCE_SECRET: SecretStr
    BINANCE_BASE_URLS: list[str] = [
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com",
    ]
    BINANCE_TESTNET_BASE_URL: str = "https://testnet.binance.vision"

    # database settings
    POSTGRES_HOST: StrictStr
    POSTGRES_PORT: int
    POSTGRES_USER: StrictStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: StrictStr
    POSTGRES_ECHO: bool = False
    DB_URL: StrictStr | None = ""

    get_pair_price_default_periodicy: int = 10

    TELEGRAM_BOT_TOKEN: SecretStr

    # rabbitmq settings
    RABBITMQ_URL: str
    TELEGRAM_QUEUE_NAME: str
    SERVER_QUEUE_NAME: str


SETTINGS = Settings()

SETTINGS.DB_URL = (
    "postgresql+asyncpg:"
    f"//{SETTINGS.POSTGRES_USER}:"
    f"{SETTINGS.POSTGRES_PASSWORD.get_secret_value()}"
    f"@{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}"
    f"/{SETTINGS.POSTGRES_DB}"
)
