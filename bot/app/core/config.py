from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_nested_delimiter='__')

    telegram_api_token: str
    database_url: str = 'sqlite+aiosqlite:///./zakupki_bot.db'
    admin_ids: list[int]


settings = Settings()
