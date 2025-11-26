"""
後端配置文件
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """應用程序設置"""
    PROJECT_NAME: str = "電子交接系統"
    DESCRIPTION: str = "支援多語言的電子交接系統"
    VERSION: str = "1.0.0"
    
    # API 設置
    API_V1_STR: str = "/api/v1"
    
    # 安全設置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 服務器設置
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", "8000"))
    BACKEND_CORS_ORIGINS: list = ["*"]  # 在生產環境中應指定更具體的來源
    
    # 數據庫設置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./handover_system.db")
    
    # 上傳設置
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "./uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 多語言設置
    SUPPORTED_LANGUAGES: list = ["ja", "zh", "en"]
    DEFAULT_LANGUAGE: str = "ja"

    class Config:
        env_file = ".env"


# 創建設置實例
settings = Settings()