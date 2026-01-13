from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    APP_NAME: str = "Flowhive"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://flowhive-crystal.vercel.app"

    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
