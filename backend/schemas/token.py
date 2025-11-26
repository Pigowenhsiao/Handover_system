"""
通用 Pydantic 架構
包含身份驗證和基礎響應模型
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """令牌響應模型"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌數據模型"""
    username: Optional[str] = None
    role: Optional[str] = None