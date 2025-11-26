"""
電子交接本系統前端主應用程式
使用 tkinter 創建的多語言界面
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

from frontend.i18n.language_manager import frontend_lang_manager
from frontend.src.components.language_selector import LanguageSelector
from frontend.src.components.attendance_section import AttendanceSection


class MainApplication:
    """
    電子交接本系統主應用程式界面
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(frontend_lang_manager.get_text("header.title", "電子交接系統"))
        self.root.geometry("1200x800")
        
        # 語言管理器
        self.lang_manager = frontend_lang_manager
        
        # 創建界面
        self.setup_ui()
        
        # 保存當前報告 ID
        self.current_report_id = None
    
    def setup_ui(self):
        """設置主界面"""
        # 主框架
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
        self.lang_selector = LanguageSelector(
            self.top_frame,
            self.lang_manager,
            callback=self.on_language_change
        )
        self.lang_selector.get_widget().pack(side=tk.RIGHT)
        
        # 主內容框架 (使用 Notebook 顯示不同頁面)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 創建各個頁面標籤
        self.create_daily_report_tab()
        self.create_attendance_tab()
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
        current_lang = self.lang_manager.get_current_language()
        lang_names = {"ja": "日本語", "zh": "中文", "en": "English"}
        lang_name = lang_names.get(current_lang, current_lang)
        self.status_var.set(f"就緒 - 當前語言: {lang_name}")
    
    def create_daily_report_tab(self):
        """創建日報表標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("navigation.reports", "報表"))
        
        # 日期和班別區域
        info_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("common.basicInfo", "基本信息"), padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 日期
        ttk.Label(info_frame, text=f"{self.lang_manager.get_text('common.date', '日期')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(info_frame, textvariable=self.date_var).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 班別
        ttk.Label(info_frame, text=f"{self.lang_manager.get_text('common.shift', '班別')}:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.shift_var = tk.StringVar(value="Day")
        shift_combo = ttk.Combobox(
            info_frame,
            textvariable=self.shift_var,
            values=["Day", "Night"],
            state="readonly"
        )
        shift_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # 區域
        ttk.Label(info_frame, text=f"{self.lang_manager.get_text('common.area', '區域')}:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.area_var = tk.StringVar(value="etching_D")
        area_combo = ttk.Combobox(
            info_frame,
            textvariable=self.area_var,
            values=["etching_D", "etching_E", "litho", "thin_film"],
            state="readonly"
        )
        area_combo.grid(row=0, column=5, sticky=tk.W)
        
        # Key Machine Output
        output_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.keyOutput", "Key Machine Output"), padding="5")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.key_output_text = tk.Text(output_frame, height=4)
        self.key_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Key Issues
        issues_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.issues", "Key Issues"), padding="5")
        issues_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.issues_text = tk.Text(issues_frame, height=4)
        self.issues_text.pack(fill=tk.BOTH, expand=True)
        
        # Countermeasures
        countermeasures_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.countermeasures", "Countermeasures"), padding="5")
        countermeasures_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.countermeasures_text = tk.Text(countermeasures_frame, height=4)
        self.countermeasures_text.pack(fill=tk.BOTH, expand=True)
        
        # 保存按鈕
        save_btn = ttk.Button(
            tab_frame,
            text=self.lang_manager.get_text("common.save", "保存"),
            command=self.save_daily_report
        )
        save_btn.grid(row=4, column=0, sticky=tk.E, pady=10)
    
    def create_attendance_tab(self):
        """創建出勤記錄標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("attendance.records", "出勤記錄"))
        
        # 使用出勤記錄組件 - 這會同時顯示正社員和契約社員的輸入欄位
        self.attendance_section = AttendanceSection(tab_frame, self.lang_manager, self)
        self.attendance_section.get_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_equipment_tab(self):
        """創建設備異常記錄標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("equipment.logs", "設備異常記錄"))
        
        # 設備ID
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('equipment.equipId', '設備ID')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_id_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.equip_id_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 異常內容
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('common.description', '異常內容')}:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5), pady=5)
        self.equip_desc_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.equip_desc_var, width=50).grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 發生時刻和影響數量
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('equipment.startTime', '發生時刻')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_start_time_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.equip_start_time_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('equipment.impactQty', '影響數量')}:").grid(row=1, column=2, sticky=tk.W, padx=(10, 5), pady=5)
        self.equip_impact_qty_var = tk.StringVar(value="0")
        ttk.Entry(tab_frame, textvariable=self.equip_impact_qty_var, width=10).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 對應內容
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('equipment.actionTaken', '對應內容')}:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.equip_action_taken_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.equip_action_taken_var, width=80).grid(row=2, column=1, columnspan=3, sticky=tk.W, pady=5)
        
        # 圖片上傳
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('common.image', '圖片')}:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=10)
        self.equip_image_path_var = tk.StringVar()
        image_frame = ttk.Frame(tab_frame)
        image_frame.grid(row=3, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
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
            tab_frame,
            text=self.lang_manager.get_text("common.add", "添加記錄"),
            command=self.add_equipment_log
        )
        add_btn.grid(row=4, column=3, sticky=tk.E, pady=10)
        
        # 配置列權重
        tab_frame.columnconfigure(3, weight=1)
    
    def create_lot_log_tab(self):
        """創建異常批次記錄標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("lot.logs", "異常批次記錄"))
        
        # 批號
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('lot.lotId', '批號')}:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_id_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.lot_id_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 異常內容
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('common.description', '異常內容')}:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5), pady=5)
        self.lot_desc_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.lot_desc_var, width=50).grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 處置狀況和特記事項
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('lot.status', '處置狀況')}:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.lot_status_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.lot_status_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(tab_frame, text=f"{self.lang_manager.get_text('common.notes', '特記事項')}:").grid(row=1, column=2, sticky=tk.W, padx=(10, 5), pady=5)
        self.lot_notes_var = tk.StringVar()
        ttk.Entry(tab_frame, textvariable=self.lot_notes_var, width=50).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 添加記錄按鈕
        add_btn = ttk.Button(
            tab_frame,
            text=self.lang_manager.get_text("common.add", "添加記錄"),
            command=self.add_lot_log
        )
        add_btn.grid(row=2, column=3, sticky=tk.E, pady=10)
        
        # 配置列權重
        tab_frame.columnconfigure(3, weight=1)
    
    def create_summary_tab(self):
        """創建總結標籤頁"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text=self.lang_manager.get_text("common.summary", "總結"))
        
        # Key Machine Output
        output_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.keyOutput", "Key Machine Output"), padding="5")
        output_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.summary_output_text = tk.Text(output_frame, height=4)
        self.summary_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Key Issues
        issues_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.issues", "Key Issues"), padding="5")
        issues_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.summary_issues_text = tk.Text(issues_frame, height=4)
        self.summary_issues_text.pack(fill=tk.BOTH, expand=True)
        
        # Countermeasures
        countermeasures_frame = ttk.LabelFrame(tab_frame, text=self.lang_manager.get_text("summary.countermeasures", "Countermeasures"), padding="5")
        countermeasures_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.summary_countermeasures_text = tk.Text(countermeasures_frame, height=4)
        self.summary_countermeasures_text.pack(fill=tk.BOTH, expand=True)
    
    def on_language_change(self, new_language_code):
        """處理語言變化事件"""
        # 更新標題和所有界面文本
        self.title_label.config(text=self.lang_manager.get_text("header.title", "電子交接系統"))
        
        # 更新 Notebook 標籤
        self.notebook.tab(0, text=self.lang_manager.get_text("navigation.reports", "報表"))
        self.notebook.tab(1, text=self.lang_manager.get_text("attendance.records", "出勤記錄"))
        self.notebook.tab(2, text=self.lang_manager.get_text("equipment.logs", "設備異常記錄"))
        self.notebook.tab(3, text=self.lang_manager.get_text("lot.logs", "異常批次記錄"))
        self.notebook.tab(4, text=self.lang_manager.get_text("common.summary", "總結"))
        
        # 更新框架標題
        self.info_frame.config(text=self.lang_manager.get_text("common.basicInfo", "基本信息"))
        self.output_frame.config(text=self.lang_manager.get_text("summary.keyOutput", "Key Machine Output"))
        self.issues_frame.config(text=self.lang_manager.get_text("summary.issues", "Key Issues"))
        self.countermeasures_frame.config(text=self.lang_manager.get_text("summary.countermeasures", "Countermeasures"))
        
        # 更新按鈕文本
        self.save_btn.config(text=self.lang_manager.get_text("common.save", "保存"))
        self.add_btn.config(text=self.lang_manager.get_text("common.add", "添加記錄"))
        
        # 更新狀態欄
        lang_names = {"ja": "日本語", "zh": "中文", "en": "English"}
        lang_name = lang_names.get(new_language_code, new_language_code)
        self.status_var.set(f"就緒 - 當前語言: {lang_name}")
    
    def save_daily_report(self):
        """保存日報表"""
        try:
            # 在實際實現中，這會調用後端API
            # 目前顯示確認對話框
            result = messagebox.askyesno(
                "確認",
                f"確定要保存以下報表嗎？\n" +
                f"日期: {self.date_var.get()}\n" +
                f"班別: {self.shift_var.get()}\n" +
                f"區域: {self.area_var.get()}"
            )
            
            if result:
                messagebox.showinfo(
                    "成功",
                    f"報表已保存!\n" +
                    f"日期: {self.date_var.get()}\n" +
                    f"班別: {self.shift_var.get()}\n" +
                    f"區域: {self.area_var.get()}"
                )
        except Exception as e:
            messagebox.showerror("錯誤", f"保存報表時發生錯誤: {str(e)}")
    
    def browse_equipment_image(self):
        """瀏覽設備圖片"""
        # 標記此功能待實現
        messagebox.showinfo("提示", "圖片上傳功能在完整實現中將接入後端API")
    
    def add_equipment_log(self):
        """添加設備異常記錄"""
        # 標記此功能待實現
        messagebox.showinfo("提示", "設備異常記錄將保存到後端數據庫")
    
    def add_lot_log(self):
        """添加異常批次記錄"""
        # 標記此功能待實現
        messagebox.showinfo("提示", "異常批次記錄將保存到後端數據庫")


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