"""
電子交接本系統桌面應用程式入口點
整合後端 API 和前端界面
"""
import sys
import os
from pathlib import Path

# 添加根目錄到 Python 路徑
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

import tkinter as tk
from tkinter import messagebox
import threading
import time
import webbrowser
from backend.main import app
from backend.database.init_db import init_db
from backend.core.config import settings


def run_backend():
    """
    在單獨的線程中運行後端服務器
    """
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=False  # 生產環境中禁用重載
    )


def run_frontend():
    """
    運行前端界面
    """
    from frontend.main import MainApplication
    
    root = tk.Tk()
    app_gui = MainApplication(root)
    
    # 設置窗口關閉事件
    def on_closing():
        if messagebox.askokcancel(
            app_gui.lang_manager.get_text("common.quit", "退出"),
            app_gui.lang_manager.get_text("common.confirmQuit", "確定要退出電子交接本系統嗎？")
        ):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 啟動 GUI 主循環
    root.mainloop()


def main():
    """
    主函數 - 啟動完整的電子交接本系統
    """
    print("正在啟動電子交接本系統...")
    print("系統將同時啟動後端 API 服務器和前端界面...")
    
    # 確保上傳目錄存在
    uploads_dir = settings.UPLOADS_DIR
    os.makedirs(uploads_dir, exist_ok=True)
    
    # 初始化數據庫
    try:
        init_db()
        print("數據庫初始化完成")
    except Exception as e:
        print(f"數據庫初始化失敗: {e}")
        messagebox.showerror("錯誤", f"數據庫初始化失敗:\n{e}")
        return
    
    # 啟動後端服務器在單獨線程中
    print(f"正在啟動後端服務器，地址: http://{settings.HOST}:{settings.PORT}")
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # 等待後端服務器啟動
    time.sleep(2)
    
    # 啟動前端界面
    print("正在啟動前端界面...")
    run_frontend()


if __name__ == "__main__":
    main()