"""
API 路由配置
"""
from fastapi import APIRouter
from backend.api.v1.endpoints import auth, users, reports, attendance, equipment, lots, languages


# 創建主路由器
api_router = APIRouter()

# 註冊子路由
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(lots.router, prefix="/lots", tags=["lots"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])