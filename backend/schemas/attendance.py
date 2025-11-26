"""
出勤記錄相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AttendanceCategory(str, Enum):
    """出勤類別"""
    REGULAR = "Regular"
    CONTRACTOR = "Contractor"


class AttendanceRecordBase(BaseModel):
    """出勤記錄基礎模型"""
    report_id: int
    category: AttendanceCategory
    scheduled_count: int = Field(0, ge=0, description="定員人數")
    present_count: int = Field(0, ge=0, description="出勤人數")
    absent_count: int = Field(0, ge=0, description="欠勤人數")
    reason: Optional[str] = Field(None, description="理由")


class AttendanceRecordCreate(AttendanceRecordBase):
    """創建出勤記錄模型"""
    pass


class AttendanceRecordUpdate(BaseModel):
    """更新出勤記錄模型"""
    category: Optional[AttendanceCategory] = Field(None, description="類別")
    scheduled_count: Optional[int] = Field(None, ge=0, description="定員人數")
    present_count: Optional[int] = Field(None, ge=0, description="出勤人數")
    absent_count: Optional[int] = Field(None, ge=0, description="欠勤人數")
    reason: Optional[str] = Field(None, description="理由")


class AttendanceRecordResponse(AttendanceRecordBase):
    """出勤記錄響應模型"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True