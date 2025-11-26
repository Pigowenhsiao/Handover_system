"""
異常批次記錄界面組件
實現異常批次記錄的輸入和顯示功能
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class LotLogSection:
    """
    異常批次記錄界面組件
    """
    
    def __init__(self, parent, lang_manager):
        """
        初始化異常批次記錄組件
        
        Args:
            parent: 父組件
            lang_manager: 語言管理器實例
        """
        self.parent = parent
        self.lang_manager = lang_manager
        
        # 創建界面
        self.setup_ui()
    
    def setup_ui(self):
        """設置界面元素"""
        # 主框架
        self.main_frame = ttk.LabelFrame(self.parent, text="異常批次記錄", padding="10")
        
        # 輸入區域
        input_frame = ttk.LabelFrame(self.main_frame, text="異常批次輸入", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 批號
        ttk.Label(input_frame, text="批號:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.lot_id_var = tk.StringVar()
        lot_id_entry = ttk.Entry(input_frame, textvariable=self.lot_id_var, width=20)
        lot_id_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10), pady=2)
        
        # 異常內容
        ttk.Label(input_frame, text="異常內容:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(input_frame, textvariable=self.description_var, width=50)
        description_entry.grid(row=0, column=3, sticky=tk.W, pady=2)
        
        # 處置狀況
        ttk.Label(input_frame, text="處置狀況:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.status_var = tk.StringVar()
        status_entry = ttk.Entry(input_frame, textvariable=self.status_var, width=30)
        status_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=2)
        
        # 特記事項
        ttk.Label(input_frame, text="特記事項:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.notes_var = tk.StringVar()
        notes_entry = ttk.Entry(input_frame, textvariable=self.notes_var, width=50)
        notes_entry.grid(row=1, column=3, sticky=tk.W, pady=2)
        
        # 設置列權重使描述和備註欄位可擴展
        input_frame.columnconfigure(3, weight=1)
        
        # 按鈕框架
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, sticky=tk.E, pady=5)
        
        # 添加記錄按鈕
        self.add_button = ttk.Button(
            button_frame,
            text="添加記錄",
            command=self.add_lot_log
        )
        self.add_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 重置按鈕
        self.reset_button = ttk.Button(
            button_frame,
            text="重置",
            command=self.reset_fields
        )
        self.reset_button.pack(side=tk.RIGHT)
        
        # 批次記錄表格
        table_frame = ttk.LabelFrame(self.main_frame, text="異常批次記錄", padding="5")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 創建表格
        columns = ("ID", "Lot ID", "Description", "Status", "Notes", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        
        # 定義表頭
        headers = {
            "ID": "ID",
            "Lot ID": "批號",
            "Description": "異常內容",
            "Status": "處置狀況",
            "Notes": "特記事項",
            "Date": "日期"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers.get(col, col))
            if col in ["Description", "Notes"]:
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=80)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定雙擊事件以編輯記錄
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # 更新界面語言
        self.update_ui_language()
    
    def update_ui_language(self):
        """根據當前語言更新界面標示"""
        # 更新框架標題
        self.main_frame.config(text=self.lang_manager.get_text("lot.logs", "異常批次記錄"))
        self.input_frame.config(text=self.lang_manager.get_text("lot.input", "異常批次輸入"))
        self.table_frame.config(text=self.lang_manager.get_text("lot.logs", "異常批次記錄"))
        
        # 更新標籤文本
        for child in self.input_frame.winfo_children():
            if isinstance(child, tk.Label):
                text = child.cget("text")
                if text == "批號:":
                    child.config(text=f"{self.lang_manager.get_text('common.lotId', '批號')}:")
                elif text == "異常內容:":
                    child.config(text=f"{self.lang_manager.get_text('common.description', '異常內容')}:")
                elif text == "處置狀況:":
                    child.config(text=f"{self.lang_manager.get_text('lot.status', '處置狀況')}:")
                elif text == "特記事項:":
                    child.config(text=f"{self.lang_manager.get_text('common.notes', '特記事項')}:")
        
        # 更新按鈕文本
        self.add_button.config(text=self.lang_manager.get_text("common.add", "添加"))
        self.reset_button.config(text=self.lang_manager.get_text("common.reset", "重置"))
        
        # 更新表格標頭
        headers = {
            "ID": self.lang_manager.get_text("common.id", "ID"),
            "Lot ID": self.lang_manager.get_text("common.lotId", "批號"),
            "Description": self.lang_manager.get_text("common.description", "異常內容"),
            "Status": self.lang_manager.get_text("lot.status", "處置狀況"),
            "Notes": self.lang_manager.get_text("common.notes", "特記事項"),
            "Date": self.lang_manager.get_text("common.date", "日期")
        }
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=headers.get(col, col))
    
    def add_lot_log(self):
        """添加批次異常記錄"""
        # 驗證必要字段
        if not self.lot_id_var.get().strip() or not self.description_var.get().strip():
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("lot.requireFields", "批號和異常內容是必填字段")
            )
            return
        
        try:
            # 在實際應用中，這裡會調用 API 保存數據
            # 目前僅添加到表格中
            item_id = len(self.tree.get_children()) + 1
            self.tree.insert("", "end", values=(
                item_id,
                self.lot_id_var.get().strip(),
                self.description_var.get().strip(),
                self.status_var.get() or "",
                self.notes_var.get() or "",
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            
            # 清空輸入字段
            self.reset_fields()
            
            messagebox.showinfo(
                self.lang_manager.get_text("common.success", "成功"),
                self.lang_manager.get_text("lot.recordAdded", "異常批次記錄已添加")
            )
        except Exception as e:
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                f"{self.lang_manager.get_text('common.operationFailed', '操作失敗')}: {str(e)}"
            )
    
    def on_double_click(self, event):
        """處理雙擊表格項目以進行編輯"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            
            # 將選定項目的數據載入到輸入字段
            if len(values) >= 5:  # 確保有足夠的值
                self.lot_id_var.set(values[1])
                self.description_var.set(values[2])
                self.status_var.set(values[3] or "")
                self.notes_var.set(values[4] or "")
    
    def reset_fields(self):
        """重置所有輸入字段"""
        self.lot_id_var.set("")
        self.description_var.set("")
        self.status_var.set("")
        self.notes_var.set("")
    
    def get_widget(self):
        """獲取組件主框架"""
        return self.main_frame
    
    def load_data(self, lots_data):
        """載入異常批次記錄數據到表格"""
        # 清空現有數據
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新數據
        for lot in lots_data:
            self.tree.insert("", "end", values=(
                lot.get("id", ""),
                lot.get("lot_id", ""),
                lot.get("description", ""),
                lot.get("status", ""),
                lot.get("notes", ""),
                lot.get("created_at", "")
            ))
    
    def get_data(self):
        """獲取當前表格中的所有記錄"""
        records = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            records.append({
                "id": values[0],
                "lot_id": values[1],
                "description": values[2],
                "status": values[3],
                "notes": values[4],
                "created_at": values[5]
            })
        return records