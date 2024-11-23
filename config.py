from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_DB: str = "postgres"

    KAFKA_BROKER: str = "kafka:9092"

    JWT_SECRET: str = "09d25e094faa6ca2556c81816X6b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    TOKEN_EXPIRATION_DELTA: int = 10

    DEBUG_ENGINE: bool = False


settings = Settings()
