"""
電子交接本系統 - 主應用程式
基於 Python、SQLite 和 tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("警告: Pillow 模組未安裝，圖片功能將不可用")
import threading

from language_manager import AppLanguageManager


class DatabaseManager:
    """數據庫管理器"""
    
    def __init__(self, db_path="handover_system.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化數據庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 創建用戶表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 創建日報表表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                shift TEXT NOT NULL,
                area TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary_key_output TEXT,
                summary_issues TEXT,
                summary_countermeasures TEXT,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        """)
        
        # 創建出勤記錄表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                scheduled_count INTEGER DEFAULT 0,
                present_count INTEGER DEFAULT 0,
                absent_count INTEGER DEFAULT 0,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES daily_reports (id) ON DELETE CASCADE
            )
        """)
        
        # 創建設備異常記錄表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                equip_id TEXT NOT NULL,
                description TEXT NOT NULL,
                start_time TEXT,
                impact_qty INTEGER DEFAULT 0,
                action_taken TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES daily_reports (id) ON DELETE CASCADE
            )
        """)
        
        # 創建異常批次記錄表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lot_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                lot_id TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES daily_reports (id) ON DELETE CASCADE
            )
        """)
        
        # 添加默認管理員用戶（如果不存在）
        # 先檢查是否存在管理員用戶
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'Admin'")
        count = cursor.fetchone()[0]

        if count == 0:
            # 對於示範目的，我們創建一個簡單的密碼哈希，實際應用中應使用更強的密碼哈希
            import hashlib
            default_password_hash = hashlib.sha256('1234'.encode()).hexdigest()

            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES ('Admin', ?, 'admin')
            """, (default_password_hash,))

        conn.commit()
        conn.close()


class UserManager:
    """用戶管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.current_user = None
    
    def authenticate(self, username: str, password: str) -> bool:
        """用戶認證"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, role FROM users 
            WHERE username = ? AND password_hash = ?
        """, (username, self.hash_password(password)))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.current_user = {
                'id': result[0],
                'username': result[1],
                'role': result[2]
            }
            return True
        return False
    
    def hash_password(self, password: str) -> str:
        """簡單的密碼哈希（在實際應用中應使用更強大的哈希算法）"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def is_admin(self) -> bool:
        """檢查當前用戶是否為管理員"""
        return self.current_user and self.current_user['role'] == 'admin'

    def add_user(self, username: str, password: str, role: str = 'user') -> bool:
        """添加新用戶"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()

        try:
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 用戶名已存在
            return False
        finally:
            conn.close()

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """更改用戶密碼"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()

        # 首先驗證舊密碼
        cursor.execute("""
            SELECT password_hash FROM users WHERE username = ?
        """, (username,))

        result = cursor.fetchone()

        if result:
            stored_hash = result[0]
            old_hash = self.hash_password(old_password)

            if stored_hash == old_hash:
                # 舊密碼正確，更新為新密碼
                new_hash = self.hash_password(new_password)
                cursor.execute("""
                    UPDATE users SET password_hash = ? WHERE username = ?
                """, (new_hash, username))

                conn.commit()
                conn.close()
                return True

        conn.close()
        return False


class DailyReportManager:
    """日報表管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_report(self, date: str, shift: str, area: str, author_id: int, 
                     summary_key_output: str, summary_issues: str, summary_countermeasures: str) -> int:
        """創建新的日報表"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO daily_reports 
            (date, shift, area, author_id, summary_key_output, summary_issues, summary_countermeasures)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date, shift, area, author_id, summary_key_output, summary_issues, summary_countermeasures))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    def update_report(self, report_id: int, date: str, shift: str, area: str,
                     summary_key_output: str, summary_issues: str, summary_countermeasures: str) -> bool:
        """更新日報表"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE daily_reports 
            SET date=?, shift=?, area=?, summary_key_output=?, summary_issues=?, summary_countermeasures=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (date, shift, area, summary_key_output, summary_issues, summary_countermeasures, report_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_report(self, report_id: int) -> bool:
        """刪除日報表"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM daily_reports WHERE id=?", (report_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """獲取單個日報表"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, date, shift, area, author_id, summary_key_output, summary_issues, summary_countermeasures, created_at, updated_at
            FROM daily_reports WHERE id=?
        """, (report_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        return {
            'id': result[0],
            'date': result[1],
            'shift': result[2],
            'area': result[3],
            'author_id': result[4],
            'summary_key_output': result[5],
            'summary_issues': result[6],
            'summary_countermeasures': result[7],
            'created_at': result[8],
            'updated_at': result[9]
        }
    
    def search_reports(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                      area: Optional[str] = None, author_id: Optional[int] = None) -> List[Dict]:
        """搜索日報表"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT r.id, r.date, r.shift, r.area, u.username, r.summary_key_output, 
                   r.summary_issues, r.summary_countermeasures, r.created_at
            FROM daily_reports r
            JOIN users u ON r.author_id = u.id
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND r.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND r.date <= ?"
            params.append(end_date)
        
        if area:
            query += " AND r.area = ?"
            params.append(area)
        
        if author_id:
            query += " AND r.author_id = ?"
            params.append(author_id)
        
        query += " ORDER BY r.date DESC, r.created_at DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        reports = []
        for result in results:
            reports.append({
                'id': result[0],
                'date': result[1],
                'shift': result[2],
                'area': result[3],
                'author_username': result[4],
                'summary_key_output': result[5][:50] + "..." if result[5] and len(result[5]) > 50 else result[5],  # 截斷長文本
                'summary_issues': result[6][:50] + "..." if result[6] and len(result[6]) > 50 else result[6],
                'summary_countermeasures': result[7][:50] + "..." if result[7] and len(result[7]) > 50 else result[7],
                'created_at': result[8]
            })
        
        return reports


class AttendanceManager:
    """出勤管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def add_attendance_record(self, report_id: int, category: str, scheduled: int, present: int, absent: int, reason: str = ""):
        """添加出勤記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO attendance_records 
            (report_id, category, scheduled_count, present_count, absent_count, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (report_id, category, scheduled, present, absent, reason))
        
        conn.commit()
        conn.close()
    
    def get_attendance_records(self, report_id: int) -> List[Dict]:
        """獲取指定報表的出勤記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, category, scheduled_count, present_count, absent_count, reason, created_at
            FROM attendance_records WHERE report_id=?
        """, (report_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        records = []
        for result in results:
            records.append({
                'id': result[0],
                'category': result[1],
                'scheduled_count': result[2],
                'present_count': result[3],
                'absent_count': result[4],
                'reason': result[5],
                'created_at': result[6]
            })
        
        return records
    
    def update_attendance_record(self, record_id: int, scheduled: int, present: int, absent: int, reason: str = ""):
        """更新出勤記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE attendance_records 
            SET scheduled_count=?, present_count=?, absent_count=?, reason=?, created_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (scheduled, present, absent, reason, record_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_attendance_record(self, record_id: int) -> bool:
        """刪除出勤記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM attendance_records WHERE id=?", (record_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success


class EquipmentManager:
    """設備異常管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def add_equipment_log(self, report_id: int, equip_id: str, description: str, 
                         start_time: str = "", impact_qty: int = 0, action_taken: str = "", image_path: str = ""):
        """添加設備異常記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO equipment_logs 
            (report_id, equip_id, description, start_time, impact_qty, action_taken, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (report_id, equip_id, description, start_time, impact_qty, action_taken, image_path))
        
        conn.commit()
        conn.close()
    
    def get_equipment_logs(self, report_id: int) -> List[Dict]:
        """獲取指定報表的設備異常記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, equip_id, description, start_time, impact_qty, action_taken, image_path, created_at
            FROM equipment_logs WHERE report_id=?
        """, (report_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        logs = []
        for result in results:
            logs.append({
                'id': result[0],
                'equip_id': result[1],
                'description': result[2],
                'start_time': result[3],
                'impact_qty': result[4],
                'action_taken': result[5],
                'image_path': result[6],
                'created_at': result[7]
            })
        
        return logs
    
    def update_equipment_log(self, log_id: int, description: str, start_time: str = "", 
                           impact_qty: int = 0, action_taken: str = "", image_path: str = ""):
        """更新設備異常記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE equipment_logs 
            SET description=?, start_time=?, impact_qty=?, action_taken=?, image_path=?, created_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (description, start_time, impact_qty, action_taken, image_path, log_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_equipment_log(self, log_id: int) -> bool:
        """刪除設備異常記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM equipment_logs WHERE id=?", (log_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success


class LotManager:
    """異常批次管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def add_lot_log(self, report_id: int, lot_id: str, description: str, status: str = "", notes: str = ""):
        """添加異常批次記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO lot_logs 
            (report_id, lot_id, description, status, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (report_id, lot_id, description, status, notes))
        
        conn.commit()
        conn.close()
    
    def get_lot_logs(self, report_id: int) -> List[Dict]:
        """獲取指定報表的異常批次記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, lot_id, description, status, notes, created_at
            FROM lot_logs WHERE report_id=?
        """, (report_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        logs = []
        for result in results:
            logs.append({
                'id': result[0],
                'lot_id': result[1],
                'description': result[2],
                'status': result[3],
                'notes': result[4],
                'created_at': result[5]
            })
        
        return logs
    
    def update_lot_log(self, log_id: int, description: str, status: str = "", notes: str = ""):
        """更新異常批次記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE lot_logs 
            SET description=?, status=?, notes=?, created_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (description, status, notes, log_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_lot_log(self, log_id: int) -> bool:
        """刪除異常批次記錄"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM lot_logs WHERE id=?", (log_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success


class LoginWindow:
    """登入窗口"""
    
    def __init__(self, parent, lang_manager, user_manager):
        self.parent = parent
        self.lang_manager = lang_manager
        self.user_manager = user_manager
        self.window = tk.Toplevel(parent)
        
        self.window.title("Login")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """設置界面"""
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 標題
        ttk.Label(main_frame, text=self.lang_manager.translate("common.login", "登入"), 
                 font=("TkDefaultFont", 16, "bold")).pack(pady=(0, 20))
        
        # 用戶名
        ttk.Label(main_frame, text=self.lang_manager.translate("common.username", "用戶名")).pack(anchor=tk.W)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        self.username_entry.pack(pady=(0, 10))
        
        # 密碼
        ttk.Label(main_frame, text=self.lang_manager.translate("common.password", "密碼")).pack(anchor=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=30, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        # 按鈕框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        # 登入按鈕
        self.login_btn = ttk.Button(button_frame, text=self.lang_manager.translate("common.login", "登入"), 
                                   command=self.login)
        self.login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 取消按鈕
        ttk.Button(button_frame, text=self.lang_manager.translate("common.cancel", "取消"), 
                  command=self.window.destroy).pack(side=tk.LEFT)
        
        # 綁定回車鍵
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # 聚焦到用戶名欄位
        self.username_entry.focus()
    
    def login(self):
        """執行登入操作"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.pleaseFillCredentials", "請填寫用戶名和密碼")
            )
            return
        
        if self.user_manager.authenticate(username, password):
            messagebox.showinfo(
                self.lang_manager.translate("common.success", "成功"),
                self.lang_manager.translate("common.loginSuccess", "登入成功")
            )
            self.window.destroy()
        else:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.invalidCredentials", "用戶名或密碼錯誤")
            )


class MainApplication:
    """主應用程式"""

    def __init__(self, root):
        self.root = root
        self.root.title("電子交接本系統")
        self.root.geometry("1200x800")

        # 初始化語言管理器
        self.lang_manager = AppLanguageManager()

        # 初始化數據庫和管理器
        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.daily_report_manager = DailyReportManager(self.db_manager)
        self.attendance_manager = AttendanceManager(self.db_manager)
        self.equipment_manager = EquipmentManager(self.db_manager)
        self.lot_manager = LotManager(self.db_manager)

        # 創建圖片存儲目錄
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        # 登入窗口
        self.login_window = None

        # 懟前頁面跟蹤
        self.current_page = None
        self.current_report_id = None

        # 設置界面
        self.setup_ui()

        # 顯示登入窗口
        self.show_login()

    def destroy(self):
        """清理資源"""
        if self.login_window:
            try:
                self.login_window.window.destroy()
            except tk.TclError:
                pass  # 視窗可能已被銷毀
    
    def setup_ui(self):
        """設置用戶界面"""
        # 創建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # 頂導欄
        self.navbar_frame = ttk.Frame(self.main_frame)
        self.navbar_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 語言切換
        self.lang_var = tk.StringVar()
        ttk.Label(self.navbar_frame, text="Language:").pack(side=tk.LEFT, padx=(0, 5))
        self.lang_combo = ttk.Combobox(
            self.navbar_frame, 
            textvariable=self.lang_var, 
            values=["ja", "en", "zh"],
            state="readonly",
            width=10
        )
        self.lang_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 頁面導航按鈕
        self.nav_buttons_frame = ttk.Frame(self.navbar_frame)
        self.nav_buttons_frame.pack(side=tk.LEFT)
        
        # 頁表按鈕
        self.home_btn = ttk.Button(
            self.nav_buttons_frame,
            text=self.lang_manager.translate("navigation.home", "首頁"),
            command=self.show_home
        )
        self.home_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 報表按鈕
        self.reports_btn = ttk.Button(
            self.nav_buttons_frame,
            text=self.lang_manager.translate("navigation.reports", "報表"),
            command=self.show_reports
        )
        self.reports_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 填寫日報按鈕
        self.fill_btn = ttk.Button(
            self.nav_buttons_frame,
            text=self.lang_manager.translate("common.fillReport", "填寫日報"),
            command=self.show_fill_report
        )
        self.fill_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 登出按鈕
        self.logout_btn = ttk.Button(
            self.navbar_frame,
            text=self.lang_manager.translate("header.logout", "登出"),
            command=self.logout
        )
        self.logout_btn.pack(side=tk.RIGHT)
        
        # 標題
        self.title_label = ttk.Label(self.main_frame, text="", font=("TkDefaultFont", 16, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # 主內容框架
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # 狀態欄
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def show_login(self):
        """顯示登入窗口"""
        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = LoginWindow(self.root, self.lang_manager, self.user_manager)
            self.login_window.window.transient(self.root)
            self.login_window.window.grab_set()
            
            # 等待登入窗口關閉
            self.root.wait_window(self.login_window.window)
            
            if self.user_manager.current_user:
                # 登入成功，顯示主页
                self.update_navbar_visibility()
                self.show_home()
            else:
                # 登入失敗或取消，退出應用
                self.root.destroy()
    
    def update_navbar_visibility(self):
        """更新導航欄可見性"""
        logged_in = self.user_manager.current_user is not None
        buttons = [self.home_btn, self.reports_btn, self.fill_btn, self.logout_btn]
        
        for btn in buttons:
            if logged_in:
                btn.pack_configure(side=tk.LEFT if btn != self.logout_btn else tk.RIGHT, padx=(0, 5))
            else:
                btn.pack_forget()
    
    def on_language_change(self, event=None):
        """語言變化事件"""
        new_lang = self.lang_var.get()
        if new_lang and self.lang_manager.change_language(new_lang):
            self.update_language_ui()
    
    def update_language_ui(self):
        """更新界面語言"""
        lang_code = self.lang_manager.get_current_language()
        self.lang_var.set(lang_code)
        
        # 更新導航按鈕文本
        self.home_btn.config(text=self.lang_manager.translate("navigation.home", "首頁"))
        self.reports_btn.config(text=self.lang_manager.translate("navigation.reports", "報表"))
        self.fill_btn.config(text=self.lang_manager.translate("common.fillReport", "填寫日報"))
        self.logout_btn.config(text=self.lang_manager.translate("header.logout", "登出"))
        
        # 更新狀態欄
        lang_names = {"ja": "日本語", "en": "English", "zh": "中文"}
        current_lang_name = lang_names.get(lang_code, lang_code)
        if self.user_manager.current_user:
            self.status_var.set(
                f"{self.lang_manager.translate('common.currentUser', '當前用戶')}: {self.user_manager.current_user['username']} | "
                f"{self.lang_manager.translate('common.currentLanguage', '當前語言')}: {current_lang_name}"
            )
        else:
            self.status_var.set(f"{self.lang_manager.translate('common.currentLanguage', '當前語言')}: {current_lang_name}")
        
        # 重新顯示當前頁面（以更新語言）
        if self.current_page == "home":
            self.show_home()
        elif self.current_page == "reports":
            self.show_reports()
        elif self.current_page == "fill_report":
            self.show_fill_report()
    
    def show_home(self):
        """顯示主页"""
        self.clear_content_frame()
        self.current_page = "home"
        
        # 更新標題
        self.title_label.config(text=self.lang_manager.translate("header.title", "電子交接系統"))
        
        # 主頁內容
        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)
        
        # 歡迎信息
        welcome_frame = ttk.LabelFrame(content, text=self.lang_manager.translate("common.welcome", "歡迎"), padding="20")
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            welcome_frame,
            text=self.lang_manager.translate("common.welcomeMessage", "歡迎使用電子交接本系統"),
            font=("TkDefaultFont", 14)
        ).pack()
        
        # 功能簡介
        features_frame = ttk.LabelFrame(content, text=self.lang_manager.translate("common.features", "系統功能"), padding="20")
        features_frame.pack(fill=tk.BOTH, expand=True)
        
        features = [
            self.lang_manager.translate("common.feature1", "填寫當日工作報表"),
            self.lang_manager.translate("common.feature2", "記錄設備異常狀況"),
            self.lang_manager.translate("common.feature3", "追蹤異常批次"),
            self.lang_manager.translate("common.feature4", "查看歷史報表"),
            self.lang_manager.translate("common.feature5", "多語言支持 (日文/英文/中文)")
        ]
        
        for i, feature in enumerate(features):
            ttk.Label(features_frame, text=f"• {feature}").pack(anchor=tk.W, pady=2)
    
    def show_reports(self):
        """顯示報表頁面"""
        self.clear_content_frame()
        self.current_page = "reports"
        
        # 更新標題
        self.title_label.config(text=self.lang_manager.translate("navigation.reports", "報表"))
        
        # 報表頁面內容
        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)
        
        # 搜索框架
        search_frame = ttk.LabelFrame(content, text=self.lang_manager.translate("common.search", "搜索"), padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 搜索欄
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X)
        
        # 日期範圍
        ttk.Label(search_row, text=self.lang_manager.translate("common.startDate", "開始日期")).pack(side=tk.LEFT, padx=(0, 5))
        self.start_date_var = tk.StringVar()
        start_date_entry = ttk.Entry(search_row, textvariable=self.start_date_var, width=12)
        start_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(search_row, text=self.lang_manager.translate("common.endDate", "結束日期")).pack(side=tk.LEFT, padx=(0, 5))
        self.end_date_var = tk.StringVar()
        end_date_entry = ttk.Entry(search_row, textvariable=self.end_date_var, width=12)
        end_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # 區域過濾
        ttk.Label(search_row, text=self.lang_manager.translate("common.area", "區域")).pack(side=tk.LEFT, padx=(20, 5))
        self.area_var = tk.StringVar()
        area_combo = ttk.Combobox(
            search_row, 
            textvariable=self.area_var, 
            values=["", "etching_D", "etching_E", "litho", "thin_film"],
            state="readonly",
            width=15
        )
        area_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 搜索按鈕
        search_btn = ttk.Button(search_row, text=self.lang_manager.translate("common.search", "搜索"), command=self.search_reports)
        search_btn.pack(side=tk.RIGHT)
        
        # 重置按鈕
        reset_btn = ttk.Button(search_row, text=self.lang_manager.translate("common.reset", "重置"), command=self.reset_report_filters)
        reset_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 報表表格
        table_frame = ttk.Frame(content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 創建表格
        columns = (
            'ID', 
            'Date', 
            'Shift', 
            'Area', 
            'Author', 
            'Key Output', 
            'Issues', 
            'Countermeasures',
            'Created At'
        )
        self.reports_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # 定義表頭
        headers = [
            'ID',
            self.lang_manager.translate("common.date", "日期"),
            self.lang_manager.translate("common.shift", "班別"),
            self.lang_manager.translate("common.area", "區域"),
            self.lang_manager.translate("common.author", "填寫者"),
            self.lang_manager.translate("common.keyOutput", "Key Output"),
            self.lang_manager.translate("common.issues", "Issues"),
            self.lang_manager.translate("common.countermeasures", "Countermeasures"),
            self.lang_manager.translate("common.createdAt", "創建時間")
        ]
        
        for col, header in zip(columns, headers):
            self.reports_tree.heading(col, text=header)
            self.reports_tree.column(col, width=100)
        
        # 設置最後一列自動填充剩餘空間
        self.reports_tree.column('Key Output', width=150)
        self.reports_tree.column('Issues', width=150)
        self.reports_tree.column('Countermeasures', width=150)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定雙擊事件以查看詳細信息
        self.reports_tree.bind('<Double-1>', self.view_report_details)
        
        # 初始加載報表
        self.load_reports()
    
    def clear_content_frame(self):
        """清除內容框架"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def search_reports(self):
        """搜索報表"""
        start_date = self.start_date_var.get() if self.start_date_var.get().strip() else None
        end_date = self.end_date_var.get() if self.end_date_var.get().strip() else None
        area = self.area_var.get() if self.area_var.get() != "" else None
        
        # 顯示搜索結果
        self.load_reports(start_date, end_date, area)
    
    def reset_report_filters(self):
        """重置報表搜索過濾器"""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.area_var.set("")
        self.load_reports()
    
    def load_reports(self, start_date=None, end_date=None, area=None):
        """載入報表"""
        # 清除現有項目
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        # 獲取報表
        reports = self.daily_report_manager.search_reports(start_date, end_date, area)
        
        # 添加到表格
        for report in reports:
            self.reports_tree.insert('', tk.END, values=(
                report['id'],
                report['date'],
                report['shift'],
                report['area'],
                report['author_username'],
                report['summary_key_output'] or "",
                report['summary_issues'] or "",
                report['summary_countermeasures'] or "",
                report['created_at']
            ))
    
    def view_report_details(self, event):
        """查看報表詳細信息"""
        selection = self.reports_tree.selection()
        if selection:
            item = self.reports_tree.item(selection[0])
            report_id = item['values'][0]  # ID 是第一列
            
            # 顯示報表詳細信息
            self.show_report_details(report_id)
    
    def show_report_details(self, report_id: int):
        """顯示報表詳細信息"""
        report = self.daily_report_manager.get_report(report_id)
        if not report:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.reportNotFound", "報表未找到")
            )
            return
        
        # 創建新窗口顯示詳細信息
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{self.lang_manager.translate('common.reportDetail', '報表詳細')} - #{report_id}")
        details_window.geometry("800x700")
        
        # 主框架
        main_frame = ttk.Frame(details_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 基本信息框架
        basic_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.basicInfo", "基本信息"), padding="10")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 填充基本信息
        basic_info = [
            (self.lang_manager.translate("common.date", "日期"), report['date']),
            (self.lang_manager.translate("common.shift", "班別"), report['shift']),
            (self.lang_manager.translate("common.area", "區域"), report['area']),
            (self.lang_manager.translate("common.author", "填寫者"), self.get_username_by_id(report['author_id'])),
            (self.lang_manager.translate("common.createdAt", "創建時間"), report['created_at']),
            (self.lang_manager.translate("common.updatedAt", "更新時間"), report['updated_at'] or "")
        ]
        
        for i, (label, value) in enumerate(basic_info):
            row_frame = ttk.Frame(basic_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"{label}:", width=15, anchor=tk.W).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=str(value), anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # 總結信息
        summary_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.summary", "總結"), padding="10")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        summary_labels = [
            (self.lang_manager.translate("common.keyOutput", "Key Output"), report['summary_key_output']),
            (self.lang_manager.translate("common.issues", "Key Issues"), report['summary_issues']),
            (self.lang_manager.translate("common.countermeasures", "Countermeasures"), report['summary_countermeasures'])
        ]
        
        for label, value in summary_labels:
            if value:  # 只有在有值時才顯示
                row_frame = ttk.Frame(summary_frame)
                row_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(row_frame, text=f"{label}:", width=15, anchor=tk.NW).pack(side=tk.LEFT)
                ttk.Label(row_frame, text=str(value), anchor=tk.NW, wraplength=600).pack(side=tk.LEFT, padx=(10, 0))
        
        # 出勤記錄
        attendance_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.attendance", "出勤記錄"), padding="10")
        attendance_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        attendance_records = self.attendance_manager.get_attendance_records(report_id)
        
        if attendance_records:
            attendance_columns = ("Category", "Scheduled", "Present", "Absent", "Reason", "Created At")
            attendance_tree = ttk.Treeview(attendance_frame, columns=attendance_columns, show='headings', height=5)
            
            attendance_headers = [
                self.lang_manager.translate("common.category", "類別"),
                self.lang_manager.translate("common.scheduled", "定員"),
                self.lang_manager.translate("common.present", "出勤"),
                self.lang_manager.translate("common.absent", "欠勤"),
                self.lang_manager.translate("common.reason", "理由"),
                self.lang_manager.translate("common.createdAt", "創建時間")
            ]
            
            for col, header in zip(attendance_columns, attendance_headers):
                attendance_tree.heading(col, text=header)
                attendance_tree.column(col, width=100)
            
            attendance_tree.column("Reason", width=200)
            
            for record in attendance_records:
                attendance_tree.insert('', tk.END, values=(
                    record['category'],
                    record['scheduled_count'],
                    record['present_count'],
                    record['absent_count'],
                    record['reason'] or "",
                    record['created_at']
                ))
            
            attendance_scrollbar = ttk.Scrollbar(attendance_frame, orient=tk.VERTICAL, command=attendance_tree.yview)
            attendance_tree.configure(yscrollcommand=attendance_scrollbar.set)
            
            attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            attendance_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            ttk.Label(attendance_frame, text=self.lang_manager.translate("common.noRecords", "無記錄")).pack()
        
        # 設備異常記錄
        equipment_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.equipment", "設備異常"), padding="10")
        equipment_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        equipment_logs = self.equipment_manager.get_equipment_logs(report_id)
        
        if equipment_logs:
            equipment_columns = ("ID", "Equipment ID", "Description", "Start Time", "Impact Qty", "Action Taken", "Image", "Created At")
            equipment_tree = ttk.Treeview(equipment_frame, columns=equipment_columns, show='headings', height=5)
            
            equipment_headers = [
                "ID",
                self.lang_manager.translate("common.equipId", "設備號碼"),
                self.lang_manager.translate("common.description", "異常內容"),
                self.lang_manager.translate("common.startTime", "發生時刻"),
                self.lang_manager.translate("common.impactQty", "影響數量"),
                self.lang_manager.translate("common.actionTaken", "對應內容"),
                self.lang_manager.translate("common.image", "圖片"),
                self.lang_manager.translate("common.createdAt", "創建時間")
            ]
            
            for col, header in zip(equipment_columns, equipment_headers):
                equipment_tree.heading(col, text=header)
                equipment_tree.column(col, width=80)
            
            equipment_tree.column("Description", width=150)
            equipment_tree.column("Action Taken", width=150)
            equipment_tree.column("Image", width=50)
            
            for log in equipment_logs:
                has_image = "✓" if log['image_path'] else "✗"
                equipment_tree.insert('', tk.END, values=(
                    log['id'],
                    log['equip_id'],
                    log['description'],
                    log['start_time'] or "",
                    log['impact_qty'],
                    log['action_taken'] or "",
                    has_image,
                    log['created_at']
                ))
            
            equipment_scrollbar = ttk.Scrollbar(equipment_frame, orient=tk.VERTICAL, command=equipment_tree.yview)
            equipment_tree.configure(yscrollcommand=equipment_scrollbar.set)
            
            equipment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            equipment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            ttk.Label(equipment_frame, text=self.lang_manager.translate("common.noRecords", "無記錄")).pack()
        
        # 異常批次記錄
        lot_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.lotLogs", "異常批次"), padding="10")
        lot_frame.pack(fill=tk.BOTH, expand=True)
        
        lot_logs = self.lot_manager.get_lot_logs(report_id)
        
        if lot_logs:
            lot_columns = ("ID", "Lot ID", "Description", "Status", "Notes", "Created At")
            lot_tree = ttk.Treeview(lot_frame, columns=lot_columns, show='headings', height=5)
            
            lot_headers = [
                "ID",
                self.lang_manager.translate("common.lotId", "批號"),
                self.lang_manager.translate("common.description", "異常內容"),
                self.lang_manager.translate("common.status", "處置狀況"),
                self.lang_manager.translate("common.notes", "特記事項"),
                self.lang_manager.translate("common.createdAt", "創建時間")
            ]
            
            for col, header in zip(lot_columns, lot_headers):
                lot_tree.heading(col, text=header)
                lot_tree.column(col, width=100)
            
            lot_tree.column("Description", width=150)
            lot_tree.column("Notes", width=150)
            
            for log in lot_logs:
                lot_tree.insert('', tk.END, values=(
                    log['id'],
                    log['lot_id'],
                    log['description'],
                    log['status'] or "",
                    log['notes'] or "",
                    log['created_at']
                ))
            
            lot_scrollbar = ttk.Scrollbar(lot_frame, orient=tk.VERTICAL, command=lot_tree.yview)
            lot_tree.configure(yscrollcommand=lot_scrollbar.set)
            
            lot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            lot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            ttk.Label(lot_frame, text=self.lang_manager.translate("common.noRecords", "無記錄")).pack()
    
    def get_username_by_id(self, user_id: int) -> str:
        """根據用戶ID獲取用戶名"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else "Unknown"
    
    def show_fill_report(self):
        """顯示填寫報表頁面"""
        self.clear_content_frame()
        self.current_page = "fill_report"
        
        # 更新標題
        self.title_label.config(text=self.lang_manager.translate("common.fillReport", "填寫日報"))
        
        # 填報頁面內容
        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)
        
        # 創建筆記本控件（分頁）
        notebook = ttk.Notebook(content)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 基本信息頁面
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text=self.lang_manager.translate("common.basicInfo", "基本信息"))
        self.create_basic_info_tab(basic_frame)
        
        # 出勤記錄頁面
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text=self.lang_manager.translate("common.attendance", "出勤記錄"))
        self.create_attendance_tab(attendance_frame)
        
        # 設備異常頁面
        equipment_frame = ttk.Frame(notebook)
        notebook.add(equipment_frame, text=self.lang_manager.translate("common.equipment", "設備異常"))
        self.create_equipment_tab(equipment_frame)
        
        # 異常批次頁面
        lot_frame = ttk.Frame(notebook)
        notebook.add(lot_frame, text=self.lang_manager.translate("common.lotLogs", "異常批次"))
        self.create_lot_tab(lot_frame)
        
        # 總結頁面
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text=self.lang_manager.translate("common.summary", "總結"))
        self.create_summary_tab(summary_frame)
        
        # 底部按鈕
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text=self.lang_manager.translate("common.save", "保存"), command=self.save_daily_report).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang_manager.translate("common.cancel", "取消"), command=self.show_home).pack(side=tk.LEFT)
    
    def create_basic_info_tab(self, parent):
        """創建基本信息頁面"""
        # 日期
        date_frame = ttk.Frame(parent, padding="10")
        date_frame.pack(fill=tk.X)
        
        ttk.Label(date_frame, text=self.lang_manager.translate("common.date", "日期")).pack(anchor=tk.W)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.date_var, state="readonly").pack(fill=tk.X, pady=(5, 10))
        
        # 班別
        shift_frame = ttk.Frame(parent, padding="10")
        shift_frame.pack(fill=tk.X)
        
        ttk.Label(shift_frame, text=self.lang_manager.translate("common.shift", "班別")).pack(anchor=tk.W)
        self.shift_var = tk.StringVar(value="Day")
        shift_combo = ttk.Combobox(
            shift_frame, 
            textvariable=self.shift_var, 
            values=["Day", "Night"],
            state="readonly"
        )
        shift_combo.pack(fill=tk.X, pady=(5, 10))
        
        # 區域
        area_frame = ttk.Frame(parent, padding="10")
        area_frame.pack(fill=tk.X)
        
        ttk.Label(area_frame, text=self.lang_manager.translate("common.area", "區域")).pack(anchor=tk.W)
        self.area_var = tk.StringVar(value="etching_D")
        area_combo = ttk.Combobox(
            area_frame, 
            textvariable=self.area_var, 
            values=["etching_D", "etching_E", "litho", "thin_film"],
            state="readonly"
        )
        area_combo.pack(fill=tk.X, pady=(5, 10))
    
    def create_attendance_tab(self, parent):
        """創建出勤記錄頁面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 輸入區域
        input_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.addRecord", "添加記錄"), padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 開發員工類別
        category_frame = ttk.Frame(input_frame)
        category_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(category_frame, text=self.lang_manager.translate("common.category", "類別")).pack(side=tk.LEFT)
        self.attendance_category_var = tk.StringVar(value="Regular")
        category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.attendance_category_var,
            values=["Regular", "Contract"],
            state="readonly"
        )
        category_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 定員、出勤、欠勤、理由
        counts_frame = ttk.Frame(input_frame)
        counts_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 定員
        ttk.Label(counts_frame, text=self.lang_manager.translate("common.scheduled", "定員")).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.scheduled_var = tk.StringVar(value="0")
        scheduled_entry = ttk.Entry(counts_frame, textvariable=self.scheduled_var, width=10)
        scheduled_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 出勤
        ttk.Label(counts_frame, text=self.lang_manager.translate("common.present", "出勤")).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.present_var = tk.StringVar(value="0")
        present_entry = ttk.Entry(counts_frame, textvariable=self.present_var, width=10)
        present_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # 欠勤
        ttk.Label(counts_frame, text=self.lang_manager.translate("common.absent", "欠勤")).grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.absent_var = tk.StringVar(value="0")
        absent_entry = ttk.Entry(counts_frame, textvariable=self.absent_var, width=10)
        absent_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 20))
        
        # 理由
        ttk.Label(counts_frame, text=self.lang_manager.translate("common.reason", "理由")).grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        self.reason_var = tk.StringVar()
        ttk.Entry(counts_frame, textvariable=self.reason_var, width=20).grid(row=0, column=7, sticky=tk.W)
        
        # 添加按鈕
        ttk.Button(input_frame, text=self.lang_manager.translate("common.add", "添加"), command=self.add_attendance_record).pack(pady=(10, 0))
        
        # 記錄表格
        table_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.records", "記錄"), padding="5")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Category", "Scheduled", "Present", "Absent", "Reason", "Actions")
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        headers = [
            "ID",
            self.lang_manager.translate("common.category", "類別"),
            self.lang_manager.translate("common.scheduled", "定員"),
            self.lang_manager.translate("common.present", "出勤"),
            self.lang_manager.translate("common.absent", "欠勤"),
            self.lang_manager.translate("common.reason", "理由"),
            self.lang_manager.translate("common.actions", "操作")
        ]
        
        for col, header in zip(columns, headers):
            self.attendance_tree.heading(col, text=header)
            self.attendance_tree.column(col, width=80)
        
        self.attendance_tree.column("Reason", width=150)
        self.attendance_tree.column("Actions", width=100)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存儲臨時記錄
        self.temporary_attendance_records = []
    
    def create_equipment_tab(self, parent):
        """創建設備異常頁面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 輸入區域
        input_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.addRecord", "添加記錄"), padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 設備號碼
        id_frame = ttk.Frame(input_frame)
        id_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(id_frame, text=self.lang_manager.translate("common.equipId", "設備號碼")).pack(anchor=tk.W)
        self.equip_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.equip_id_var).pack(fill=tk.X, pady=(5, 0))
        
        # 異常內容
        desc_frame = ttk.Frame(input_frame)
        desc_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(desc_frame, text=self.lang_manager.translate("common.description", "異常內容")).pack(anchor=tk.W)
        self.equip_desc_var = tk.StringVar()
        ttk.Entry(desc_frame, textvariable=self.equip_desc_var).pack(fill=tk.X, pady=(5, 0))
        
        # 發生時刻和影響數量
        time_qty_frame = ttk.Frame(input_frame)
        time_qty_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(time_qty_frame, text=self.lang_manager.translate("common.startTime", "發生時刻")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.equip_start_time_var = tk.StringVar()
        ttk.Entry(time_qty_frame, textvariable=self.equip_start_time_var, width=15).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(time_qty_frame, text=self.lang_manager.translate("common.impactQty", "影響數量")).grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        self.equip_impact_qty_var = tk.StringVar(value="0")
        ttk.Entry(time_qty_frame, textvariable=self.equip_impact_qty_var, width=10).grid(row=0, column=3, sticky=tk.W)
        
        # 對應內容
        action_frame = ttk.Frame(input_frame)
        action_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(action_frame, text=self.lang_manager.translate("common.actionTaken", "對應內容")).pack(anchor=tk.W)
        self.equip_action_var = tk.StringVar()
        ttk.Entry(action_frame, textvariable=self.equip_action_var).pack(fill=tk.X, pady=(5, 0))
        
        # 圖片上傳
        image_frame = ttk.Frame(input_frame)
        image_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(image_frame, text=self.lang_manager.translate("common.image", "圖片")).pack(anchor=tk.W)
        self.image_path_var = tk.StringVar()
        image_path_entry = ttk.Entry(image_frame, textvariable=self.image_path_var, state="readonly", width=50)
        image_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(5, 0), padx=(0, 5))
        ttk.Button(image_frame, text=self.lang_manager.translate("common.browse", "瀏覽"), command=self.browse_image).pack(side=tk.LEFT)
        
        # 添加按鈕
        ttk.Button(input_frame, text=self.lang_manager.translate("common.add", "添加"), command=self.add_equipment_log).pack(pady=(10, 0))
        
        # 記錄表格
        table_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.records", "記錄"), padding="5")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Equipment ID", "Description", "Start Time", "Impact Qty", "Action Taken", "Image", "Actions")
        self.equipment_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        headers = [
            "ID",
            self.lang_manager.translate("common.equipId", "設備號碼"),
            self.lang_manager.translate("common.description", "異常內容"),
            self.lang_manager.translate("common.startTime", "發生時刻"),
            self.lang_manager.translate("common.impactQty", "影響數量"),
            self.lang_manager.translate("common.actionTaken", "對應內容"),
            self.lang_manager.translate("common.image", "圖片"),
            self.lang_manager.translate("common.actions", "操作")
        ]
        
        for col, header in zip(columns, headers):
            self.equipment_tree.heading(col, text=header)
            self.equipment_tree.column(col, width=80)
        
        self.equipment_tree.column("Description", width=120)
        self.equipment_tree.column("Action Taken", width=120)
        self.equipment_tree.column("Actions", width=100)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.equipment_tree.yview)
        self.equipment_tree.configure(yscrollcommand=scrollbar.set)
        
        self.equipment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存儲臨時記錄
        self.temporary_equipment_logs = []
    
    def create_lot_tab(self, parent):
        """創建異常批次頁面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 輸入區域
        input_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.addRecord", "添加記錄"), padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 批號
        id_frame = ttk.Frame(input_frame)
        id_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(id_frame, text=self.lang_manager.translate("common.lotId", "批號")).pack(anchor=tk.W)
        self.lot_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.lot_id_var).pack(fill=tk.X, pady=(5, 0))
        
        # 異常內容
        desc_frame = ttk.Frame(input_frame)
        desc_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(desc_frame, text=self.lang_manager.translate("common.description", "異常內容")).pack(anchor=tk.W)
        self.lot_desc_var = tk.StringVar()
        ttk.Entry(desc_frame, textvariable=self.lot_desc_var).pack(fill=tk.X, pady=(5, 0))
        
        # 處置狀況和特記事項
        status_notes_frame = ttk.Frame(input_frame)
        status_notes_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(status_notes_frame, text=self.lang_manager.translate("common.status", "處置狀況")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.lot_status_var = tk.StringVar()
        ttk.Entry(status_notes_frame, textvariable=self.lot_status_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(status_notes_frame, text=self.lang_manager.translate("common.notes", "特記事項")).grid(row=0, column=2, sticky=tk.W)
        self.lot_notes_var = tk.StringVar()
        ttk.Entry(status_notes_frame, textvariable=self.lot_notes_var, width=30).grid(row=0, column=3, sticky=tk.W)
        
        # 添加按鈕
        ttk.Button(input_frame, text=self.lang_manager.translate("common.add", "添加"), command=self.add_lot_log).pack(pady=(10, 0))
        
        # 記錄表格
        table_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.records", "記錄"), padding="5")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Lot ID", "Description", "Status", "Notes", "Actions")
        self.lot_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        headers = [
            "ID",
            self.lang_manager.translate("common.lotId", "批號"),
            self.lang_manager.translate("common.description", "異常內容"),
            self.lang_manager.translate("common.status", "處置狀況"),
            self.lang_manager.translate("common.notes", "特記事項"),
            self.lang_manager.translate("common.actions", "操作")
        ]
        
        for col, header in zip(columns, headers):
            self.lot_tree.heading(col, text=header)
            self.lot_tree.column(col, width=100)
        
        self.lot_tree.column("Description", width=150)
        self.lot_tree.column("Notes", width=150)
        self.lot_tree.column("Actions", width=100)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.lot_tree.yview)
        self.lot_tree.configure(yscrollcommand=scrollbar.set)
        
        self.lot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存儲臨時記錄
        self.temporary_lot_logs = []
    
    def create_summary_tab(self, parent):
        """創建總結頁面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Key Machine Output
        key_output_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.keyOutput", "Key Machine Output"), padding="10")
        key_output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.summary_key_output_var = tk.StringVar()
        self.key_output_text = tk.Text(key_output_frame, height=5, wrap=tk.WORD)
        self.key_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Key Issues
        key_issues_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.issues", "Key Issues"), padding="10")
        key_issues_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.summary_issues_var = tk.StringVar()
        self.issues_text = tk.Text(key_issues_frame, height=5, wrap=tk.WORD)
        self.issues_text.pack(fill=tk.BOTH, expand=True)
        
        # Countermeasures
        countermeasures_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.translate("common.countermeasures", "Countermeasures"), padding="10")
        countermeasures_frame.pack(fill=tk.BOTH, expand=True)
        
        self.summary_countermeasures_var = tk.StringVar()
        self.countermeasures_text = tk.Text(countermeasures_frame, height=5, wrap=tk.WORD)
        self.countermeasures_text.pack(fill=tk.BOTH, expand=True)
    
    def add_attendance_record(self):
        """添加出勤記錄"""
        try:
            scheduled = int(self.scheduled_var.get()) if self.scheduled_var.get().isdigit() else 0
            present = int(self.present_var.get()) if self.present_var.get().isdigit() else 0
            absent = int(self.absent_var.get()) if self.absent_var.get().isdigit() else 0
        except ValueError:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.invalidNumber", "請輸入有效的數字")
            )
            return
        
        # 驗證數據邏輯
        if present + absent != scheduled:
            messagebox.showwarning(
                self.lang_manager.translate("common.warning", "警告"),
                self.lang_manager.translate("common.attendanceMismatch", "出勤人數加上欠勤人數應等於定員人數")
            )
        
        record = {
            'id': len(self.temporary_attendance_records) + 1,  # 臨時 ID
            'category': self.attendance_category_var.get(),
            'scheduled_count': scheduled,
            'present_count': present,
            'absent_count': absent,
            'reason': self.reason_var.get()
        }
        
        self.temporary_attendance_records.append(record)
        
        # 更新表格
        self.attendance_tree.insert('', tk.END, values=(
            record['id'],
            record['category'],
            record['scheduled_count'],
            record['present_count'],
            record['absent_count'],
            record['reason'],
            self.lang_manager.translate("common.delete", "刪除")
        ))
    
    def add_equipment_log(self):
        """添加設備異常記錄"""
        if not self.equip_id_var.get().strip() or not self.equip_desc_var.get().strip():
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.pleaseFillRequired", "請填寫設備號碼和異常內容")
            )
            return
        
        try:
            impact_qty = int(self.equip_impact_qty_var.get()) if self.equip_impact_qty_var.get().isdigit() else 0
        except ValueError:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.invalidNumber", "請輸入有效的數字")
            )
            return
        
        log = {
            'id': len(self.temporary_equipment_logs) + 1,  # 臨時 ID
            'equip_id': self.equip_id_var.get().strip(),
            'description': self.equip_desc_var.get().strip(),
            'start_time': self.equip_start_time_var.get().strip(),
            'impact_qty': impact_qty,
            'action_taken': self.equip_action_var.get().strip(),
            'image_path': self.image_path_var.get().strip()
        }
        
        self.temporary_equipment_logs.append(log)
        
        # 更新表格
        has_image = "✓" if log['image_path'] else "✗"
        self.equipment_tree.insert('', tk.END, values=(
            log['id'],
            log['equip_id'],
            log['description'],
            log['start_time'],
            log['impact_qty'],
            log['action_taken'],
            has_image,
            self.lang_manager.translate("common.delete", "刪除")
        ))
    
    def add_lot_log(self):
        """添加異常批次記錄"""
        if not self.lot_id_var.get().strip() or not self.lot_desc_var.get().strip():
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.pleaseFillRequired", "請填寫批號和異常內容")
            )
            return
        
        log = {
            'id': len(self.temporary_lot_logs) + 1,  # 臨時 ID
            'lot_id': self.lot_id_var.get().strip(),
            'description': self.lot_desc_var.get().strip(),
            'status': self.lot_status_var.get().strip(),
            'notes': self.lot_notes_var.get().strip()
        }
        
        self.temporary_lot_logs.append(log)
        
        # 更新表格
        self.lot_tree.insert('', tk.END, values=(
            log['id'],
            log['lot_id'],
            log['description'],
            log['status'],
            log['notes'],
            self.lang_manager.translate("common.delete", "刪除")
        ))
    
    def browse_image(self):
        """瀏覽圖片文件"""
        if not PIL_AVAILABLE:
            messagebox.showwarning(
                self.lang_manager.translate("common.warning", "警告"),
                self.lang_manager.translate("common.imageFeatureNotAvailable", "圖片功能需要安裝 Pillow 模組")
            )
            return

        file_path = filedialog.askopenfilename(
            title=self.lang_manager.translate("common.selectImage", "選擇圖片"),
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            # 複製圖片到上傳目錄
            import shutil
            from pathlib import Path

            filename = os.path.basename(file_path)
            dest_path = os.path.join("uploads", filename)

            # 處理重複文件名
            counter = 1
            name, ext = os.path.splitext(dest_path)
            while os.path.exists(dest_path):
                dest_path = f"{name}_{counter}{ext}"
                counter += 1

            shutil.copy2(file_path, dest_path)
            self.image_path_var.set(dest_path)
    
    def save_daily_report(self):
        """保存日報表"""
        if not self.user_manager.current_user:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.notLoggedIn", "請先登入")
            )
            return
        
        # 獲取總結文本
        key_output = self.key_output_text.get(1.0, tk.END).strip()
        issues = self.issues_text.get(1.0, tk.END).strip()
        countermeasures = self.countermeasures_text.get(1.0, tk.END).strip()
        
        # 創建報表
        try:
            report_id = self.daily_report_manager.create_report(
                self.date_var.get(),
                self.shift_var.get(),
                self.area_var.get(),
                self.user_manager.current_user['id'],
                key_output,
                issues,
                countermeasures
            )
            
            # 保存臨時記錄到數據庫
            for record in self.temporary_attendance_records:
                self.attendance_manager.add_attendance_record(
                    report_id,
                    record['category'],
                    record['scheduled_count'],
                    record['present_count'],
                    record['absent_count'],
                    record['reason']
                )
            
            for log in self.temporary_equipment_logs:
                self.equipment_manager.add_equipment_log(
                    report_id,
                    log['equip_id'],
                    log['description'],
                    log['start_time'],
                    log['impact_qty'],
                    log['action_taken'],
                    log['image_path']
                )
            
            for log in self.temporary_lot_logs:
                self.lot_manager.add_lot_log(
                    report_id,
                    log['lot_id'],
                    log['description'],
                    log['status'],
                    log['notes']
                )
            
            messagebox.showinfo(
                self.lang_manager.translate("common.success", "成功"),
                self.lang_manager.translate("common.reportSaved", "報表已成功保存")
            )
            
            # 清空臨時記錄
            self.temporary_attendance_records = []
            self.temporary_equipment_logs = []
            self.temporary_lot_logs = []
            
            # 清空表格
            for item in self.attendance_tree.get_children():
                self.attendance_tree.delete(item)
            for item in self.equipment_tree.get_children():
                self.equipment_tree.delete(item)
            for item in self.lot_tree.get_children():
                self.lot_tree.delete(item)
            
            # 返回主頁面
            self.show_home()
            
        except Exception as e:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                f"{self.lang_manager.translate('common.saveError', '保存失敗')}: {str(e)}"
            )
    
    def logout(self):
        """登出"""
        self.user_manager.current_user = None
        self.update_navbar_visibility()
        
        # 清空臨時數據
        self.temporary_attendance_records = []
        self.temporary_equipment_logs = []
        self.temporary_lot_logs = []
        
        # 顯示登入窗口
        self.show_login()


def main():
    """主函數"""
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()