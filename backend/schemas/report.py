"""
報告相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ShiftType(str, Enum):
    """班別類型"""
    DAY = "Day"
    NIGHT = "Night"


class AreaType(str, Enum):
    """區域類型"""
    ETCHING_D = "etching_D"
    ETCHING_E = "etching_E"
    LITHO = "litho"
    THIN_FILM = "thin_film"


class DailyReportBase(BaseModel):
    """日報表基礎模型"""
    date: str = Field(..., description="日期，格式: YYYY-MM-DD")
    shift: ShiftType = Field(..., description="班別")
    area: AreaType = Field(..., description="區域")
    summary_key_output: Optional[str] = Field(None, description="Key Machine Output 摘要")
    summary_issues: Optional[str] = Field(None, description="Key Issues 摘要")
    summary_countermeasures: Optional[str] = Field(None, description="Countermeasures 摘要")


class DailyReportCreate(DailyReportBase):
    """創建日報表模型"""
    pass


class DailyReportUpdate(BaseModel):
    """更新日報表模型"""
    date: Optional[str] = Field(None, description="日期，格式: YYYY-MM-DD")
    shift: Optional[ShiftType] = Field(None, description="班別")
    area: Optional[AreaType] = Field(None, description="區域")
    summary_key_output: Optional[str] = Field(None, description="Key Machine Output 摘要")
    summary_issues: Optional[str] = Field(None, description="Key Issues 摘要")
    summary_countermeasures: Optional[str] = Field(None, description="Countermeasures 摘要")


class DailyReportResponse(DailyReportBase):
    """日報表響應模型"""
    id: int
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True