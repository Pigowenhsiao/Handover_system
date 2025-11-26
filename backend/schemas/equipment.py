"""
設備記錄相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EquipmentLogBase(BaseModel):
    """設備記錄基礎模型"""
    report_id: int
    equip_id: str = Field(..., max_length=50, description="設備ID")
    description: str = Field(..., description="異常內容描述")
    start_time: Optional[str] = Field(None, description="發生時刻，格式: HH:MM")
    impact_qty: Optional[int] = Field(0, ge=0, description="影響數量")
    action_taken: Optional[str] = Field(None, description="對應內容")
    image_path: Optional[str] = Field(None, description="圖片路徑")


class EquipmentLogCreate(EquipmentLogBase):
    """創建設備記錄模型"""
    pass


class EquipmentLogUpdate(BaseModel):
    """更新設備記錄模型"""
    equip_id: Optional[str] = Field(None, max_length=50, description="設備ID")
    description: Optional[str] = Field(None, description="異常內容描述")
    start_time: Optional[str] = Field(None, description="發生時刻，格式: HH:MM")
    impact_qty: Optional[int] = Field(None, ge=0, description="影響數量")
    action_taken: Optional[str] = Field(None, description="對應內容")
    image_path: Optional[str] = Field(None, description="圖片路徑")


class EquipmentLogResponse(EquipmentLogBase):
    """設備記錄響應模型"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True