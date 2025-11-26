"""
CRUD 操作實現
包含對 User, DailyReport, AttendanceRecord, EquipmentLog, LotLog 的基本操作
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
import logging

from backend.models.all_models import User, DailyReport, AttendanceRecord, EquipmentLog, LotLog, LanguageSetting
from backend.schemas.user import UserCreate, UserUpdate
from backend.schemas.report import DailyReportCreate, DailyReportUpdate
from backend.schemas.attendance import AttendanceRecordCreate, AttendanceRecordUpdate
from backend.schemas.equipment import EquipmentLogCreate, EquipmentLogUpdate
from backend.schemas.lot import LotLogCreate, LotLogUpdate
from backend.core.security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[User]:
    """獲取用戶"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根據電子郵件獲取用戶"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根據用戶名獲取用戶"""
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """獲取用戶列表"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """創建用戶"""
    try:
        # 創建用戶對象
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            role=user.role,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="用戶名或電子郵件已存在"
        )


def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
    """更新用戶信息"""
    try:
        # 更新用戶屬性
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.role is not None:
            db_user.role = user_update.role
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active
        if user_update.password is not None:
            db_user.hashed_password = get_password_hash(user_update.password)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="用戶名或電子郵件已存在"
        )


def delete_user(db: Session, db_user: User) -> User:
    """刪除用戶"""
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """驗證用戶"""
    from backend.core.security import verify_password
    user = get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_daily_report(db: Session, report_id: int) -> Optional[DailyReport]:
    """獲取日報表"""
    return db.query(DailyReport).filter(DailyReport.id == report_id).first()


def get_daily_reports(db: Session, skip: int = 0, limit: int = 100) -> List[DailyReport]:
    """獲取日報表列表"""
    return db.query(DailyReport).offset(skip).limit(limit).all()


def get_daily_reports_by_date_range(db: Session, start_date: str, end_date: str) -> List[DailyReport]:
    """根據日期範圍獲取日報表"""
    from datetime import datetime
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") 
    
    return db.query(DailyReport).filter(
        DailyReport.date >= start_dt,
        DailyReport.date <= end_dt
    ).all()


def create_daily_report(db: Session, report: DailyReportCreate, author_id: int) -> DailyReport:
    """創建日報表"""
    db_report = DailyReport(
        date=report.date,
        shift=report.shift,
        area=report.area,
        author_id=author_id,
        summary_key_output=report.summary_key_output,
        summary_issues=report.summary_issues,
        summary_countermeasures=report.summary_countermeasures
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_daily_report(db: Session, report_id: int, report_update: DailyReportUpdate) -> Optional[DailyReport]:
    """更新日報表"""
    db_report = get_daily_report(db, report_id)
    if not db_report:
        return None
    
    if report_update.date is not None:
        db_report.date = report_update.date
    if report_update.shift is not None:
        db_report.shift = report_update.shift
    if report_update.area is not None:
        db_report.area = report_update.area
    if report_update.summary_key_output is not None:
        db_report.summary_key_output = report_update.summary_key_output
    if report_update.summary_issues is not None:
        db_report.summary_issues = report_update.summary_issues
    if report_update.summary_countermeasures is not None:
        db_report.summary_countermeasures = report_update.summary_countermeasures
    
    db.commit()
    db.refresh(db_report)
    return db_report


def delete_daily_report(db: Session, report_id: int) -> bool:
    """刪除日報表"""
    db_report = get_daily_report(db, report_id)
    if not db_report:
        return False
    
    db.delete(db_report)
    db.commit()
    return True


def get_attendance_records(db: Session, report_id: int) -> List[AttendanceRecord]:
    """獲取指定報表的出勤記錄"""
    return db.query(AttendanceRecord).filter(AttendanceRecord.report_id == report_id).all()


def create_attendance_record(db: Session, record: AttendanceRecordCreate) -> AttendanceRecord:
    """創建出勤記錄"""
    db_record = AttendanceRecord(
        report_id=record.report_id,
        category=record.category,
        scheduled_count=record.scheduled_count,
        present_count=record.present_count,
        absent_count=record.absent_count,
        reason=record.reason
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_attendance_record(db: Session, record_id: int, record_update: AttendanceRecordUpdate) -> Optional[AttendanceRecord]:
    """更新出勤記錄"""
    db_record = db.query(AttendanceRecord).filter(AttendanceRecord.id == record_id).first()
    if not db_record:
        return None
    
    if record_update.category is not None:
        db_record.category = record_update.category
    if record_update.scheduled_count is not None:
        db_record.scheduled_count = record_update.scheduled_count
    if record_update.present_count is not None:
        db_record.present_count = record_update.present_count
    if record_update.absent_count is not None:
        db_record.absent_count = record_update.absent_count
    if record_update.reason is not None:
        db_record.reason = record_update.reason
    
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_attendance_record(db: Session, record_id: int) -> bool:
    """刪除出勤記錄"""
    db_record = db.query(AttendanceRecord).filter(AttendanceRecord.id == record_id).first()
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True


def get_equipment_logs(db: Session, report_id: int) -> List[EquipmentLog]:
    """獲取指定報表的設備記錄"""
    return db.query(EquipmentLog).filter(EquipmentLog.report_id == report_id).all()


def create_equipment_log(db: Session, log: EquipmentLogCreate) -> EquipmentLog:
    """創建設備記錄"""
    db_log = EquipmentLog(
        report_id=log.report_id,
        equip_id=log.equip_id,
        description=log.description,
        start_time=log.start_time,
        impact_qty=log.impact_qty,
        action_taken=log.action_taken,
        image_path=log.image_path
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_equipment_log(db: Session, log_id: int, log_update: EquipmentLogUpdate) -> Optional[EquipmentLog]:
    """更新設備記錄"""
    db_log = db.query(EquipmentLog).filter(EquipmentLog.id == log_id).first()
    if not db_log:
        return None
    
    if log_update.equip_id is not None:
        db_log.equip_id = log_update.equip_id
    if log_update.description is not None:
        db_log.description = log_update.description
    if log_update.start_time is not None:
        db_log.start_time = log_update.start_time
    if log_update.impact_qty is not None:
        db_log.impact_qty = log_update.impact_qty
    if log_update.action_taken is not None:
        db_log.action_taken = log_update.action_taken
    if log_update.image_path is not None:
        db_log.image_path = log_update.image_path
    
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_equipment_log(db: Session, log_id: int) -> bool:
    """刪除設備記錄"""
    db_log = db.query(EquipmentLog).filter(EquipmentLog.id == log_id).first()
    if not db_log:
        return False
    
    db.delete(db_log)
    db.commit()
    return True


def get_lot_logs(db: Session, report_id: int) -> List[LotLog]:
    """獲取指定報表的批次記錄"""
    return db.query(LotLog).filter(LotLog.report_id == report_id).all()


def create_lot_log(db: Session, log: LotLogCreate) -> LotLog:
    """創建批次記錄"""
    db_log = LotLog(
        report_id=log.report_id,
        lot_id=log.lot_id,
        description=log.description,
        status=log.status,
        notes=log.notes
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_lot_log(db: Session, log_id: int, log_update: LotLogUpdate) -> Optional[LotLog]:
    """更新批次記錄"""
    db_log = db.query(LotLog).filter(LotLog.id == log_id).first()
    if not db_log:
        return None
    
    if log_update.lot_id is not None:
        db_log.lot_id = log_update.lot_id
    if log_update.description is not None:
        db_log.description = log_update.description
    if log_update.status is not None:
        db_log.status = log_update.status
    if log_update.notes is not None:
        db_log.notes = log_update.notes
    
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_lot_log(db: Session, log_id: int) -> bool:
    """刪除批次記錄"""
    db_log = db.query(LotLog).filter(LotLog.id == log_id).first()
    if not db_log:
        return False
    
    db.delete(db_log)
    db.commit()
    return True


def get_user_language_setting(db: Session, user_id: int) -> Optional[LanguageSetting]:
    """獲取用戶的語言設置"""
    return db.query(LanguageSetting).filter(LanguageSetting.user_id == user_id).first()


def get_system_default_language_setting(db: Session) -> Optional[LanguageSetting]:
    """獲取系統默認語言設置"""
    return db.query(LanguageSetting).filter(
        LanguageSetting.user_id.is_(None),
        LanguageSetting.is_default == True
    ).first()


def update_user_language_setting(db: Session, user_id: int, language_code: str) -> Optional[LanguageSetting]:
    """更新用戶的語言設置"""
    db_setting = get_user_language_setting(db, user_id)
    if not db_setting:
        # 如果用戶沒有設置語言，則創建一個
        db_setting = LanguageSetting(
            user_id=user_id,
            language_code=language_code,
            is_default=False,
            is_active=True
        )
        db.add(db_setting)
    else:
        db_setting.language_code = language_code
    
    db.commit()
    db.refresh(db_setting)
    return db_setting