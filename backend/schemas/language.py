"""
語言相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class LanguageCodeEnum(str, Enum):
    """語言代碼枚舉"""
    JA = "ja"  # 日文
    ZH = "zh"  # 中文
    EN = "en"  # 英文


class LanguageResourceBase(BaseModel):
    """語言資源基礎模型"""
    language_code: LanguageCodeEnum
    resource_key: str = Field(..., max_length=255, description="翻譯鍵")
    resource_value: str = Field(..., description="翻譯值")
    namespace: Optional[str] = Field("common", description="命名空間")


class LanguageResourceCreate(LanguageResourceBase):
    """創建語言資源模型"""
    pass


class LanguageResourceUpdate(BaseModel):
    """更新語言資源模型"""
    resource_value: Optional[str] = Field(None, description="新的翻譯值")
    namespace: Optional[str] = Field(None, description="新的命名空間")


class LanguageResourceResponse(LanguageResourceBase):
    """語言資源響應模型"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class LanguageSettingBase(BaseModel):
    """語言設定基礎模型"""
    user_id: Optional[int] = Field(None, description="用戶ID (NULL表示系統級設定)")
    language_code: LanguageCodeEnum = Field(..., description="語言代碼")
    is_default: bool = Field(False, description="是否為默認語言")
    is_active: bool = Field(True, description="是否啟用")


class LanguageSettingUpdate(BaseModel):
    """更新語言設定模型"""
    language_code: Optional[LanguageCodeEnum] = Field(None, description="新的語言代碼")
    is_default: Optional[bool] = Field(None, description="是否設為默認")
    is_active: Optional[bool] = Field(None, description="是否啟用")


class LanguageSettingResponse(LanguageSettingBase):
    """語言設定響應模型"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True




class LanguageResourcesResponse(BaseModel):
    """語言資源響應模型（批量）"""
    lang: str
    namespace: str = "common"
    resources: dict
    
    class Config:
        from_attributes = True