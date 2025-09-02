from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Ride-Matching API"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite:///./data/rides.db"
    secret_key: str = "riding-app"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = ["*"]
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()