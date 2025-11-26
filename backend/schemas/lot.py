"""
批次記錄相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LotLogBase(BaseModel):
    """批次記錄基礎模型"""
    report_id: int
    lot_id: str = Field(..., max_length=50, description="批次ID")
    description: str = Field(..., description="異常內容描述")
    status: Optional[str] = Field(None, description="處置狀況")
    notes: Optional[str] = Field(None, description="特記事項")


class LotLogCreate(LotLogBase):
    """創建批次記錄模型"""
    pass


class LotLogUpdate(BaseModel):
    """更新批次記錄模型"""
    lot_id: Optional[str] = Field(None, max_length=50, description="批次ID")
    description: Optional[str] = Field(None, description="異常內容描述")
    status: Optional[str] = Field(None, description="處置狀況")
    notes: Optional[str] = Field(None, description="特記事項")


class LotLogResponse(LotLogBase):
    """批次記錄響應模型"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True