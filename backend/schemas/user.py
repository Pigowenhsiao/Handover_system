"""
用戶相關 Pydantic 架構
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """用戶角色枚舉"""
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """用戶基礎模型"""
    username: str = Field(..., min_length=3, max_length=50)
    # 在 Pydantic v2 中，使用 pattern 替代 regex
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[UserRole] = UserRole.USER
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """創建用戶模型"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """更新用戶模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)


class UserInDBBase(UserBase):
    """數據庫用戶基礎模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """用戶響應模型"""
    pass