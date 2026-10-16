from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Aegis"
    database_url: str = "postgresql+psycopg2://aegis:aegis@localhost:5432/aegis"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 60
    otel_service_name: str = "aegis-api"
    log_level: str = "INFO"


settings = Settings()
