"""
電子交接本系統主入口點
基於 FastAPI 和 tkinter 的多語言支持系統
"""
import os
import sys
from pathlib import Path

# 添加根目錄到 Python 路徑
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from backend.main import app
from backend.core.config import settings

def main():
    """主執行函數"""
    print("正在啟動電子交接本系統...")
    print(f"數據庫位置: {settings.DATABASE_URL}")
    print("系統初始化完成，正在啟動伺服器...")
    
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )

if __name__ == "__main__":
    main()