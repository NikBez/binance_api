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
        'https://api.binance.com',
        'https://api1.binance.com',
        'https://api2.binance.com',
        'https://api3.binance.com'
    ]
    BINANCE_TESTNET_BASE_URL: str = 'https://testnet.binance.vision'

SETTINGS = Settings()

