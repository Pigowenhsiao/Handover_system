"""
Pydantic 架構定義
用於 API 請求/響應驗證
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# 用戶相關架構
class UserRole(str, Enum):
    """用戶角色枚舉"""
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """用戶基礎架構"""
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[UserRole] = UserRole.USER
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """創建用戶架構"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """更新用戶架構"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)


class UserInDBBase(UserBase):
    """數據庫用戶基礎架構"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserInDBBase):
    """用戶響應架構"""
    pass


# 認證相關架構
class Token(BaseModel):
    """令牌架構"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌數據架構"""
    username: Optional[str] = None


# 日報表相關架構
class ShiftType(str, Enum):
    """班別類型枚舉"""
    DAY = "Day"
    NIGHT = "Night"


class AreaType(str, Enum):
    """區域類型枚舉"""
    ETCHING_D = "etching_D"
    ETCHING_E = "etching_E"
    LITHO = "litho"
    THIN_FILM = "thin_film"


class DailyReportBase(BaseModel):
    """日報表基礎架構"""
    date: str  # 格式: YYYY-MM-DD
    shift: ShiftType
    area: AreaType
    summary_key_output: Optional[str] = None
    summary_issues: Optional[str] = None
    summary_countermeasures: Optional[str] = None


class DailyReportCreate(DailyReportBase):
    """創建日報表架構"""
    pass


class DailyReportUpdate(BaseModel):
    """更新日報表架構"""
    date: Optional[str] = None
    shift: Optional[ShiftType] = None
    area: Optional[AreaType] = None
    summary_key_output: Optional[str] = None
    summary_issues: Optional[str] = None
    summary_countermeasures: Optional[str] = None


class DailyReportResponse(DailyReportBase):
    """日報表響應架構"""
    id: int
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# 出勤記錄相關架構
class AttendanceCategory(str, Enum):
    """出勤類別枚舉"""
    REGULAR = "Regular"
    CONTRACTOR = "Contractor"


class AttendanceRecordBase(BaseModel):
    """出勤記錄基礎架構"""
    report_id: int
    category: AttendanceCategory
    scheduled_count: int = 0
    present_count: int = 0
    absent_count: int = 0
    reason: Optional[str] = None


class AttendanceRecordCreate(AttendanceRecordBase):
    """創建出勤記錄架構"""
    pass


class AttendanceRecordUpdate(BaseModel):
    """更新出勤記錄架構"""
    category: Optional[AttendanceCategory] = None
    scheduled_count: Optional[int] = None
    present_count: Optional[int] = None
    absent_count: Optional[int] = None
    reason: Optional[str] = None


class AttendanceRecordResponse(AttendanceRecordBase):
    """出勤記錄響應架構"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# 設備異常記錄相關架構
class EquipmentLogBase(BaseModel):
    """設備異常記錄基礎架構"""
    report_id: int
    equip_id: str
    description: str
    start_time: Optional[str] = None  # 格式: HH:MM
    impact_qty: Optional[int] = 0
    action_taken: Optional[str] = None
    image_path: Optional[str] = None


class EquipmentLogCreate(EquipmentLogBase):
    """創建設備異常記錄架構"""
    pass


class EquipmentLogUpdate(BaseModel):
    """更新設備異常記錄架構"""
    equip_id: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    impact_qty: Optional[int] = None
    action_taken: Optional[str] = None
    image_path: Optional[str] = None


class EquipmentLogResponse(EquipmentLogBase):
    """設備異常記錄響應架構"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# 異常批次記錄相關架構
class LotLogBase(BaseModel):
    """異常批次記錄基礎架構"""
    report_id: int
    lot_id: str
    description: str
    status: Optional[str] = None
    notes: Optional[str] = None


class LotLogCreate(LotLogBase):
    """創建異常批次記錄架構"""
    pass


class LotLogUpdate(BaseModel):
    """更新異常批次記錄架構"""
    lot_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class LotLogResponse(LotLogBase):
    """異常批次記錄響應架構"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# 語言相關架構
class LanguageCodeEnum(str, Enum):
    """語言代碼枚舉"""
    JA = "ja"
    ZH = "zh"
    EN = "en"


class LanguageResourceBase(BaseModel):
    """語言資源基礎架構"""
    language_code: LanguageCodeEnum
    resource_key: str = Field(..., max_length=255)
    resource_value: str
    namespace: Optional[str] = "common"


class LanguageResourceCreate(LanguageResourceBase):
    """創建語言資源架構"""
    pass


class LanguageResourceUpdate(BaseModel):
    """更新語言資源架構"""
    resource_value: Optional[str] = None
    namespace: Optional[str] = None


class LanguageResourceResponse(LanguageResourceBase):
    """語言資源響應架構"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class LanguageSettingBase(BaseModel):
    """語言設定基礎架構"""
    user_id: Optional[int] = None
    language_code: LanguageCodeEnum
    is_default: bool = False
    is_active: bool = True


class LanguageSettingUpdate(BaseModel):
    """更新語言設定架構"""
    language_code: Optional[LanguageCodeEnum] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class LanguageSettingResponse(LanguageSettingBase):
    """語言設定響應架構"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True