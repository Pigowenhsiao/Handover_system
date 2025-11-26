"""
數據庫模型定義
包含 User, DailyReport, AttendanceRecord, EquipmentLog, LotLog, LanguageResource, LanguageSetting 等實體
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base


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

    # 設置關係
    daily_reports = relationship("DailyReport", back_populates="author")
    language_settings = relationship("LanguageSetting", back_populates="user")


class DailyReport(Base):
    """日報表模型"""
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)  # 報告日期
    shift = Column(String(10), nullable=False)  # 班別: 'Day', 'Night'
    area = Column(String(50), nullable=False)  # 區域: 'etching_D', 'etching_E', 'litho', 'thin_film'
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 摘要欄位
    summary_key_output = Column(Text)
    summary_issues = Column(Text)
    summary_countermeasures = Column(Text)

    # 設置關係
    author = relationship("User", back_populates="daily_reports")
    attendance_records = relationship("AttendanceRecord", back_populates="report", cascade="all, delete-orphan")
    equipment_logs = relationship("EquipmentLog", back_populates="report", cascade="all, delete-orphan")
    lot_logs = relationship("LotLog", back_populates="report", cascade="all, delete-orphan")


class AttendanceRecord(Base):
    """出勤記錄模型"""
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    category = Column(String(20), nullable=False)  # 'Regular', 'Contractor'
    scheduled_count = Column(Integer, default=0)  # 定員數
    present_count = Column(Integer, default=0)   # 出勤數
    absent_count = Column(Integer, default=0)    # 欠勤數
    reason = Column(Text)  # 理由
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # 設置關係
    report = relationship("DailyReport", back_populates="attendance_records")


class EquipmentLog(Base):
    """設備異常記錄模型"""
    __tablename__ = "equipment_logs"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    equip_id = Column(String(50), nullable=False)  # 設備ID
    description = Column(Text, nullable=False)     # 異常內容
    start_time = Column(Time)                      # 發生時刻
    impact_qty = Column(Integer, default=0)        # 影響數量
    action_taken = Column(Text)                    # 對應內容
    image_path = Column(String(255), nullable=True)  # 圖片路徑
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # 設置關係
    report = relationship("DailyReport", back_populates="equipment_logs")


class LotLog(Base):
    """異常批次記錄模型"""
    __tablename__ = "lot_logs"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    lot_id = Column(String(50), nullable=False)    # 批號
    description = Column(Text, nullable=False)     # 異常內容
    status = Column(Text)                          # 處置狀況
    notes = Column(Text)                           # 特記事項
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # 設置關係
    report = relationship("DailyReport", back_populates="lot_logs")


class LanguageResource(Base):
    """語言資源模型"""
    __tablename__ = "language_resources"

    id = Column(Integer, primary_key=True, index=True)
    language_code = Column(String(10), nullable=False)  # 'ja', 'zh', 'en'
    resource_key = Column(String(255), nullable=False)  # 翻譯鍵
    resource_value = Column(Text, nullable=False)       # 翻譯值
    namespace = Column(String(100), default='common')   # 命名空間
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 最後更新用戶


class LanguageSetting(Base):
    """語言設定模型"""
    __tablename__ = "language_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL表示系統默認
    language_code = Column(String(10), nullable=False)  # 'ja', 'zh', 'en'
    is_default = Column(Boolean, default=False)  # 是否為默認語言
    is_active = Column(Boolean, default=True)    # 該語言是否啟用
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 設置關係
    user = relationship("User", back_populates="language_settings")