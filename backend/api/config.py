from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
