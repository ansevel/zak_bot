from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )

    telegram_api_token: str
    admin_ids: list[int]

    database_url: str


settings = Settings()
