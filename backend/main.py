"""
電子交接本系統主應用程式
使用 FastAPI 框架
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1.api import api_router
from backend.core.config import settings


def create_app():
    """創建並配置 FastAPI 應用程式實例"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )

    # 添加 CORS 中介軟體
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 在生產環境中應指定具體域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 包含 API 路由
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        """健康檢查端點"""
        return {"status": "healthy", "service": "handover-system"}

    return app


# 創建應用程式實例
app = create_app()


# 主頁面路由
@app.get("/")
async def root():
    return {"message": "電子交接本系統 API", "version": settings.VERSION}