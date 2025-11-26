"""
數據庫連接和會話管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from backend.core.config import settings

# 創建引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

# 創建會話工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基礎模型類
Base = declarative_base()


def get_db():
    """獲取數據庫會話的依賴函數"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()