"""
電子交接本系統 - 輕量級桌面應用程式
實現多語言支持和同時顯示正社員與契約社員出勤記錄功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
import threading
from pathlib import Path


class LanguageManager:
    """
    語言管理器
    負責管理多語言資源並提供翻譯功能
    """
    
    def __init__(self, locales_dir: str = "frontend/public/locales"):
        self.locales_dir = locales_dir
        self.current_language = "ja"  # 默認為日文
        self.translations = {}

        # 支援的語言
        self.supported_languages = ["ja", "zh", "en"]

        # 加載所有語言資源
        self.load_all_translations()

    def load_all_translations(self):
        """加載所有支援語言的翻譯資源"""
        for lang_code in self.supported_languages:
            self.translations[lang_code] = self.load_language_translations(lang_code)

    def load_language_translations(self, lang_code: str):
        """加載特定語言的翻譯資源"""
        try:
            # 檢查目錄是否存在
            os.makedirs(self.locales_dir, exist_ok=True)
            
            # 檢查語言文件是否存在，如果不存在則創建默認文件
            file_path = os.path.join(self.locales_dir, f"{lang_code}.json")
            if not os.path.exists(file_path):
                self.create_default_language_file(lang_code)
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 找不到語言文件 {file_path}")
            # 返回默認翻譯
            return self.get_default_translations(lang_code)
        except json.JSONDecodeError:
            print(f"錯誤: 語言文件 {file_path} 格式無效")
            return {}

    def create_default_language_file(self, lang_code: str):
        """創建默認語言文件"""
        default_translations = self.get_default_translations(lang_code)
        file_path = os.path.join(self.locales_dir, f"{lang_code}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_translations, f, ensure_ascii=False, indent=2)

    def get_default_translations(self, lang_code: str):
        """獲取默認翻譯資源"""
        defaults = {
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

        return defaults.get(lang_code, {})

    def get_text(self, key: str, default_text: str = ""):
        """
        獲取指定鍵的翻譯文本
        :param key: 翻譯鍵 (例如: "header.title")
        :param default_text: 默認文本
        :return: 翻譯後的文本或默認文本
        """
        try:
            # 分割鍵以支持嵌套結構 (例如: "header.title")
            keys = key.split('.')
            current_dict = self.translations[self.current_language]

            for k in keys:
                current_dict = current_dict.get(k, {})

            if isinstance(current_dict, str):
                return current_dict
            else:
                # 如果找不到確切的鍵，返回默認值或鍵本身
                return default_text or key
        except (TypeError, AttributeError):
            # 如果當前語言中找不到翻譯，則檢查其他語言
            for lang_code in self.supported_languages:
                if lang_code != self.current_language:
                    try:
                        current_dict = self.translations[lang_code]
                        for k in keys:
                            current_dict = current_dict.get(k, {})
                        
                        if isinstance(current_dict, str):
                            return current_dict
                    except (KeyError, TypeError, AttributeError):
                        continue

            # 如果所有語言都沒有找到，返回默認文本或鍵值
            return default_text or key

    def set_language(self, language_code: str):
        """
        設置當前語言
        :param language_code: 語言代碼
        :return: 設置成功與否
        """
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        else:
            print(f"不支援的語言代碼: {language_code}")
            return False

    def get_current_language(self):
        """
        獲取當前語言代碼
        :return: 當前語言代碼
        """
        return self.current_language

    def get_supported_languages(self):
        """
        獲取支援的語言列表
        :return: 支援的語言代碼列表
        """
        return self.supported_languages


class AttendanceSection:
    """
    出勤記錄組件
    同時顯示正社員和契約社員的出勤記錄輸入區域
    """
    
    def __init__(self, parent, lang_manager, callback=None):
        """
        初始化出勤記錄組件
        
        Args:
            parent: 父組件
            lang_manager: 語言管理器實例
            callback: 處理回調函數（如保存操作）
        """
        self.parent = parent
        self.lang_manager = lang_manager
        self.callback = callback
        
        # 創建界面
        self.create_ui()
    
    def create_ui(self):
        """創建界面元素"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="出勤記錄", padding="10")
        
        # 正社員出勤記錄區域
        regular_frame = ttk.LabelFrame(self.frame, text="正社員 (Regular Staff)", padding="5")
        regular_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        regular_frame.columnconfigure(1, weight=1)
        
        # 定員、出勤、欠勤、理由欄位 (正社員)
        ttk.Label(regular_frame, text=f"{self.lang_manager.get_text('common.scheduled', '定員')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.regular_scheduled_var = tk.StringVar(value="0")
        ttk.Entry(regular_frame, textvariable=self.regular_scheduled_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(regular_frame, text=f"{self.lang_manager.get_text('common.present', '出勤')}:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.regular_present_var = tk.StringVar(value="0")
        ttk.Entry(regular_frame, textvariable=self.regular_present_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(regular_frame, text=f"{self.lang_manager.get_text('common.absent', '欠勤')}:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5), pady=2)
        self.regular_absent_var = tk.StringVar(value="0")
        ttk.Entry(regular_frame, textvariable=self.regular_absent_var, width=10).grid(row=0, column=5, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(regular_frame, text=f"{self.lang_manager.get_text('common.reason', '理由')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.regular_reason_var = tk.StringVar()
        ttk.Entry(regular_frame, textvariable=self.regular_reason_var, width=50).grid(row=1, column=1, columnspan=5, sticky=(tk.W, tk.E), pady=2)
        
        # 契約社員出勤記錄區域 - 同時顯示，不使用下拉選單切換
        contractor_frame = ttk.LabelFrame(self.frame, text="契約社員 (Contractor Staff)", padding="5")
        contractor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        contractor_frame.columnconfigure(1, weight=1)
        
        # 定員、出勤、欠勤、理由欄位 (契約社員)
        ttk.Label(contractor_frame, text=f"{self.lang_manager.get_text('common.scheduled', '定員')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.contractor_scheduled_var = tk.StringVar(value="0")
        ttk.Entry(contractor_frame, textvariable=self.contractor_scheduled_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(contractor_frame, text=f"{self.lang_manager.get_text('common.present', '出勤')}:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.contractor_present_var = tk.StringVar(value="0")
        ttk.Entry(contractor_frame, textvariable=self.contractor_present_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(contractor_frame, text=f"{self.lang_manager.get_text('common.absent', '欠勤')}:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5), pady=2)
        self.contractor_absent_var = tk.StringVar(value="0")
        ttk.Entry(contractor_frame, textvariable=self.contractor_absent_var, width=10).grid(row=0, column=5, sticky=tk.W, padx=(0, 15), pady=2)
        
        ttk.Label(contractor_frame, text=f"{self.lang_manager.get_text('common.reason', '理由')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.contractor_reason_var = tk.StringVar()
        ttk.Entry(contractor_frame, textvariable=self.contractor_reason_var, width=50).grid(row=1, column=1, columnspan=5, sticky=(tk.W, tk.E), pady=2)
        
        # 驗證按鈕 - 檢查輸入數據的合理性
        validate_btn = ttk.Button(
            self.frame,
            text="驗證數據",
            command=self.validate_attendance_data
        )
        validate_btn.grid(row=2, column=0, sticky=tk.E, pady=5)
    
    def validate_attendance_data(self):
        """驗證出勤數據的合理性"""
        try:
            # 驗證正社員數據
            regular_scheduled = int(self.regular_scheduled_var.get() or "0")
            regular_present = int(self.regular_present_var.get() or "0")
            regular_absent = int(self.regular_absent_var.get() or "0")
            
            if regular_present + regular_absent > regular_scheduled:
                messagebox.showwarning(
                    "數據不合理",
                    f"正社員出勤人數 ({regular_present}) + 欠勤人數 ({regular_absent}) > 定員人數 ({regular_scheduled})"
                )
                return False
            
            # 驗證契約社員數據
            contractor_scheduled = int(self.contractor_scheduled_var.get() or "0")
            contractor_present = int(self.contractor_present_var.get() or "0")
            contractor_absent = int(self.contractor_absent_var.get() or "0")
            
            if contractor_present + contractor_absent > contractor_scheduled:
                messagebox.showwarning(
                    "數據不合理",
                    f"契約社員出勤人數 ({contractor_present}) + 欠勤人數 ({contractor_absent}) > 定員人數 ({contractor_scheduled})"
                )
                return False
            
            # 如果所有驗證通過
            messagebox.showinfo(
                "驗證成功",
                "所有出勤數據輸入合理。\n" +
                f"正社員: 定員 {regular_scheduled}, 出勤 {regular_present}, 欠勤 {regular_absent}\n" +
                f"契約社員: 定員 {contractor_scheduled}, 出勤 {contractor_present}, 欠勤 {contractor_absent}"
            )
            return True
            
        except ValueError:
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("common.invalidNumbers", "請確保輸入的都是有效數字")
            )
            return False
    
    def get_data(self):
        """獲取當前輸入的數據"""
        return {
            "regular": {
                "scheduled": int(self.regular_scheduled_var.get() or "0"),
                "present": int(self.regular_present_var.get() or "0"),
                "absent": int(self.regular_absent_var.get() or "0"),
                "reason": self.regular_reason_var.get()
            },
            "contractor": {
                "scheduled": int(self.contractor_scheduled_var.get() or "0"),
                "present": int(self.contractor_present_var.get() or "0"),
                "absent": int(self.contractor_absent_var.get() or "0"),
                "reason": self.contractor_reason_var.get()
            }
        }
    
    def get_widget(self):
        """獲取組件主框架"""
        return self.frame


class MainApplication:
    """
    電子交接本系統主應用程式界面
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("電子交接系統")
        self.root.geometry("1200x800")
        
        # 語言管理器
        self.lang_manager = LanguageManager()
        
        # 設置界面
        self.setup_ui()
    
    def setup_ui(self):
        """設置界面元素"""
        # 創建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置窗口大小調整
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # 頂部導航欄
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 標題
        self.title_label = ttk.Label(
            self.top_frame, 
            text=self.lang_manager.get_text("header.title", "電子交接系統"), 
            font=("TkDefaultFont", 16, "bold")
        )
        self.title_label.pack(side=tk.LEFT)
        
        # 語言選擇器
        lang_label = ttk.Label(self.top_frame, text="語言/Language/言語:")
        lang_label.pack(side=tk.RIGHT, padx=(10, 5))
        
        self.lang_var = tk.StringVar()
        self.lang_combo = ttk.Combobox(
            self.top_frame,
            textvariable=self.lang_var,
            values=["日本語", "中文", "English"],
            state="readonly",
            width=10
        )
        self.lang_combo.pack(side=tk.RIGHT)
        
        # 設置當前語言顯示
        lang_map = {"ja": "日本語", "zh": "中文", "en": "English"}
        current_lang_name = lang_map.get(self.lang_manager.get_current_language(), "日本語")
        self.lang_var.set(current_lang_name)
        
        # 綁定語言選擇事件
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 主內容區域 (使用 Notebook 顯示不同頁面)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 創建各個頁面標籤
        self.create_daily_report_tab()
        self.create_attendance_tab()  # 實現正社員和契約社員同時呈現輸入的功能
        self.create_equipment_tab()
        self.create_lot_log_tab()
        self.create_summary_tab()
        
        # 底部狀態欄
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 設置當前狀態
        lang_names = {"ja": "日本語", "zh": "中文", "en": "English"}
        lang_name = lang_names.get(self.lang_manager.get_current_language(), "日本語")
        self.status_var.set(f"就緒 - 當前語言: {lang_name}")
    
    def on_language_change(self, event):
        """處理語言變化事件"""
        lang_map = {"日本語": "ja", "English": "en", "中文": "zh"}
        selected_lang = self.lang_var.get()
        new_lang_code = lang_map.get(selected_lang, "ja")
        
        # 更新語言管理器中的當前語言
        self.lang_manager.set_language(new_lang_code)
        
        # 更新界面語言
        self.update_ui_language()
        
        # 更新狀態欄
        lang_names = {"ja": "日本語", "zh": "中文", "en": "English"}
        lang_name = lang_names.get(self.lang_manager.get_current_language(), "日本語")
        self.status_var.set(f"就緒 - 當前語言: {lang_name}")
    
    def update_ui_language(self):
        """根據當前語言更新界面標示"""
        # 更新標題
        self.title_label.config(text=self.lang_manager.get_text("header.title", "電子交接系統"))
        
        # 更新 Notebook 標籤
        self.notebook.tab(0, text=self.lang_manager.get_text("navigation.reports", "報表"))
        self.notebook.tab(1, text=self.lang_manager.get_text("attendance.records", "出勤記錄"))
        self.notebook.tab(2, text=self.lang_manager.get_text("common.equipment", "設備異常"))
        self.notebook.tab(3, text=self.lang_manager.get_text("common.lots", "異常批次"))
        self.notebook.tab(4, text=self.lang_manager.get_text("common.summary", "總結"))
    
    def create_daily_report_tab(self):
        """創建日報表標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("navigation.reports", "報表"))
        
        # 日期和班別區域
        info_frame = ttk.LabelFrame(tab_frame, text="基本信息", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 日期
        date_frame = ttk.Frame(info_frame)
        date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(date_frame, text=f"{self.lang_manager.get_text('common.date', '日期')}:").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.date_var, width=15).pack(side=tk.LEFT, padx=(10, 20))
        
        # 班別
        ttk.Label(date_frame, text=f"{self.lang_manager.get_text('common.shift', '班別')}:").pack(side=tk.LEFT)
        self.shift_var = tk.StringVar(value="Day")
        shift_combo = ttk.Combobox(
            date_frame,
            textvariable=self.shift_var,
            values=["Day", "Night"],
            state="readonly"
        )
        shift_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        # 區域
        ttk.Label(date_frame, text=f"{self.lang_manager.get_text('common.area', '區域')}:").pack(side=tk.LEFT)
        self.area_var = tk.StringVar(value="etching_D")
        area_combo = ttk.Combobox(
            date_frame,
            textvariable=self.area_var,
            values=["etching_D", "etching_E", "litho", "thin_film"],
            state="readonly"
        )
        area_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # 摘要區域
        summary_frame = ttk.LabelFrame(tab_frame, text="摘要", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Key Machine Output
        ttk.Label(summary_frame, text=self.lang_manager.get_text("summary.keyOutput", "Key Machine Output")).pack(anchor=tk.W)
        self.key_output_text = tk.Text(summary_frame, height=4)
        self.key_output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Key Issues
        ttk.Label(summary_frame, text=self.lang_manager.get_text("summary.issues", "Key Issues")).pack(anchor=tk.W)
        self.issues_text = tk.Text(summary_frame, height=4)
        self.issues_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Countermeasures
        ttk.Label(summary_frame, text=self.lang_manager.get_text("summary.countermeasures", "Countermeasures")).pack(anchor=tk.W)
        self.countermeasures_text = tk.Text(summary_frame, height=4)
        self.countermeasures_text.pack(fill=tk.BOTH, expand=True)
        
        # 保存按鈕
        button_frame = ttk.Frame(tab_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text=self.lang_manager.get_text("common.save", "保存"), command=self.save_daily_report).pack(side=tk.RIGHT)
    
    def create_attendance_tab(self):
        """創建出勤記錄標籤頁 - 同時顯示正社員和契約社員的輸入欄位，不使用下拉式選單區分"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("attendance.records", "出勤記錄"))
        
        # 使用出勤記錄組件 - 同時顯示正社員和契約社員的欄位
        self.attendance_section = AttendanceSection(tab_frame, self.lang_manager)
        self.attendance_section.get_widget().pack(fill=tk.BOTH, expand=True)
        
        # 保存按鈕
        button_frame = ttk.Frame(tab_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text=self.lang_manager.get_text("common.save", "保存"), command=self.save_attendance_record).pack(side=tk.RIGHT)
    
    def create_equipment_tab(self):
        """創建設備異常記錄標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("common.equipment", "設備異常"))
        
        # 輸入區域
        input_frame = ttk.LabelFrame(tab_frame, text="設備異常輸入", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 設備ID和異常內容
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('equipment.equipId', '設備ID')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.equip_id_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('common.description', '異常內容')}:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.equip_desc_var, width=50).grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 發生時刻和影響數量
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('equipment.startTime', '發生時刻')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_start_time_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.equip_start_time_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('equipment.impactQty', '影響數量')}:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_impact_qty_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.equip_impact_qty_var, width=20).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 對應內容
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('equipment.actionTaken', '對應內容')}:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_action_taken_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.equip_action_taken_var, width=80).grid(row=2, column=1, columnspan=3, sticky=tk.W, pady=5)
        
        # 圖片上傳
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('common.image', '圖片')}:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=10)
        self.equip_image_path_var = tk.StringVar()
        image_frame = ttk.Frame(input_frame)
        image_frame.grid(row=3, column=1, columnspan=3, sticky=tk.W, pady=10)
        
        image_entry = ttk.Entry(image_frame, textvariable=self.equip_image_path_var, width=60, state="readonly")
        image_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        browse_btn = ttk.Button(
            image_frame,
            text=self.lang_manager.get_text("common.browse", "瀏覽"),
            command=self.browse_equipment_image
        )
        browse_btn.pack(side=tk.LEFT)
        
        # 添加記錄按鈕
        add_btn = ttk.Button(
            input_frame,
            text=self.lang_manager.get_text("common.add", "添加記錄"),
            command=self.add_equipment_log
        )
        add_btn.grid(row=4, column=3, sticky=tk.E, pady=10)
        
        # 配置列權重
        input_frame.columnconfigure(3, weight=1)
    
    def create_lot_log_tab(self):
        """創建異常批次記錄標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("common.lots", "異常批次"))
        
        # 輸入區域
        input_frame = ttk.LabelFrame(tab_frame, text="異常批次輸入", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 批號和異常內容
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('lot.lotId', '批號')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.lot_id_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('common.description', '異常內容')}:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.lot_desc_var, width=50).grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 處置狀況和特記事項
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('lot.status', '處置狀況')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_status_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.lot_status_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        ttk.Label(input_frame, text=f"{self.lang_manager.get_text('common.notes', '特記事項')}:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_notes_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.lot_notes_var, width=50).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 配置列權重
        input_frame.columnconfigure(3, weight=1)
        
        # 添加記錄按鈕
        add_btn = ttk.Button(
            input_frame,
            text=self.lang_manager.get_text("common.add", "添加記錄"),
            command=self.add_lot_log
        )
        add_btn.grid(row=2, column=3, sticky=tk.E, pady=10)
    
    def create_summary_tab(self):
        """創建總結標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("common.summary", "總結"))
        
        # Key Machine Output
        output_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.keyOutput", "Key Machine Output"), padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.summary_output_text = tk.Text(output_frame, height=4)
        self.summary_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Key Issues
        issues_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.issues", "Key Issues"), padding="5")
        issues_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.summary_issues_text = tk.Text(issues_frame, height=4)
        self.summary_issues_text.pack(fill=tk.BOTH, expand=True)
        
        # Countermeasures
        countermeasures_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.countermeasures", "Countermeasures"), padding="5")
        countermeasures_frame.pack(fill=tk.BOTH, expand=True)
        
        self.summary_countermeasures_text = tk.Text(countermeasures_frame, height=4)
        self.summary_countermeasures_text.pack(fill=tk.BOTH, expand=True)
    
    def save_daily_report(self):
        """保存日報表"""
        try:
            # 這裡會實現保存邏輯到後端 API
            # 目前僅顯示確認對話框
            messagebox.showinfo(
                self.lang_manager.get_text("common.success", "成功"),
                f"報表已保存!\n日期: {self.date_var.get()}\n班別: {self.shift_var.get()}\n區域: {self.area_var.get()}"
            )
        except Exception as e:
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                f"{self.lang_manager.get_text('common.saveFailed', '保存失敗')}: {str(e)}"
            )
    
    def save_attendance_record(self):
        """保存出勤記錄 - 實現正社員和契約社員同時記錄的功能"""
        try:
            # 驗證數據
            attendance_data = self.attendance_section.get_data()
            if not self.attendance_section.validate_attendance_data():
                return  # 數據驗證失敗，不繼續保存
            
            # 在實際實現中，這會調用後端API保存數據
            # 目前僅顯示保存確認對話框
            messagebox.showinfo(
                self.lang_manager.get_text("common.success", "成功"),
                f"出勤記錄已保存!\n" +
                f"{self.lang_manager.get_text('attendance.regular', '正社員')}: 定員 {attendance_data['regular']['scheduled']}, 出勤 {attendance_data['regular']['present']}, 欠勤 {attendance_data['regular']['absent']}\n" +
                f"{self.lang_manager.get_text('attendance.contractor', '契約社員')}: 定員 {attendance_data['contractor']['scheduled']}, 出勤 {attendance_data['contractor']['present']}, 欠勤 {attendance_data['contractor']['absent']}"
            )
        except Exception as e:
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                f"{self.lang_manager.get_text('common.saveFailed', '保存失敗')}: {str(e)}"
            )
    
    def browse_equipment_image(self):
        """瀏覽設備圖片"""
        file_path = filedialog.askopenfilename(
            title=self.lang_manager.get_text("common.selectImage", "選擇圖片"),
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # 在實際實現中，這會上傳文件到服務器，但目前僅顯示文件路徑
            self.equip_image_path_var.set(file_path)
    
    def add_equipment_log(self):
        """添加設備異常記錄"""
        if not self.equip_id_var.get().strip() or not self.equip_desc_var.get().strip():
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("equipment.requireFields", "設備ID和異常內容是必填字段")
            )
            return
        
        # 在實際實現中，這會調用後端API保存數據
        # 目前僅顯示確認對話框
        messagebox.showinfo(
            self.lang_manager.get_text("common.success", "成功"),
            self.lang_manager.get_text("equipment.recordAdded", "設備異常記錄已添加")
        )
    
    def add_lot_log(self):
        """添加異常批次記錄"""
        if not self.lot_id_var.get().strip() or not self.lot_desc_var.get().strip():
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("lot.requireFields", "批號和異常內容是必填字段")
            )
            return
        
        # 在實際實現中，這會調用後端API保存數據
        # 目前僅顯示確認對話框
        messagebox.showinfo(
            self.lang_manager.get_text("common.success", "成功"),
            self.lang_manager.get_text("lot.recordAdded", "異常批次記錄已添加")
        )


def main():
    """主函數"""
    root = tk.Tk()
    app = MainApplication(root)
    
    # 設置窗口關閉事件
    def on_closing():
        if messagebox.askokcancel(
            app.lang_manager.get_text("common.quit", "退出"),
            app.lang_manager.get_text("common.confirmQuit", "確定要退出電子交接系統嗎？")
        ):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()


if __name__ == "__main__":
    main()