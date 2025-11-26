"""
數據庫初始化腳本
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from backend.core.config import settings
import hashlib


# 創建引擎和基礎模型類
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """使用者模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # "admin", "user"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


def init_db():
    """初始化數據庫並創建表"""
    print("正在初始化數據庫...")
    
    # 創建所有表
    Base.metadata.create_all(bind=engine)
    
    # 添加默認管理員用戶
    db = SessionLocal()
    try:
        # 檢查是否已存在管理員用戶
        admin_user = db.query(User).filter(User.username == "Admin").first()
        if not admin_user:
            # 創建默認管理員用戶 (密碼: 1234)
            password_hash = hashlib.sha256("1234".encode()).hexdigest()
            admin = User(
                username="Admin",
                email="admin@example.com",
                hashed_password=password_hash,
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("默認管理員用戶已創建 (用戶名: Admin, 密碼: 1234)")
        else:
            print("管理員用戶已存在")
    except Exception as e:
        print(f"創建默認用戶時發生錯誤: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("數據庫初始化完成！")


if __name__ == "__main__":
    init_db()