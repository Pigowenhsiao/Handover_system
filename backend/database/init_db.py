"""
初始化數據庫表
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings
from backend.database.base import Base
from backend.models.all_models import User
from passlib.context import CryptContext

# 創建引擎和會話工廠
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 密碼加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_default_admin():
    """創建默認管理員帳戶"""
    db = SessionLocal()

    try:
        # 檢查是否已存在管理員帳戶
        admin_user = db.query(User).filter(User.username == "Admin").first()
        if not admin_user:
            # 創建默認管理員帳戶 (密碼: 1234)
            hashed_password = pwd_context.hash("1234")
            admin = User(
                username="Admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("默認管理員帳戶已創建 (用戶名: Admin, 密碼: 1234)")
        else:
            print("管理員帳戶已存在，跳過創建")
    finally:
        db.close()


def init_db():
    """初始化數據庫"""
    print("正在初始化數據庫...")

    # 創建所有表
    Base.metadata.create_all(bind=engine)

    # 添加默認數據
    create_default_admin()

    print("數據庫初始化完成！")


if __name__ == "__main__":
    init_db()