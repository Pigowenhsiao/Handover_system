"""
設備異常記錄界面組件
實現設備異常記錄的輸入和顯示功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os


class EquipmentLogSection:
    """
    設備異常記錄界面組件
    """
    
    def __init__(self, parent, lang_manager):
        """
        初始化設備異常記錄組件
        
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
        self.main_frame = ttk.LabelFrame(self.parent, text="設備異常記錄", padding="10")
        
        # 輸入區域
        input_frame = ttk.LabelFrame(self.main_frame, text="設備異常輸入", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 設備號碼
        ttk.Label(input_frame, text="設備號碼:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.equip_id_var = tk.StringVar()
        equip_id_entry = ttk.Entry(input_frame, textvariable=self.equip_id_var, width=20)
        equip_id_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10), pady=2)
        
        # 異常內容
        ttk.Label(input_frame, text="異常內容:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(input_frame, textvariable=self.description_var, width=50)
        description_entry.grid(row=0, column=3, sticky=tk.W, pady=2)
        
        # 發生時刻
        ttk.Label(input_frame, text="發生時刻:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.start_time_var = tk.StringVar()
        start_time_entry = ttk.Entry(input_frame, textvariable=self.start_time_var, width=20)
        start_time_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=2)
        
        # 影響數量
        ttk.Label(input_frame, text="影響數量:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.impact_qty_var = tk.StringVar(value="0")
        impact_qty_entry = ttk.Entry(input_frame, textvariable=self.impact_qty_var, width=10)
        impact_qty_entry.grid(row=1, column=3, sticky=tk.W, pady=2)
        
        # 對應內容
        ttk.Label(input_frame, text="對應內容:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.action_taken_var = tk.StringVar()
        action_taken_entry = ttk.Entry(input_frame, textvariable=self.action_taken_var, width=80)
        action_taken_entry.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        # 圖片上傳
        ttk.Label(input_frame, text="圖片上傳:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.image_path_var = tk.StringVar()
        image_path_entry = ttk.Entry(input_frame, textvariable=self.image_path_var, width=70, state="readonly")
        image_path_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=2)
        browse_button = ttk.Button(input_frame, text="瀏覽", command=self.browse_image)
        browse_button.grid(row=3, column=3, sticky=tk.W, padx=(5, 0), pady=2)
        
        # 設置列權重使對應內容和圖片路徑欄位可擴展
        input_frame.columnconfigure(3, weight=1)
        
        # 按鈕框架
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, sticky=tk.E, pady=5)
        
        # 添加記錄按鈕
        self.add_button = ttk.Button(
            button_frame,
            text="添加記錄",
            command=self.add_equipment_log
        )
        self.add_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 重置按鈕
        self.reset_button = ttk.Button(
            button_frame,
            text="重置",
            command=self.reset_fields
        )
        self.reset_button.pack(side=tk.RIGHT)
        
        # 記錄表格
        table_frame = ttk.LabelFrame(self.main_frame, text="設備異常記錄", padding="5")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 創建表格
        columns = ("ID", "Equip ID", "Description", "Start Time", "Impact Qty", "Action Taken", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        
        # 定義表頭
        headers = {
            "ID": "ID",
            "Equip ID": "設備ID",
            "Description": "異常內容",
            "Start Time": "發生時刻",
            "Impact Qty": "影響數量",
            "Action Taken": "對應內容",
            "Date": "日期"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers.get(col, col))
            if col in ["Description", "Action Taken"]:
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
        self.main_frame.config(text=self.lang_manager.get_text("common.equipmentLogs", "設備異常記錄"))
        self.input_frame.config(text=self.lang_manager.get_text("equipment.input", "設備異常輸入"))
        self.table_frame.config(text=self.lang_manager.get_text("equipment.logs", "設備異常記錄"))
        
        # 更新標籤文本
        for child in self.input_frame.winfo_children():
            if isinstance(child, tk.Label):
                text = child.cget("text")
                if text == "設備ID:":
                    child.config(text=f"{self.lang_manager.get_text('equipment.equipId', '設備ID')}:")
                elif text == "異常內容:":
                    child.config(text=f"{self.lang_manager.get_text('common.description', '異常內容')}:")
                elif text == "發生時刻:":
                    child.config(text=f"{self.lang_manager.get_text('equipment.startTime', '發生時刻')}:")
                elif text == "影響數量:":
                    child.config(text=f"{self.lang_manager.get_text('equipment.impactQty', '影響數量')}:")
                elif text == "對應內容:":
                    child.config(text=f"{self.lang_manager.get_text('equipment.actionTaken', '對應內容')}:")
                elif text == "圖片上傳:":
                    child.config(text=f"{self.lang_manager.get_text('common.imageUpload', '圖片上傳')}:")
        
        # 更新按鈕文本
        self.add_button.config(text=self.lang_manager.get_text("common.add", "添加"))
        self.reset_button.config(text=self.lang_manager.get_text("common.reset", "重置"))
        
        # 更新表格標頭
        headers = {
            "ID": self.lang_manager.get_text("common.id", "ID"),
            "Equip ID": self.lang_manager.get_text("equipment.equipId", "設備ID"),
            "Description": self.lang_manager.get_text("common.description", "異常內容"),
            "Start Time": self.lang_manager.get_text("equipment.startTime", "發生時刻"),
            "Impact Qty": self.lang_manager.get_text("equipment.impactQty", "影響數量"),
            "Action Taken": self.lang_manager.get_text("equipment.actionTaken", "對應內容"),
            "Date": self.lang_manager.get_text("common.date", "日期")
        }
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=headers.get(col, col))
    
    def browse_image(self):
        """瀏覽圖片文件"""
        file_path = filedialog.askopenfilename(
            title=self.lang_manager.get_text("common.selectImage", "選擇圖片"),
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # 驗證文件類型是否支援
            supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in supported_extensions:
                # 記錄文件路徑，實際應用中可能需要上傳到服務器
                self.image_path_var.set(file_path)
            else:
                messagebox.showerror(
                    self.lang_manager.get_text("common.error", "錯誤"),
                    self.lang_manager.get_text("common.unsupportedFormat", "不支援的文件格式")
                )
    
    def add_equipment_log(self):
        """添加設備異常記錄"""
        # 驗證必要字段
        if not self.equip_id_var.get().strip() or not self.description_var.get().strip():
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("equipment.requireFields", "設備ID和異常內容是必填字段")
            )
            return
        
        try:
            # 驗證影響數量是否為有效數字
            impact_qty = int(self.impact_qty_var.get() or "0")
            
            # 在實際應用中，這裡會調用 API 保存數據
            # 目前僅添加到表格中
            item_id = len(self.tree.get_children()) + 1
            self.tree.insert("", "end", values=(
                item_id,
                self.equip_id_var.get().strip(),
                self.description_var.get().strip(),
                self.start_time_var.get() or "",
                impact_qty,
                self.action_taken_var.get() or "",
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            
            # 清空輸入字段
            self.reset_fields()
            
            messagebox.showinfo(
                self.lang_manager.get_text("common.success", "成功"),
                self.lang_manager.get_text("equipment.recordAdded", "設備異常記錄已添加")
            )
        except ValueError:
            messagebox.showerror(
                self.lang_manager.get_text("common.error", "錯誤"),
                self.lang_manager.get_text("common.invalidNumber", "影響數量必須是有效數字")
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
            if len(values) >= 6:  # 確保有足夠的值
                self.equip_id_var.set(values[1])
                self.description_var.set(values[2])
                self.start_time_var.set(values[3])
                self.impact_qty_var.set(str(values[4]))
                self.action_taken_var.set(values[5])
    
    def reset_fields(self):
        """重置所有輸入字段"""
        self.equip_id_var.set("")
        self.description_var.set("")
        self.start_time_var.set("")
        self.impact_qty_var.set("0")
        self.action_taken_var.set("")
        self.image_path_var.set("")
    
    def get_widget(self):
        """獲取組件主框架"""
        return self.main_frame
    
    def load_data(self, logs_data):
        """載入設備異常記錄數據到表格"""
        # 清空現有數據
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新數據
        for log in logs_data:
            self.tree.insert("", "end", values=(
                log.get("id", ""),
                log.get("equip_id", ""),
                log.get("description", ""),
                log.get("start_time", ""),
                log.get("impact_qty", 0),
                log.get("action_taken", ""),
                log.get("created_at", "")
            ))
    
    def get_data(self):
        """獲取當前表格中的所有記錄"""
        records = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            records.append({
                "id": values[0],
                "equip_id": values[1],
                "description": values[2],
                "start_time": values[3],
                "impact_qty": values[4],
                "action_taken": values[5],
                "created_at": values[6]
            })
        return records