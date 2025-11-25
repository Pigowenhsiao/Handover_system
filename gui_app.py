"""
多語言支持系統 - 圖形用戶界面
基於 Python tkinter 和 SQLite
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import os
from language_manager import AppLanguageManager


class LanguageApp:
    """多語言圖形界面應用程式"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("多語言支持系統")
        self.root.geometry("800x600")
        
        # 初始化語言管理器
        self.lang_manager = AppLanguageManager()
        
        # 設置界面
        self.setup_ui()
        
        # 加載初始語言
        self.update_language_ui()
    
    def setup_ui(self):
        """設置用戶界面"""
        # 創建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # 語言切換下拉菜單
        self.lang_frame = ttk.Frame(self.main_frame)
        self.lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.lang_frame, text="語言/Language/言語:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.lang_var = tk.StringVar()
        self.lang_combo = ttk.Combobox(
            self.lang_frame, 
            textvariable=self.lang_var, 
            values=["ja", "en", "zh"],
            state="readonly",
            width=10
        )
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 標題
        self.title_label = ttk.Label(self.main_frame, text="", font=("TkDefaultFont", 16, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # 主要內容框架
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # 按鈕框架
        self.button_frame = ttk.Frame(self.content_frame)
        self.button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 管理按鈕
        self.manage_btn = ttk.Button(
            self.button_frame, 
            text="", 
            command=self.open_management_window
        )
        self.manage_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 測試按鈕
        self.test_btn = ttk.Button(
            self.button_frame,
            text="",
            command=self.test_translation
        )
        self.test_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 匯入按鈕
        self.import_btn = ttk.Button(
            self.button_frame,
            text="",
            command=self.import_translations
        )
        self.import_btn.pack(side=tk.LEFT)
        
        # 主顯示區域
        self.display_area = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.display_area.yview)
        self.display_area.configure(yscrollcommand=scrollbar.set)
        
        self.display_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # 狀態欄
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def update_language_ui(self):
        """更新界面語言"""
        # 更新標題
        self.title_label.config(text=self.lang_manager.translate("header.title", "多語言支持系統"))
        
        # 更新語言下拉選項（顯示人類可讀的語言名稱）
        current_lang = self.lang_manager.get_current_language()
        self.lang_var.set(current_lang)
        
        # 更新按鈕文本
        self.manage_btn.config(text=self.lang_manager.translate("common.admin", "管理"))
        self.test_btn.config(text=self.lang_manager.translate("common.test", "測試"))
        self.import_btn.config(text=self.lang_manager.translate("common.import", "匯入"))
        
        # 更新狀態欄
        lang_names = {"ja": "日本語", "en": "English", "zh": "中文"}
        current_lang_name = lang_names.get(current_lang, current_lang)
        self.status_var.set(self.lang_manager.translate("common.currentLanguage", f"當前語言: {current_lang_name}"))
        
        # 顯示一些示例文本
        self.display_area.config(state=tk.NORMAL)
        self.display_area.delete(1.0, tk.END)
        
        example_text = f"""
{self.lang_manager.translate('common.title', '系統標題')}:
{self.lang_manager.translate('header.title', '電子交接系統')}

{self.lang_manager.translate('common.language', '語言')}:
{self.lang_manager.translate('common.switchLanguage', '切換語言')}

{self.lang_manager.translate('navigation.home', '首頁')} | 
{self.lang_manager.translate('navigation.reports', '報表')} | 
{self.lang_manager.translate('navigation.settings', '設定')} | 
{self.lang_manager.translate('navigation.admin', '管理')}

{self.lang_manager.translate('common.description', '這是多語言支持系統的示例文本')}
        """
        
        self.display_area.insert(tk.END, example_text.strip())
        self.display_area.config(state=tk.DISABLED)
    
    def on_language_change(self, event=None):
        """語言變化事件處理"""
        new_language = self.lang_var.get()
        if self.lang_manager.change_language(new_language):
            self.update_language_ui()
            self.status_var.set(
                self.lang_manager.translate("common.languageChanged", f"語言已更改為: {new_language}")
            )
    
    def open_management_window(self):
        """打開資源管理窗口"""
        ManagementWindow(self.root, self.lang_manager)
    
    def test_translation(self):
        """測試翻譯功能"""
        # 顯示一個測試對話框
        test_window = tk.Toplevel(self.root)
        test_window.title(self.lang_manager.translate("common.test", "測試"))
        test_window.geometry("400x300")
        
        ttk.Label(
            test_window, 
            text=self.lang_manager.translate("common.testTranslation", "翻譯測試")
        ).pack(pady=10)
        
        # 輸入框
        ttk.Label(test_window, text=self.lang_manager.translate("common.key", "鍵:")).pack()
        key_entry = ttk.Entry(test_window, width=50)
        key_entry.pack(pady=5)
        
        ttk.Label(test_window, text=self.lang_manager.translate("common.defaultValue", "默認值:")).pack()
        default_entry = ttk.Entry(test_window, width=50)
        default_entry.pack(pady=5)
        
        # 結果顯示
        result_var = tk.StringVar()
        result_label = ttk.Label(test_window, textvariable=result_var, wraplength=380)
        result_label.pack(pady=10)
        
        def test_translation():
            key = key_entry.get().strip()
            default_val = default_entry.get().strip()
            if key:
                translation = self.lang_manager.translate(key, default_val)
                result_var.set(f"{self.lang_manager.translate('common.result', '結果')}: {translation}")
            else:
                result_var.set(self.lang_manager.translate("common.pleaseEnterKey", "請輸入鍵"))
        
        ttk.Button(test_window, text=self.lang_manager.translate("common.test", "測試"), command=test_translation).pack(pady=10)
        
        # 示例鍵列表
        examples_frame = ttk.LabelFrame(test_window, text=self.lang_manager.translate("common.examples", "示例"))
        examples_frame.pack(fill=tk.X, padx=10, pady=5)
        
        examples = [
            "common.title",
            "header.title", 
            "navigation.home",
            "not.existing.key"
        ]
        
        for example in examples:
            ttk.Label(examples_frame, text=example).pack(anchor=tk.W)
    
    def import_translations(self):
        """匯入翻譯文件"""
        file_path = filedialog.askopenfilename(
            title=self.lang_manager.translate("common.selectJsonFile", "選擇 JSON 文件"),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 獲取語言代碼（假設從文件名或特殊字段獲取）
                lang_code = os.path.basename(file_path).split('.')[0]
                if lang_code not in ['ja', 'en', 'zh']:
                    lang_code = self.lang_manager.get_current_language()
                
                # 匯入翻譯資源
                self._import_translation_data(data, lang_code, 'common')
                
                messagebox.showinfo(
                    self.lang_manager.translate("common.success", "成功"),
                    self.lang_manager.translate("common.importSuccess", f"成功匯入 {len(data)} 個翻譯資源")
                )
                
                # 重新載入當前語言資源
                self.lang_manager.translation_manager.load_language_resources(
                    self.lang_manager.get_current_language()
                )
                
            except Exception as e:
                messagebox.showerror(
                    self.lang_manager.translate("common.error", "錯誤"),
                    f"{self.lang_manager.translate('common.importError', '匯入錯誤')}: {str(e)}"
                )
    
    def _import_translation_data(self, data, lang_code, namespace, prefix=""):
        """遞歸匯入翻譯數據"""
        resource_manager = self.lang_manager.get_resource_manager()
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                # 如果值是字典，遞歸處理
                self._import_translation_data(value, lang_code, namespace, full_key)
            else:
                # 如果值是字符串，添加到資源管理器
                if isinstance(value, str):
                    resource_manager.add_resource(lang_code, full_key, value, namespace)


class ManagementWindow:
    """語言資源管理窗口"""
    
    def __init__(self, parent, lang_manager):
        self.parent = parent
        self.lang_manager = lang_manager
        self.resource_manager = lang_manager.get_resource_manager()
        
        self.window = tk.Toplevel(parent)
        self.window.title(self.lang_manager.translate("common.resourceManagement", "資源管理"))
        self.window.geometry("900x600")
        
        self.setup_management_ui()
        self.load_resources()
    
    def setup_management_ui(self):
        """設置管理界面"""
        # 主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 控制框架
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 搜索框
        ttk.Label(control_frame, text=self.lang_manager.translate("common.search", "搜索:")).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # 語言過濾
        ttk.Label(control_frame, text=self.lang_manager.translate("common.language", "語言:")).pack(side=tk.LEFT)
        self.filter_lang_var = tk.StringVar(value="")
        lang_combo = ttk.Combobox(
            control_frame,
            textvariable=self.filter_lang_var,
            values=["", "ja", "en", "zh"],
            state="readonly",
            width=7
        )
        lang_combo.pack(side=tk.LEFT, padx=(5, 10))
        lang_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # 命名空間過濾
        ttk.Label(control_frame, text=self.lang_manager.translate("common.namespace", "命名空間:")).pack(side=tk.LEFT)
        self.filter_namespace_var = tk.StringVar(value="")
        namespace_entry = ttk.Entry(control_frame, textvariable=self.filter_namespace_var, width=15)
        namespace_entry.pack(side=tk.LEFT, padx=(5, 10))
        namespace_entry.bind('<KeyRelease>', self.on_filter_change)
        
        # 按鈕框架
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text=self.lang_manager.translate("common.create", "新增"), command=self.add_resource).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text=self.lang_manager.translate("common.refresh", "刷新"), command=self.load_resources).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text=self.lang_manager.translate("common.close", "關閉"), command=self.window.destroy).pack(side=tk.LEFT)
        
        # 表格框架
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 創建表格
        columns = ('ID', 'Language', 'Key', 'Value', 'Namespace')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # 定義表頭
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # 滾動條
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定雙擊事件以編輯資源
        self.tree.bind('<Double-1>', self.edit_resource)
    
    def load_resources(self, search_term="", language_code="", namespace=""):
        """載入資源到表格"""
        # 清除現有項目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 獲取資源
        resources = self.resource_manager.search_resources(search_term, language_code, namespace)
        
        # 添加到表格
        for res in resources:
            self.tree.insert('', tk.END, values=(
                res['id'],
                res['language_code'],
                res['resource_key'],
                res['resource_value'][:50] + "..." if len(res['resource_value']) > 50 else res['resource_value'],  # 截斷長文本
                res['namespace']
            ))
    
    def on_search_change(self, event):
        """搜索變化事件"""
        self.load_resources(
            search_term=self.search_var.get(),
            language_code=self.filter_lang_var.get(),
            namespace=self.filter_namespace_var.get()
        )
    
    def on_filter_change(self, event):
        """過濾變化事件"""
        self.load_resources(
            search_term=self.search_var.get(),
            language_code=self.filter_lang_var.get(),
            namespace=self.filter_namespace_var.get()
        )
    
    def add_resource(self):
        """添加新資源"""
        AddEditResourceWindow(self.window, self.lang_manager, self, new=True)
    
    def edit_resource(self, event):
        """編輯選定資源"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            resource_id = item['values'][0]
            EditResourceWindow(self.window, self.lang_manager, self, resource_id)
    
    def refresh(self):
        """刷新資源列表"""
        self.load_resources(
            search_term=self.search_var.get(),
            language_code=self.filter_lang_var.get(),
            namespace=self.filter_namespace_var.get()
        )


class AddEditResourceWindow:
    """新增/編輯資源窗口"""
    
    def __init__(self, parent, lang_manager, manager_window, new=True, resource_id=None):
        self.parent = parent
        self.lang_manager = lang_manager
        self.manager_window = manager_window
        self.new = new
        self.resource_id = resource_id
        self.resource_manager = lang_manager.get_resource_manager()
        
        self.window = tk.Toplevel(parent)
        title = self.lang_manager.translate("common.createResource", "新增資源") if new else self.lang_manager.translate("common.editResource", "編輯資源")
        self.window.title(title)
        self.window.geometry("500x400")
        
        self.setup_form()
        
        if not new:
            self.load_resource_data()
    
    def setup_form(self):
        """設置表單"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 語言
        ttk.Label(main_frame, text=self.lang_manager.translate("common.language", "語言:")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(main_frame, textvariable=self.lang_var, values=["ja", "en", "zh"], state="readonly")
        lang_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        main_frame.columnconfigure(1, weight=1)
        
        # 鍲名
        ttk.Label(main_frame, text=self.lang_manager.translate("common.key", "鍵:")).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.key_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.key_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # 值
        ttk.Label(main_frame, text=self.lang_manager.translate("common.value", "值:")).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.value_text = tk.Text(main_frame, height=8)
        value_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.value_text.yview)
        self.value_text.configure(yscrollcommand=value_scrollbar.set)
        
        self.value_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        value_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), pady=2)
        
        # 命名空間
        ttk.Label(main_frame, text=self.lang_manager.translate("common.namespace", "命名空間:")).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.namespace_var = tk.StringVar(value="common")
        ttk.Entry(main_frame, textvariable=self.namespace_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # 按鈕框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text=self.lang_manager.translate("common.save", "保存"), command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang_manager.translate("common.cancel", "取消"), command=self.window.destroy).pack(side=tk.LEFT)
    
    def load_resource_data(self):
        """載入資源數據（編輯模式）"""
        if self.resource_id:
            # 從數據庫獲取資源
            conn = sqlite3.connect(self.resource_manager.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT language_code, resource_key, resource_value, namespace FROM language_resources WHERE id = ?",
                (self.resource_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.lang_var.set(result[0])
                self.key_var.set(result[1])
                self.value_text.insert(tk.END, result[2])
                self.namespace_var.set(result[3])
    
    def save(self):
        """保存資源"""
        language_code = self.lang_var.get()
        resource_key = self.key_var.get().strip()
        resource_value = self.value_text.get(1.0, tk.END).strip()
        namespace = self.namespace_var.get().strip() or "common"
        
        if not language_code or not resource_key or not resource_value:
            messagebox.showerror(
                self.lang_manager.translate("common.error", "錯誤"),
                self.lang_manager.translate("common.pleaseFillRequired", "請填寫所有必填字段")
            )
            return
        
        if self.new:
            # 添加新資源
            self.resource_manager.add_resource(language_code, resource_key, resource_value, namespace)
        else:
            # 更新現有資源 - 需要先獲取 ID 並使用 update 方法
            conn = sqlite3.connect(self.resource_manager.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE language_resources 
                SET language_code=?, resource_key=?, resource_value=?, namespace=?, updated_at=CURRENT_TIMESTAMP 
                WHERE id=?
            """, (language_code, resource_key, resource_value, namespace, self.resource_id))
            conn.commit()
            conn.close()
        
        # 更新翻譯緩存
        self.lang_manager.translation_manager.load_language_resources(language_code)
        
        # 通知管理窗口刷新
        self.manager_window.refresh()
        
        # 關閉窗口
        self.window.destroy()


class EditResourceWindow(AddEditResourceWindow):
    """編輯資源窗口（繼承自新增/編輯窗口）"""
    def __init__(self, parent, lang_manager, manager_window, resource_id):
        super().__init__(parent, lang_manager, manager_window, new=False, resource_id=resource_id)


def main():
    """主函數"""
    root = tk.Tk()
    app = LanguageApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()