"""
電子交接本系統 - 主啟動文件
整合前端界面和後端API服務
"""
import sys
import os
import threading
import subprocess
import time
from pathlib import Path

# 添加項目根目錄到系統路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_backend():
    """
    運行後端 FastAPI 服務
    """
    import uvicorn
    from backend.main import app
    from backend.core.config import settings
    
    print(f"正在啟動後端服務器，監聽 {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=False  # 生產環境中應禁用重載
    )


def run_frontend():
    """
    運行前端界面
    """
    import tkinter as tk
    from frontend.main import MainApplication
    
    root = tk.Tk()
    app = MainApplication(root)
    
    def on_closing():
        """窗口關閉事件處理"""
        if tk.messagebox.askokcancel("退出", "確定要退出電子交接系統嗎？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def main():
    """
    主函數 - 啟動完整系統
    """
    print("電子交接本系統啟動中...")
    print("="*50)
    
    # 檢查並創建必要的目錄
    required_dirs = [
        "uploads",
        "uploads/equipment_images",
        "frontend/public/locales",
        "backend/database"
    ]
    
    for dir_path in required_dirs:
        full_path = os.path.join(project_root, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"✓ 確保目錄存在: {dir_path}")
    
    # 初始化數據庫
    print("\n初始化數據庫...")
    try:
        from backend.database.init_db import init_db
        init_db()
        print("✓ 數據庫初始化完成")
    except Exception as e:
        print(f"✗ 數據庫初始化失敗: {e}")
        return
    
    # 檢查語言資源文件是否存在，如果不存在則創建
    print("\n檢查語言資源文件...")
    locales_dir = os.path.join(project_root, "frontend", "public", "locales")
    lang_files = ["ja.json", "zh.json", "en.json"]
    
    for lang_file in lang_files:
        file_path = os.path.join(locales_dir, lang_file)
        if not os.path.exists(file_path):
            print(f"創建語言文件: {lang_file}")
            
            # 語言資源內容
            default_translations = {
                "ja": {
                    "header": {
                        "title": "電子交接系統",
                        "languageSwitch": "言語切替",
                        "login": "ログイン",
                        "logout": "ログアウト"
                    },
                    "navigation": {
                        "home": "ホーム",
                        "reports": "レポート",
                        "settings": "設定",
                        "admin": "管理"
                    },
                    "common": {
                        "date": "日付",
                        "shift": "シフト",
                        "area": "区域",
                        "save": "保存",
                        "cancel": "キャンセル",
                        "create": "作成",
                        "update": "更新",
                        "delete": "削除",
                        "search": "検索",
                        "edit": "編集",
                        "confirm": "確認",
                        "yes": "はい",
                        "no": "いいえ",
                        "loading": "読み込み中...",
                        "error": "エラー",
                        "success": "成功",
                        "scheduled": "定員",
                        "present": "出勤",
                        "absent": "欠勤",
                        "reason": "理由",
                        "regular": "正社員",
                        "contractor": "契約社員"
                    },
                    "attendance": {
                        "regular": "正社員",
                        "contractor": "契約社員",
                        "input": "出勤入力",
                        "records": "出勤記録"
                    },
                    "equipment": {
                        "equipId": "設備ID",
                        "startTime": "発生時刻",
                        "description": "異常内容",
                        "impactQty": "影響数量",
                        "actionTaken": "対応内容",
                        "image": "画像"
                    },
                    "lot": {
                        "lotId": "ロットNO",
                        "status": "処置状況",
                        "notes": "特記事項"
                    },
                    "summary": {
                        "keyOutput": "Key Machine Output",
                        "issues": "Key Issues",
                        "countermeasures": "Countermeasures"
                    }
                },
                "zh": {
                    "header": {
                        "title": "電子交接系統",
                        "languageSwitch": "語言切換",
                        "login": "登入",
                        "logout": "登出"
                    },
                    "navigation": {
                        "home": "首頁",
                        "reports": "報表",
                        "settings": "設定",
                        "admin": "管理"
                    },
                    "common": {
                        "date": "日期",
                        "shift": "班別",
                        "area": "區域",
                        "save": "保存",
                        "cancel": "取消",
                        "create": "新增",
                        "update": "更新",
                        "delete": "刪除",
                        "search": "搜尋",
                        "edit": "編輯",
                        "confirm": "確認",
                        "yes": "是",
                        "no": "否",
                        "loading": "載入中...",
                        "error": "錯誤",
                        "success": "成功",
                        "scheduled": "定員",
                        "present": "出勤",
                        "absent": "欠勤",
                        "reason": "理由",
                        "regular": "正社員",
                        "contractor": "契約社員"
                    },
                    "attendance": {
                        "regular": "正社員",
                        "contractor": "契約社員",
                        "input": "出勤輸入",
                        "records": "出勤記錄"
                    },
                    "equipment": {
                        "equipId": "設備ID",
                        "startTime": "發生時刻",
                        "description": "異常內容",
                        "impactQty": "影響數量",
                        "actionTaken": "對應內容",
                        "image": "圖片"
                    },
                    "lot": {
                        "lotId": "批號",
                        "status": "處置狀況",
                        "notes": "特記事項"
                    },
                    "summary": {
                        "keyOutput": "Key Machine Output",
                        "issues": "Key Issues",
                        "countermeasures": "Countermeasures"
                    }
                },
                "en": {
                    "header": {
                        "title": "Digital Handover System",
                        "languageSwitch": "Language Switch",
                        "login": "Login",
                        "logout": "Logout"
                    },
                    "navigation": {
                        "home": "Home",
                        "reports": "Reports",
                        "settings": "Settings",
                        "admin": "Admin"
                    },
                    "common": {
                        "date": "Date",
                        "shift": "Shift",
                        "area": "Area",
                        "save": "Save",
                        "cancel": "Cancel",
                        "create": "Create",
                        "update": "Update",
                        "delete": "Delete",
                        "search": "Search",
                        "edit": "Edit",
                        "confirm": "Confirm",
                        "yes": "Yes",
                        "no": "No",
                        "loading": "Loading...",
                        "error": "Error",
                        "success": "Success",
                        "scheduled": "Scheduled",
                        "present": "Present",
                        "absent": "Absent",
                        "reason": "Reason",
                        "regular": "Regular Staff",
                        "contractor": "Contractor Staff"
                    },
                    "attendance": {
                        "regular": "Regular",
                        "contractor": "Contractor",
                        "input": "Attendance Input",
                        "records": "Attendance Records"
                    },
                    "equipment": {
                        "equipId": "Equipment ID",
                        "startTime": "Start Time",
                        "description": "Description",
                        "impactQty": "Impact Qty",
                        "actionTaken": "Action Taken",
                        "image": "Image"
                    },
                    "lot": {
                        "lotId": "Lot ID",
                        "status": "Status",
                        "notes": "Notes"
                    },
                    "summary": {
                        "keyOutput": "Key Machine Output",
                        "issues": "Key Issues",
                        "countermeasures": "Countermeasures"
                    }
                }
            }
            
            lang_code = lang_file.split('.')[0]
            translations = default_translations.get(lang_code, default_translations["ja"])
            
            with open(file_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print("✓ 語言資源文件檢查完成")
    
    print("\n電子交接本系統已準備就緒")
    print("前端界面將在獨立窗口中啟動")
    print("後端 API 服務器將在 http://localhost:8000 運行")
    print("="*50)
    
    # 啟動前端界面 (主要界面，使用tkinter)
    print("啟動前端界面...")
    run_frontend()


if __name__ == "__main__":
    main()