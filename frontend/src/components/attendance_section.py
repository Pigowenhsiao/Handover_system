"""
出勤記錄界面組件
實現正社員和契約社員同時呈現輸入的功能
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class AttendanceSection:
    """
    出勤記錄界面組件
    同時顯示正社員和契約社員的出勤記錄輸入區域
    """
    
    def __init__(self, parent, lang_manager, app_instance):
        """
        初始化出勤記錄組件
        
        Args:
            parent: 父組件
            lang_manager: 語言管理器實例
            app_instance: 主應用程式實例（用於回調）
        """
        self.parent = parent
        self.lang_manager = lang_manager
        self.app_instance = app_instance
        
        # 創建界面
        self.setup_ui()
    
    def setup_ui(self):
        """設置界面元素"""
        # 創建主框架
        self.main_frame = ttk.Frame(self.parent, padding="10")
        
        # 正社員出勤記錄區域 (不再使用下拉選單切換)
        regular_frame = ttk.LabelFrame(self.main_frame, text="正社員 (Regular Staff)", padding="10")
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
        
        # 契約社員出勤記錄區域 (不再使用下拉選單切換)
        contractor_frame = ttk.LabelFrame(self.main_frame, text="契約社員 (Contractor Staff)", padding="10")
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
            self.main_frame,
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
                    f"正社員出勤人數({regular_present}) + 欠勤人數({regular_absent}) > 定員人數({regular_scheduled})"
                )
                return False
            
            # 驗證契約社員數據
            contractor_scheduled = int(self.contractor_scheduled_var.get() or "0")
            contractor_present = int(self.contractor_present_var.get() or "0")
            contractor_absent = int(self.contractor_absent_var.get() or "0")
            
            if contractor_present + contractor_absent > contractor_scheduled:
                messagebox.showwarning(
                    "數據不合理",
                    f"契約社員出勤人數({contractor_present}) + 欠勤人數({contractor_absent}) > 定員人數({contractor_scheduled})"
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
            messagebox.showerror("錯誤", "請確保輸入的都是有效數字")
            return False
    
    def get_attendance_data(self):
        """獲取當前出勤數據"""
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
    
    def set_attendance_data(self, data):
        """設置出勤數據"""
        if 'regular' in data:
            regular_data = data['regular']
            self.regular_scheduled_var.set(str(regular_data.get('scheduled', 0)))
            self.regular_present_var.set(str(regular_data.get('present', 0)))
            self.regular_absent_var.set(str(regular_data.get('absent', 0)))
            self.regular_reason_var.set(regular_data.get('reason', ''))
        
        if 'contractor' in data:
            contractor_data = data['contractor']
            self.contractor_scheduled_var.set(str(contractor_data.get('scheduled', 0)))
            self.contractor_present_var.set(str(contractor_data.get('present', 0)))
            self.contractor_absent_var.set(str(contractor_data.get('absent', 0)))
            self.contractor_reason_var.set(contractor_data.get('reason', ''))
    
    def get_widget(self):
        """獲取組件主框架"""
        return self.main_frame