"""
電子交接本系統 - 主入口點
基於 Python tkinter 和 SQLite
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading

# 添加當前目錄到 Python 路徑，以便導入本地模塊
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handover_app import MainApplication


def check_dependencies():
    """檢查依賴項"""
    try:
        import tkinter
        import sqlite3
        import json
        import threading
        from datetime import datetime
        # 檢查 Pillow 依賴（用於圖片處理）
        try:
            import PIL
        except ImportError:
            print("警告: Pillow 模塊未安裝，圖片功能可能不可用")
        return True
    except ImportError as e:
        print(f"缺少依賴: {e}")
        return False


def main():
    """主入口函數"""
    print("正在啟動電子交接本系統...")

    # 檢查依賴項
    if not check_dependencies():
        print("錯誤: 缺少必要的依賴項")
        sys.exit(1)

    # 啟動 GUI 應用程式
    print("正在啟動圖形界面...")
    try:
        root = tk.Tk()

        # 設置窗口關閉事件
        def on_closing():
            try:
                # 如果應用程式對象已存在，詢問是否要退出
                current_widgets = [widget for widget in root.winfo_children()]
                if hasattr(root, '_app_instance') and root._app_instance:
                    if messagebox.askokcancel(
                        root._app_instance.lang_manager.translate("common.quit", "退出"),
                        root._app_instance.lang_manager.translate("common.confirmQuit", "確定要退出電子交接本系統嗎？")
                    ):
                        root.destroy()
                else:
                    if messagebox.askokcancel(
                        "退出",
                        "確定要退出電子交接本系統嗎？"
                    ):
                        root.destroy()
            except tk.TclError:
                # 視窗可能已被銷毀
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # 創建應用程式實例
        app = MainApplication(root)
        root._app_instance = app  # 存儲應用程式實例以便在關閉事件中訪問

        print("應用程式啟動完成，請在圖形界面中操作")
        root.mainloop()

    except Exception as e:
        print(f"GUI 啟動失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()