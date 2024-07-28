from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
