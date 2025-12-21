"""
現代化主應用程序界面框架
採用側邊導航、卡片式設計、現代色彩方案
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
import pandas as pd

# 導入現有組件
from frontend.src.components.language_selector import LanguageSelector
from frontend.main import LanguageManager
from frontend.src.components.admin_section import UserManagementSection, TranslationManagementSection
from frontend.src.components.attendance_section_optimized import AttendanceSectionOptimized
from models import DelayEntry, SummaryActualEntry, SessionLocal


class ModernMainFrame:
    """
    現代化主應用框架
    採用 Material Design 設計理念
    """
    
    COLORS = {
        'primary': '#1976D2',      # 主色 - 藍色
        'primary_dark': '#1565C0',
        'primary_light': '#E3F2FD',
        'accent': '#FF9800',       # 強調色 - 橙色
        'background': '#FAFAFA',   # 背景色
        'surface': '#FFFFFF',      # 表面色
        'text_primary': '#212121', # 主要文字
        'text_secondary': '#757575', # 次要文字
        'divider': '#E0E0E0',      # 分割線
        'success': '#4CAF50',      # 成功色
        'warning': '#FF9800',      # 警告色
        'error': '#F44336',        # 錯誤色
        'sidebar': '#2C3E50',      # 側邊欄背景
        'sidebar_active': '#3498DB' # 側邊欄激活項
    }
    
    def __init__(self, parent, lang_manager):
        self.parent = parent
        self.lang_manager = lang_manager
        self.current_user = None
        self.sidebar_collapsed = False
        self._global_i18n = []
        self._page_i18n = []
        self._nav_items = []
        self.report_context = {"date": "", "shift": "", "area": ""}
        self.layout = {
            "page_pad": 24,
            "section_pad": 20,
            "card_pad": 20,
            "row_pad": 12,
            "field_gap": 16,
        }
        self.delay_pending_records = []
        self.summary_pending_records = []
        
        # 配置現代化樣式
        self.setup_modern_styles()
        
        # 創建界面
        self.setup_ui()
        
        # 初始化第一個頁面
        self.show_page('daily_report')

    def _t(self, key, default):
        return self.lang_manager.get_text(key, default)

    def _register_text(self, widget, key, default, scope="global"):
        entry = {"widget": widget, "key": key, "default": default}
        if scope == "page":
            self._page_i18n.append(entry)
        else:
            self._global_i18n.append(entry)
        widget.config(text=self._t(key, default))

    def _apply_i18n(self):
        for entry in self._global_i18n + self._page_i18n:
            widget = entry["widget"]
            if widget.winfo_exists():
                widget.config(text=self._t(entry["key"], entry["default"]))

    def _clear_page_i18n(self):
        self._page_i18n = []

    def _set_status(self, key, default):
        self.status_label.config(text=self._t(key, default))

    def _update_auth_ui(self):
        has_nav = hasattr(self, "nav_buttons")
        if self.current_user:
            username = self.current_user.get("username", "")
            role = self.current_user.get("role", "")
            label = self._t("auth.logged_in_as", "👤 {username} ({role})")
            self.user_info_label.config(text=label.format(username=username, role=role))
            self.auth_button.config(text=self._t("header.logout", "登出"))
            if has_nav and "admin" in self.nav_buttons:
                self.nav_buttons["admin"].config(state="normal")
        else:
            self.user_info_label.config(text=self._t("auth.not_logged_in", "未登入"))
            self.auth_button.config(text=self._t("header.login", "登入"))
            if has_nav and "admin" in self.nav_buttons:
                self.nav_buttons["admin"].config(state="disabled")

    def _clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
    
    def setup_modern_styles(self):
        """設置現代化樣式"""
        style = ttk.Style()
        
        # 配置顏色
        colors = self.COLORS
        
        # 框架樣式
        style.configure('Modern.TFrame', background=colors['background'])
        style.configure('Sidebar.TFrame', background=colors['sidebar'])
        style.configure('MainContent.TFrame', background=colors['background'])
        style.configure('Card.TFrame', background=colors['surface'], relief='flat')
        style.configure('Toolbar.TFrame', background=colors['surface'], relief='flat')
        
        # 按鈕樣式
        style.configure('Primary.TButton',
                       background=colors['primary'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Accent.TButton',
                       background=colors['accent'],
                       foreground='white',
                       padding=(10, 6),
                       font=('Segoe UI', 9, 'bold'))
        
        style.configure('Sidebar.TButton',
                       background=colors['sidebar'],
                       foreground='white',
                       padding=(15, 12),
                       font=('Segoe UI', 10),
                       anchor='w')

        style.configure('SidebarActive.TButton',
                       background=colors['sidebar_active'],
                       foreground='white',
                       padding=(15, 12),
                       font=('Segoe UI', 10, 'bold'),
                       anchor='w')
        
        style.map('Sidebar.TButton',
                 background=[('active', colors['sidebar_active']),
                            ('pressed', colors['primary_dark'])],
                 foreground=[('active', 'white')])
        
        # 標籤樣式
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=colors['text_primary'],
                       background=colors['background'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 14),
                       foreground=colors['text_secondary'],
                       background=colors['background'])

        style.configure('Context.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=colors['text_secondary'],
                       background=colors['background'])
        
        style.configure('CardTitle.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=colors['text_primary'],
                       background=colors['surface'])
        
        style.configure('Sidebar.TLabel',
                       font=('Segoe UI', 11),
                       foreground='white',
                       background=colors['sidebar'])
        
        # 筆記本樣式
        style.configure('Modern.TNotebook', background=colors['background'])
        style.configure('Modern.TNotebook.Tab',
                       font=('Segoe UI', 10),
                       padding=(15, 8),
                       background=colors['surface'])
        
        # 輸入框樣式
        style.configure('Modern.TEntry',
                       fieldbackground=colors['surface'],
                       font=('Segoe UI', 10),
                       padding=(8, 5))
        
        # 進度條樣式
        style.configure('Horizontal.TProgressbar',
                       background=colors['primary'],
                       troughcolor=colors['background'],
                       thickness=8)
        
        # 分隔線樣式
        style.configure('Line.TSeparator', background=colors['divider'])
    
    def setup_ui(self):
        """設置現代化界面"""
        # 主容器
        self.main_container = ttk.Frame(self.parent, style='Modern.TFrame')
        self.main_container.pack(fill='both', expand=True)
        
        # 創建頂部工具欄
        self.create_top_toolbar()
        
        # 創建側邊導航欄
        self.create_sidebar()
        self._update_auth_ui()
        
        # 創建主內容區域
        self.create_main_content()
        
        # 創建狀態欄
        self.create_status_bar()
    
    def create_top_toolbar(self):
        """創建頂部工具欄"""
        toolbar = ttk.Frame(self.main_container, height=60, style='Toolbar.TFrame')
        toolbar.pack(fill='x', padx=0, pady=0)
        toolbar.pack_propagate(False)
        
        # Logo/標題容器
        title_container = ttk.Frame(toolbar, style='Toolbar.TFrame')
        title_container.pack(side='left', padx=20)
        
        # 主標題
        self.main_title = ttk.Label(
            title_container,
            font=('Segoe UI', 18, 'bold'),
            foreground=self.COLORS['primary'],
            background=self.COLORS['surface']
        )
        self._register_text(self.main_title, "header.title", "電子交接系統")
        self.main_title.pack(side='left')
        
        # 副標題
        self.subtitle = ttk.Label(
            title_container,
            font=('Segoe UI', 9),
            foreground=self.COLORS['text_secondary'],
            background=self.COLORS['surface']
        )
        self._register_text(self.subtitle, "header.subtitle", "Handover Management System")
        self.subtitle.pack(side='left', padx=(10, 0))
        
        # 右側工具區
        tool_container = ttk.Frame(toolbar, style='Toolbar.TFrame')
        tool_container.pack(side='right', padx=20)
        
        # 使用者資訊
        self.user_info_label = ttk.Label(
            tool_container,
            font=('Segoe UI', 10),
            foreground=self.COLORS['text_secondary'],
            background=self.COLORS['surface']
        )
        self.user_info_label.pack(side='left', padx=(0, 15))
        
        # 語言選擇器
        self.lang_selector = LanguageSelector(
            tool_container,
            self.lang_manager,
            callback=self.on_language_changed
        )
        self.lang_selector.get_widget().pack(side='left', padx=(0, 10))
        
        # 登出/登入按鈕
        self.auth_button = ttk.Button(
            tool_container,
            style='Accent.TButton',
            command=self.toggle_auth,
            width=12
        )
        self.auth_button.pack(side='left')
        self._update_auth_ui()
    
    def create_sidebar(self):
        """創建側邊導航欄"""
        self.sidebar_frame = ttk.Frame(self.main_container, width=220, style='Sidebar.TFrame')
        self.sidebar_frame.pack(side='left', fill='y', padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)
        
        # 側邊欄標題
        sidebar_title = ttk.Label(
            self.sidebar_frame,
            font=('Segoe UI', 12, 'bold'),
            foreground='white',
            background=self.COLORS['sidebar']
        )
        self._register_text(sidebar_title, "navigation.menuTitle", "導航選單")
        sidebar_title.pack(pady=(20, 10), padx=20, anchor='w')
        
        # 導航按鈕
        self.nav_buttons = {}
        
        self._nav_items = [
            ('daily_report', '📋', "navigation.dailyReport", "日報表"),
            ('attendance', '👥', "navigation.attendance", "出勤記錄"),
            ('equipment', '⚙️', "navigation.equipment", "設備異常"),
            ('lot', '📦', "navigation.lot", "異常批次"),
            ('summary', '📊', "navigation.summary", "總結"),
            ('delay_list', '⏱️', "navigation.delayList", "延遲清單"),
            ('summary_actual', '🧾', "navigation.summaryActual", "Summary Actual"),
            ('admin', '⚙️', "navigation.admin", "系統管理")
        ]

        for item_id, icon, text_key, text_default in self._nav_items:
            btn = ttk.Button(
                self.sidebar_frame,
                text=f"{icon} {self._t(text_key, text_default)}",
                style='Sidebar.TButton',
                command=lambda page=item_id: self.show_page(page),
                width=20
            )
            btn.pack(fill='x', padx=10, pady=2)
            self.nav_buttons[item_id] = btn
            
            # 添加懸停效果提示
            self.add_tooltip(btn, text_key, text_default)
        
        # 側邊欄底部資訊
        separator = ttk.Separator(self.sidebar_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=(20, 10))
        
        version_label = ttk.Label(
            self.sidebar_frame,
            font=('Segoe UI', 8),
            foreground='white',
            background=self.COLORS['sidebar']
        )
        self._register_text(version_label, "header.version", "Version 2.0")
        version_label.pack(side='bottom', pady=(0, 10), padx=20, anchor='w')
        
        # 收合/展開按鈕
        self.toggle_sidebar_btn = ttk.Button(
            self.sidebar_frame,
            text="◀",
            width=3,
            command=self.toggle_sidebar
        )
        self._position_sidebar_toggle()
    
    def create_main_content(self):
        """創建主內容區域"""
        # 內容容器
        self.content_container = ttk.Frame(self.main_container, style='MainContent.TFrame')
        self.content_container.pack(side='left', fill='both', expand=True, padx=0, pady=0)
        
        # 內容區域（使用 Card 設計）
        self.content_frame = ttk.Frame(self.content_container, style='Modern.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=self.layout["page_pad"], pady=self.layout["page_pad"])
        
        # 頁面標題
        self.page_header = ttk.Frame(self.content_frame, style='Modern.TFrame')
        self.page_header.pack(fill='x', pady=(0, 20))
        
        self.page_title = ttk.Label(
            self.page_header,
            text="",
            style='Title.TLabel'
        )
        self.page_title.pack(side='left')
        
        self.page_subtitle = ttk.Label(
            self.page_header,
            text="",
            style='Subtitle.TLabel'
        )
        self.page_subtitle.pack(side='left', padx=(10, 0))

        self.context_label = ttk.Label(
            self.page_header,
            text="",
            style='Context.TLabel'
        )
        self.context_label.pack(side='right')
        
        # 分隔線
        separator = ttk.Separator(self.content_frame, orient='horizontal', style='Line.TSeparator')
        separator.pack(fill='x', pady=(0, 20))
        
        # 內容區（動態載入）
        self.page_content = ttk.Frame(self.content_frame, style='Modern.TFrame')
        self.page_content.pack(fill='both', expand=True)
        
        # 初始化各個頁面
        self.pages = {}
        self.current_page = None
    
    def create_status_bar(self):
        """創建狀態欄"""
        self.status_frame = ttk.Frame(self.main_container, height=30, style='Toolbar.TFrame')
        self.status_frame.pack(side='bottom', fill='x', pady=0)
        self.status_frame.pack_propagate(False)
        
        self.status_label = ttk.Label(
            self.status_frame,
            font=('Segoe UI', 9),
            foreground=self.COLORS['text_secondary'],
            background=self.COLORS['surface']
        )
        self.status_label.pack(side='left', padx=20)
        self._set_status("status.ready", "就緒")
        
        # 狀態指示器
        self.status_indicator = tk.Canvas(self.status_frame, width=12, height=12, highlightthickness=0)
        self.status_indicator.create_oval(1, 1, 11, 11, fill=self.COLORS['success'], outline="")
        self.status_indicator.pack(side='right', padx=20)
    
    def show_page(self, page_id):
        """顯示指定頁面"""
        # 清除現有內容
        for widget in self.page_content.winfo_children():
            widget.destroy()
        self._clear_page_i18n()
        
        # 更新導航按鈕狀態
        self.update_nav_buttons(page_id)
        
        # 根據頁面ID創建內容
        if page_id == 'daily_report':
            self.create_daily_report_page()
        elif page_id == 'attendance':
            self.create_attendance_page()
        elif page_id == 'equipment':
            self.create_equipment_page()
        elif page_id == 'lot':
            self.create_lot_page()
        elif page_id == 'summary':
            self.create_summary_page()
        elif page_id == 'delay_list':
            self.create_delay_list_page()
        elif page_id == 'summary_actual':
            self.create_summary_actual_page()
        elif page_id == 'admin':
            self.create_admin_page()
        
        self.current_page = page_id
        self._update_report_context_label()
    
    def update_nav_buttons(self, active_page):
        """更新導航按鈕狀態"""
        for page_id, button in self.nav_buttons.items():
            if page_id == active_page:
                button.state(['pressed'])
                # 突出顯示活動按鈕
                button.configure(style='SidebarActive.TButton')
            else:
                button.state(['!pressed'])
                button.configure(style='Sidebar.TButton')
    
    def create_daily_report_page(self):
        """創建日報表頁面"""
        self._register_text(self.page_title, "pages.dailyReport.title", "日報表", scope="page")
        self._register_text(self.page_subtitle, "pages.dailyReport.subtitle", "記錄每日生產交接資訊", scope="page")
        
        # 日期與班別卡片
        date_card = self.create_card(self.page_content, '📅', "cards.dateShift", "日期與班別資訊")
        date_card.pack(fill='x', padx=0, pady=(0, 20))
        
        # 表單布局
        form_frame = ttk.Frame(date_card, style='Card.TFrame')
        form_frame.pack(fill='x', padx=self.layout["card_pad"], pady=self.layout["card_pad"])
        
        # 日期
        self.create_form_row(
            form_frame, 0,
            "fields.date", "📅 日期:",
            'date',
            widget_type='entry',
            var_name='date_var',
            default=datetime.now().strftime("%Y-%m-%d")
        )
        
        # 班別
        shift_values = [
            self._t("shift.day", "Day"),
            self._t("shift.night", "Night"),
        ]
        self.shift_values = shift_values
        self.shift_combo = self.create_form_row(
            form_frame, 1,
            "fields.shift", "⏰ 班別:",
            'shift',
            widget_type='combo',
            var_name='shift_var',
            values=shift_values,
            default=shift_values[0]
        )
        
        # 區域
        self.create_form_row(
            form_frame, 2,
            "fields.area", "🏭 區域:",
            'area',
            widget_type='combo',
            var_name='area_var',
            values=["etching_D", "etching_E", "litho", "thin_film"],
            default="etching_D"
        )

        self.date_var.trace_add("write", lambda *_: self._sync_report_context_from_form())
        self.shift_var.trace_add("write", lambda *_: self._sync_report_context_from_form())
        self.area_var.trace_add("write", lambda *_: self._sync_report_context_from_form())
        self._sync_report_context_from_form()
        
        # 基本信息卡片
        basic_card = self.create_card(self.page_content, '📝', "cards.basicSummary", "基本資訊與摘要")
        basic_card.pack(fill='both', expand=True, padx=0, pady=(0, 20))
        
        # Key Machine Output
        key_output_label = ttk.Label(basic_card, style='CardTitle.TLabel')
        self._register_text(key_output_label, "summary.keyOutput", "🔑 Key Machine Output:", scope="page")
        key_output_label.pack(anchor='w', padx=self.layout["card_pad"], pady=(20, 5))
        self.key_output_text = tk.Text(basic_card, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.key_output_text.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 15))
        
        # Key Issues
        key_issues_label = ttk.Label(basic_card, style='CardTitle.TLabel')
        self._register_text(key_issues_label, "summary.issues", "⚠️ Key Issues:", scope="page")
        key_issues_label.pack(anchor='w', padx=self.layout["card_pad"], pady=(15, 5))
        self.key_issues_text = tk.Text(basic_card, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.key_issues_text.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 15))
        
        # Countermeasures
        counter_label = ttk.Label(basic_card, style='CardTitle.TLabel')
        self._register_text(counter_label, "summary.countermeasures", "✅ Countermeasures:", scope="page")
        counter_label.pack(anchor='w', padx=self.layout["card_pad"], pady=(15, 5))
        self.countermeasures_text = tk.Text(basic_card, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.countermeasures_text.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 20))
        
        # 操作按鈕
        button_frame = ttk.Frame(basic_card, style='Card.TFrame')
        button_frame.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 20))
        
        save_btn = ttk.Button(button_frame, style='Primary.TButton', command=self.save_daily_report)
        self._register_text(save_btn, "actions.saveDailyReport", "💾 儲存日報", scope="page")
        save_btn.pack(side='left')
        reset_btn = ttk.Button(button_frame, style='Accent.TButton', command=self.reset_daily_report)
        self._register_text(reset_btn, "actions.resetDailyReport", "🔄 重置", scope="page")
        reset_btn.pack(side='left', padx=(10, 0))
    
    def create_card(self, parent, emoji, title_key, title_default):
        """創建卡片容器"""
        card = ttk.Frame(parent, style='Card.TFrame')
        
        # 卡片標題
        title_frame = ttk.Frame(card, style='Card.TFrame')
        title_frame.pack(fill='x', padx=20, pady=(15, 0))
        
        title_label = ttk.Label(title_frame, style='CardTitle.TLabel')
        self._register_text(title_label, title_key, f"{emoji} {title_default}", scope="page")
        title_label.pack(side='left')
        
        # 分隔線
        sep = ttk.Separator(card, orient='horizontal', style='Line.TSeparator')
        sep.pack(fill='x', padx=20, pady=(10, 0))
        
        # 記錄卡片以便後續引用
        setattr(self, f"{title_default.lower().replace(' ', '_').replace('/', '_')}_card", card)
        
        return card
    
    def create_form_row(self, parent, row, label_key, label_default, field_name, widget_type='entry', **kwargs):
        """創建表單行"""
        label = ttk.Label(parent, font=('Segoe UI', 10))
        self._register_text(label, label_key, label_default, scope="page")
        label.grid(row=row, column=0, sticky='w', padx=0, pady=self.layout["row_pad"])
        
        widget = None
        if widget_type == 'entry':
            var = tk.StringVar(value=kwargs.get('default', ''))
            setattr(self, kwargs['var_name'], var)
            widget = ttk.Entry(parent, textvariable=var, style='Modern.TEntry', width=30)
            widget.grid(row=row, column=1, sticky='ew', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"])
        elif widget_type == 'combo':
            var = tk.StringVar(value=kwargs.get('default', ''))
            setattr(self, kwargs['var_name'], var)
            widget = ttk.Combobox(
                parent,
                textvariable=var,
                values=kwargs['values'],
                state='readonly',
                font=('Segoe UI', 10),
                width=28
            )
            widget.grid(row=row, column=1, sticky='ew', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"])
        parent.columnconfigure(1, weight=1)
        return widget
    
    def create_attendance_page(self):
        """創建出勤記錄頁面"""
        self._register_text(self.page_title, "pages.attendance.title", "出勤記錄", scope="page")
        self._register_text(self.page_subtitle, "pages.attendance.subtitle", "記錄正社員與契約社員出勤資訊", scope="page")
        
        # 使用優化版出勤組件
        self.attendance_section = AttendanceSectionOptimized(self.page_content, self.lang_manager, self)
        self.attendance_section.get_widget().pack(fill='both', expand=True)
    
    def create_equipment_page(self):
        """創建設備異常頁面"""
        self._register_text(self.page_title, "pages.equipment.title", "設備異常", scope="page")
        self._register_text(self.page_subtitle, "pages.equipment.subtitle", "記錄設備異常與處理資訊", scope="page")
        
        card = self.create_card(self.page_content, '⚙️', "cards.equipmentRecord", "設備異常記錄")
        card.pack(fill='both', expand=True)
        
        # 表單
        form_frame = ttk.Frame(card, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, padx=self.layout["card_pad"], pady=self.layout["card_pad"])
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # 設備號碼
        equip_id_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(equip_id_label, "equipment.equipId", "設備號碼:", scope="page")
        equip_id_label.grid(row=0, column=0, sticky='w', pady=self.layout["row_pad"])
        self.equip_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.equip_id_var, style='Modern.TEntry').grid(
            row=0, column=1, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"]
        )
        
        # 發生時刻
        start_time_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(start_time_label, "equipment.startTime", "發生時刻:", scope="page")
        start_time_label.grid(row=0, column=2, sticky='w', pady=self.layout["row_pad"])
        self.start_time_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.start_time_var, style='Modern.TEntry').grid(
            row=0, column=3, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"]
        )
        
        # 影響數量
        impact_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(impact_label, "equipment.impactQty", "影響數量:", scope="page")
        impact_label.grid(row=1, column=0, sticky='w', pady=self.layout["row_pad"])
        self.impact_qty_var = tk.StringVar(value='0')
        ttk.Entry(form_frame, textvariable=self.impact_qty_var, style='Modern.TEntry').grid(
            row=1, column=1, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"]
        )
        
        # 異常內容
        desc_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(desc_label, "common.description", "異常內容:", scope="page")
        desc_label.grid(row=2, column=0, sticky='w', pady=self.layout["row_pad"])
        self.equip_desc_text = tk.Text(form_frame, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.equip_desc_text.grid(row=2, column=1, columnspan=3, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"])
        
        # 對應內容
        action_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(action_label, "equipment.actionTaken", "對應內容:", scope="page")
        action_label.grid(row=3, column=0, sticky='w', pady=self.layout["row_pad"])
        self.action_text = tk.Text(form_frame, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.action_text.grid(row=3, column=1, columnspan=3, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"])
        
        # 圖片上傳
        image_frame = ttk.Frame(form_frame, style='Card.TFrame')
        image_frame.grid(row=4, column=0, columnspan=4, sticky='ew', padx=0, pady=self.layout["row_pad"])
        image_frame.columnconfigure(1, weight=1)
        
        image_label = ttk.Label(image_frame, font=('Segoe UI', 10))
        self._register_text(image_label, "common.image", "異常圖片:", scope="page")
        image_label.pack(side='left')
        self.image_path_var = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.image_path_var, state='readonly', style='Modern.TEntry').pack(side='left', padx=self.layout["field_gap"], fill='x', expand=True)
        browse_btn = ttk.Button(image_frame, style='Accent.TButton', command=self.browse_image)
        self._register_text(browse_btn, "common.browse", "瀏覽...", scope="page")
        browse_btn.pack(side='left')
        
        # 按鈕
        button_frame = ttk.Frame(card, style='Card.TFrame')
        button_frame.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 20))
        
        add_btn = ttk.Button(button_frame, style='Primary.TButton', command=self.add_equipment_record)
        self._register_text(add_btn, "actions.addEquipment", "➕ 添加記錄", scope="page")
        add_btn.pack(side='left')
        history_btn = ttk.Button(button_frame, style='Accent.TButton', command=self.view_equipment_history)
        self._register_text(history_btn, "actions.viewEquipmentHistory", "📋 查看歷史", scope="page")
        history_btn.pack(side='left', padx=10)
    
    def create_lot_page(self):
        """創建異常批次頁面"""
        self._register_text(self.page_title, "pages.lot.title", "異常批次", scope="page")
        self._register_text(self.page_subtitle, "pages.lot.subtitle", "記錄批次異常與處置狀況", scope="page")
        
        card = self.create_card(self.page_content, '📦', "cards.lotRecord", "異常批次記錄")
        card.pack(fill='both', expand=True)
        
        form_frame = ttk.Frame(card, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, padx=self.layout["card_pad"], pady=self.layout["card_pad"])
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # 批號
        lot_id_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(lot_id_label, "lot.lotId", "批號:", scope="page")
        lot_id_label.grid(row=0, column=0, sticky='w', pady=self.layout["row_pad"])
        self.lot_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.lot_id_var, style='Modern.TEntry').grid(
            row=0, column=1, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"]
        )
        
        # 異常內容
        lot_desc_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(lot_desc_label, "common.description", "異常內容:", scope="page")
        lot_desc_label.grid(row=1, column=0, sticky='w', pady=self.layout["row_pad"])
        self.lot_desc_text = tk.Text(form_frame, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.lot_desc_text.grid(row=1, column=1, columnspan=3, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"])
        
        # 處置狀況
        status_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(status_label, "lot.status", "處置狀況:", scope="page")
        status_label.grid(row=2, column=0, sticky='w', pady=self.layout["row_pad"])
        self.lot_status_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.lot_status_var, style='Modern.TEntry').grid(
            row=2, column=1, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"]
        )
        
        # 特記事項
        notes_label = ttk.Label(form_frame, font=('Segoe UI', 10))
        self._register_text(notes_label, "lot.notes", "特記事項:", scope="page")
        notes_label.grid(row=3, column=0, sticky='w', pady=self.layout["row_pad"])
        self.lot_notes_text = tk.Text(form_frame, height=4, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.lot_notes_text.grid(row=3, column=1, columnspan=3, sticky='ew', padx=self.layout["field_gap"], pady=self.layout["row_pad"])
        
        # 按鈕
        button_frame = ttk.Frame(card, style='Card.TFrame')
        button_frame.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 20))
        
        add_btn = ttk.Button(button_frame, style='Primary.TButton', command=self.add_lot_record)
        self._register_text(add_btn, "actions.addLot", "➕ 添加批次", scope="page")
        add_btn.pack(side='left')
        list_btn = ttk.Button(button_frame, style='Accent.TButton', command=self.view_lot_list)
        self._register_text(list_btn, "actions.viewLotList", "📋 批次列表", scope="page")
        list_btn.pack(side='left', padx=10)
    
    def create_summary_page(self):
        """創建總結頁面"""
        self._register_text(self.page_title, "pages.summary.title", "總結", scope="page")
        self._register_text(self.page_subtitle, "pages.summary.subtitle", "記錄每日總結與分析", scope="page")
        
        card = self.create_card(self.page_content, '📊', "cards.workSummary", "工作總結")
        card.pack(fill='both', expand=True)
        
        # Key Issues
        issues_label = ttk.Label(card, style='CardTitle.TLabel')
        self._register_text(issues_label, "summary.issues", "⚠️ Key Issues (關鍵問題):", scope="page")
        issues_label.pack(anchor='w', padx=self.layout["card_pad"], pady=(20, 5))
        self.summary_key_issues_text = tk.Text(card, height=6, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.summary_key_issues_text.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 15))
        
        # Countermeasures
        counter_label = ttk.Label(card, style='CardTitle.TLabel')
        self._register_text(counter_label, "summary.countermeasures", "✅ Countermeasures (對策):", scope="page")
        counter_label.pack(anchor='w', padx=self.layout["card_pad"], pady=(15, 5))
        self.summary_countermeasures_text = tk.Text(card, height=6, font=('Segoe UI', 10), relief='flat', bg=self.COLORS['surface'], wrap="word")
        self.summary_countermeasures_text.pack(fill='x', padx=self.layout["card_pad"], pady=(0, 20))
        
        # 統計資訊卡片
        stats_card = self.create_card(self.page_content, '📈', "cards.statsToday", "今日統計")
        stats_card.pack(fill='x')
        
        stats_frame = ttk.Frame(stats_card, style='Card.TFrame')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # 今日報表數、出勤率等統計
        stat_items = [
            ('📋', "stats.dailyReports", "今日報表", '5', "stats.unitReports", "份"),
            ('👥', "stats.avgAttendance", "平均出勤率", '92.5', "stats.unitPercent", '%'),
            ('⚠️', "stats.equipmentIssues", "設備異常", '3', "stats.unitItems", '件'),
            ('📦', "stats.lotIssues", "批次異常", '1', "stats.unitItems", '件')
        ]
        
        for i, (emoji, label_key, label_default, value, unit_key, unit_default) in enumerate(stat_items):
            frame = ttk.Frame(stats_frame, style='Card.TFrame')
            frame.grid(row=0, column=i, padx=10, pady=0)
            
            ttk.Label(frame, text=emoji, font=('Segoe UI', 24)).pack()
            label_widget = ttk.Label(frame, font=('Segoe UI', 10), foreground=self.COLORS['text_secondary'])
            self._register_text(label_widget, label_key, label_default, scope="page")
            label_widget.pack()
            ttk.Label(frame, text=value, font=('Segoe UI', 18, 'bold'), foreground=self.COLORS['primary']).pack()
            unit_widget = ttk.Label(frame, font=('Segoe UI', 9), foreground=self.COLORS['text_secondary'])
            self._register_text(unit_widget, unit_key, unit_default, scope="page")
            unit_widget.pack()

    def create_delay_list_page(self):
        """創建延遲清單頁面"""
        self._register_text(self.page_title, "pages.delayList.title", "延遲清單", scope="page")
        self._register_text(self.page_subtitle, "pages.delayList.subtitle", "延遲清單匯入與查詢", scope="page")

        control_card = self.create_card(self.page_content, '⏱️', "cards.delayList", "延遲清單")
        control_card.pack(fill='x', padx=0, pady=(0, 20))

        control_frame = ttk.Frame(control_card, style='Card.TFrame')
        control_frame.pack(fill='x', padx=self.layout["card_pad"], pady=self.layout["card_pad"])

        start_label = ttk.Label(control_frame, font=('Segoe UI', 10))
        self._register_text(start_label, "delay.startDate", "起日 YYYY-MM-DD", scope="page")
        start_label.grid(row=0, column=0, sticky='w', pady=self.layout["row_pad"])
        self.delay_start_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.delay_start_var, style='Modern.TEntry', width=16).grid(
            row=0, column=1, sticky='w', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"]
        )

        end_label = ttk.Label(control_frame, font=('Segoe UI', 10))
        self._register_text(end_label, "delay.endDate", "迄日 YYYY-MM-DD", scope="page")
        end_label.grid(row=0, column=2, sticky='w', padx=(20, 0), pady=self.layout["row_pad"])
        self.delay_end_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.delay_end_var, style='Modern.TEntry', width=16).grid(
            row=0, column=3, sticky='w', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"]
        )
        self._apply_report_date_to_filters()

        search_btn = ttk.Button(control_frame, style='Accent.TButton', command=self._load_delay_entries)
        self._register_text(search_btn, "common.search", "搜尋", scope="page")
        search_btn.grid(row=0, column=4, padx=(20, 0), pady=self.layout["row_pad"])

        import_btn = ttk.Button(control_frame, style='Accent.TButton', command=self._import_delay_excel)
        self._register_text(import_btn, "delay.importExcel", "匯入延遲Excel", scope="page")
        import_btn.grid(row=1, column=0, pady=self.layout["row_pad"])

        upload_btn = ttk.Button(control_frame, style='Primary.TButton', command=self._upload_delay_pending)
        self._register_text(upload_btn, "delay.confirmUpload", "確認上傳", scope="page")
        upload_btn.grid(row=1, column=1, padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"])

        refresh_btn = ttk.Button(control_frame, style='Accent.TButton', command=self._load_delay_entries)
        self._register_text(refresh_btn, "delay.refresh", "重新整理", scope="page")
        refresh_btn.grid(row=1, column=2, padx=(20, 0), pady=self.layout["row_pad"])

        clear_btn = ttk.Button(
            control_frame,
            style='Accent.TButton',
            command=lambda: self._clear_delay_view(),
        )
        self._register_text(clear_btn, "delay.clear", "清除畫面", scope="page")
        clear_btn.grid(row=1, column=3, padx=(20, 0), pady=self.layout["row_pad"])

        table_card = self.create_card(self.page_content, '📋', "cards.delayListTable", "延遲清單資料")
        table_card.pack(fill='both', expand=True)

        table_frame = ttk.Frame(table_card, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True, padx=self.layout["card_pad"], pady=self.layout["card_pad"])

        cols = (
            "id",
            "date",
            "time",
            "reactor",
            "process",
            "lot",
            "wafer",
            "progress",
            "prev_steps",
            "prev_time",
            "severity",
            "action",
            "note",
        )
        self.delay_columns = cols
        self.delay_header_keys = [
            ("common.id", "ID"),
            ("delay.date", "日期"),
            ("delay.time", "時間"),
            ("delay.reactor", "設備"),
            ("delay.process", "製程"),
            ("delay.lot", "批號"),
            ("delay.wafer", "晶圓"),
            ("delay.progress", "進行中"),
            ("delay.prevSteps", "前站"),
            ("delay.prevTime", "前站時間"),
            ("delay.severity", "嚴重度"),
            ("delay.action", "對應內容"),
            ("delay.note", "備註"),
        ]

        self.delay_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)
        self._update_delay_headers()
        self.delay_tree.pack(side='left', fill='both', expand=True)
        delay_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.delay_tree.yview)
        self.delay_tree.configure(yscrollcommand=delay_scroll.set)
        delay_scroll.pack(side="right", fill="y")
        self.delay_tree.bind("<Double-1>", lambda e: self._edit_delay_dialog())

        self._load_delay_entries()

    def create_summary_actual_page(self):
        """創建 Summary Actual 頁面"""
        self._register_text(self.page_title, "pages.summaryActual.title", "Summary Actual", scope="page")
        self._register_text(self.page_subtitle, "pages.summaryActual.subtitle", "Summary Actual 匯入與查詢", scope="page")

        control_card = self.create_card(self.page_content, '🧾', "cards.summaryActual", "Summary Actual")
        control_card.pack(fill='x', padx=0, pady=(0, 20))

        control_frame = ttk.Frame(control_card, style='Card.TFrame')
        control_frame.pack(fill='x', padx=self.layout["card_pad"], pady=self.layout["card_pad"])

        start_label = ttk.Label(control_frame, font=('Segoe UI', 10))
        self._register_text(start_label, "summaryActual.startDate", "日期篩選起日 YYYY-MM-DD", scope="page")
        start_label.grid(row=0, column=0, sticky='w', pady=self.layout["row_pad"])
        self.summary_start_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.summary_start_var, style='Modern.TEntry', width=16).grid(
            row=0, column=1, sticky='w', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"]
        )

        end_label = ttk.Label(control_frame, font=('Segoe UI', 10))
        self._register_text(end_label, "summaryActual.endDate", "日期篩選迄日 YYYY-MM-DD", scope="page")
        end_label.grid(row=0, column=2, sticky='w', padx=(20, 0), pady=self.layout["row_pad"])
        self.summary_end_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.summary_end_var, style='Modern.TEntry', width=16).grid(
            row=0, column=3, sticky='w', padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"]
        )
        self._apply_report_date_to_filters()

        search_btn = ttk.Button(control_frame, style='Accent.TButton', command=self._load_summary_actual)
        self._register_text(search_btn, "common.search", "搜尋", scope="page")
        search_btn.grid(row=0, column=4, padx=(20, 0), pady=self.layout["row_pad"])

        import_btn = ttk.Button(control_frame, style='Accent.TButton', command=self._import_summary_actual_excel)
        self._register_text(import_btn, "summaryActual.importExcel", "匯入 Summary Actual", scope="page")
        import_btn.grid(row=1, column=0, pady=self.layout["row_pad"])

        upload_btn = ttk.Button(control_frame, style='Primary.TButton', command=self._upload_summary_pending)
        self._register_text(upload_btn, "summaryActual.confirmUpload", "確認上傳", scope="page")
        upload_btn.grid(row=1, column=1, padx=(self.layout["field_gap"], 0), pady=self.layout["row_pad"])

        clear_btn = ttk.Button(
            control_frame,
            style='Accent.TButton',
            command=self._clear_summary_view,
        )
        self._register_text(clear_btn, "summaryActual.clear", "清除畫面", scope="page")
        clear_btn.grid(row=1, column=2, padx=(20, 0), pady=self.layout["row_pad"])

        table_card = self.create_card(self.page_content, '📋', "cards.summaryActualTable", "Summary Actual 資料")
        table_card.pack(fill='both', expand=True)

        table_frame = ttk.Frame(table_card, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True, padx=self.layout["card_pad"], pady=self.layout["card_pad"])

        cols = (
            "id",
            "date",
            "label",
            "plan",
            "completed",
            "in_process",
            "on_track",
            "at_risk",
            "delayed",
            "no_data",
            "scrapped",
        )
        self.summary_columns = cols
        self.summary_header_keys = [
            ("common.id", "ID"),
            ("summaryActual.date", "日期"),
            ("summaryActual.label", "標籤"),
            ("summaryActual.plan", "Plan"),
            ("summaryActual.completed", "Completed"),
            ("summaryActual.inProcess", "In Process"),
            ("summaryActual.onTrack", "On Track"),
            ("summaryActual.atRisk", "At Risk"),
            ("summaryActual.delayed", "Delayed"),
            ("summaryActual.noData", "No Data"),
            ("summaryActual.scrapped", "Scrapped"),
        ]

        self.summary_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)
        self._update_summary_headers()
        self.summary_tree.pack(side='left', fill='both', expand=True)
        summary_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=summary_scroll.set)
        summary_scroll.pack(side="right", fill="y")
        self.summary_tree.bind("<Double-1>", lambda e: self._edit_summary_dialog())

        self._load_summary_actual()
    
    def create_admin_page(self):
        """創建管理員頁面"""
        self._register_text(self.page_title, "pages.admin.title", "系統管理", scope="page")
        self._register_text(self.page_subtitle, "pages.admin.subtitle", "管理使用者、翻譯資源與系統設定", scope="page")
        
        # 創建 Notebook 分頁
        self.admin_notebook = ttk.Notebook(self.page_content, style='Modern.TNotebook')
        self.admin_notebook.pack(fill='both', expand=True)
        
        # 使用者管理分頁
        user_tab = ttk.Frame(admin_notebook, style='Modern.TFrame')
        self.admin_notebook.add(user_tab, text=self._t("admin.tabUsers", "👥 使用者管理"))
        
        self.admin_user_mgmt = UserManagementSection(user_tab, self.lang_manager)
        self.admin_user_mgmt.get_widget().pack(fill='both', expand=True, padx=20, pady=20)
        
        # 翻譯管理分頁
        translation_tab = ttk.Frame(admin_notebook, style='Modern.TFrame')
        self.admin_notebook.add(translation_tab, text=self._t("admin.tabTranslations", "🌐 翻譯管理"))
        
        self.admin_trans_mgmt = TranslationManagementSection(translation_tab, self.lang_manager)
        self.admin_trans_mgmt.get_widget().pack(fill='both', expand=True, padx=20, pady=20)
        
        # 系統設定分頁
        settings_tab = ttk.Frame(admin_notebook, style='Modern.TFrame')
        self.admin_notebook.add(settings_tab, text=self._t("admin.tabSettings", "⚙️ 系統設定"))
        
        self.create_settings_page(settings_tab)
    
    def create_settings_page(self, parent):
        """創建設定頁面"""
        # 資料庫設定
        db_card = self.create_card(parent, '🗄️', "cards.databaseSettings", "資料庫設定")
        db_card.pack(fill='x', padx=20, pady=(20, 10))
        
        db_path_label = ttk.Label(db_card, font=('Segoe UI', 10))
        self._register_text(db_path_label, "settings.databasePath", "資料庫路徑:", scope="page")
        db_path_label.pack(anchor='w', padx=20, pady=(15, 5))
        db_path_frame = ttk.Frame(db_card, style='Card.TFrame')
        db_path_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        self.db_path_var = tk.StringVar(value='handover_system.db')
        ttk.Entry(db_path_frame, textvariable=self.db_path_var, width=50, state='readonly', style='Modern.TEntry').pack(side='left', padx=(0, 10))
        browse_btn = ttk.Button(db_path_frame, style='Accent.TButton')
        self._register_text(browse_btn, "common.browse", "瀏覽...", scope="page")
        browse_btn.pack(side='left')
        
        # 系統設定
        system_card = self.create_card(parent, '⚙️', "cards.systemSettings", "系統設定")
        system_card.pack(fill='x', padx=20, pady=(0, 20))
        
        # 自動備份
        backup_frame = ttk.Frame(system_card, style='Card.TFrame')
        backup_frame.pack(fill='x', padx=20, pady=15)
        
        self.auto_backup_var = tk.BooleanVar(value=True)
        auto_backup_cb = ttk.Checkbutton(backup_frame, variable=self.auto_backup_var)
        self._register_text(auto_backup_cb, "settings.autoBackup", "啟用自動備份", scope="page")
        auto_backup_cb.pack(side='left')
        
        interval_label = ttk.Label(backup_frame, font=('Segoe UI', 10))
        self._register_text(interval_label, "settings.backupInterval", "備份間隔:", scope="page")
        interval_label.pack(side='left', padx=(20, 10))
        self.backup_interval_var = tk.StringVar(value='7')
        ttk.Entry(backup_frame, textvariable=self.backup_interval_var, width=5, style='Modern.TEntry').pack(side='left')
        days_label = ttk.Label(backup_frame, font=('Segoe UI', 10))
        self._register_text(days_label, "settings.days", "天", scope="page")
        days_label.pack(side='left', padx=(5, 0))
    
    def toggle_sidebar(self):
        """收合/展開側邊欄"""
        self.sidebar_collapsed = not self.sidebar_collapsed
        
        if self.sidebar_collapsed:
            self.sidebar_frame.configure(width=60)
            self.toggle_sidebar_btn.configure(text='▶')
            # 隱藏文字
            for btn in self.nav_buttons.values():
                btn.configure(text='')
        else:
            self.sidebar_frame.configure(width=220)
            self.toggle_sidebar_btn.configure(text='◀')
            # 恢復文字
            self.update_nav_text()
        self._position_sidebar_toggle()

    def _position_sidebar_toggle(self):
        width = 60 if self.sidebar_collapsed else 220
        self.toggle_sidebar_btn.place(x=width - 24, y=10)
    
    def update_nav_text(self):
        """更新導航文字"""
        for item_id, icon, text_key, text_default in self._nav_items:
            if item_id in self.nav_buttons:
                if self.sidebar_collapsed:
                    self.nav_buttons[item_id].configure(text="")
                else:
                    label = self._t(text_key, text_default)
                    self.nav_buttons[item_id].configure(text=f"{icon} {label}")
    
    def toggle_auth(self):
        """切換登入/登出"""
        if self.current_user:
            self.logout()
        else:
            self.login()
    
    def login(self):
        """登入"""
        try:
            from frontend.src.components.password_change_dialog import PasswordChangeDialog
            
            # 模擬登入
            self.current_user = {'username': 'Admin', 'role': 'admin'}
            self._update_auth_ui()
            self._set_status("status.loginSuccess", "✅ 登入成功")
            
        except ImportError:
            messagebox.showerror(self._t("common.error", "錯誤"), self._t("auth.loginUnavailable", "登入功能暫時無法使用"))
    
    def logout(self):
        """登出"""
        self.current_user = None
        self._update_auth_ui()
        self._set_status("status.loggedOut", "✅ 已登出")
        self.show_page('daily_report')
    
    def on_language_changed(self, new_lang_code):
        """語言變更回調"""
        lang_names = {"ja": "日本語", "en": "English", "zh": "中文"}
        current_lang_name = lang_names.get(new_lang_code, new_lang_code)
        self._apply_i18n()
        self.update_nav_text()
        self.lang_selector.update_text()
        self._update_auth_ui()
        self._update_admin_tab_texts()
        if hasattr(self, "attendance_section"):
            self.attendance_section.update_language()
        if hasattr(self, "admin_user_mgmt"):
            self.admin_user_mgmt.update_ui_language()
        if hasattr(self, "admin_trans_mgmt"):
            self.admin_trans_mgmt.update_ui_language()
        self._update_shift_values()
        self._sync_report_context_from_form()
        self._update_delay_headers()
        self._update_summary_headers()
        self._update_report_context_label()
        self.status_label.config(text=self._t("status.languageChanged", "🌐 語言已切換至: {language}").format(language=current_lang_name))
        self.update_nav_text()
    
    def add_tooltip(self, widget, text_key, text_default):
        """添加懸停提示"""
        def enter(event):
            self.status_label.config(text=f'💡 {self._t(text_key, text_default)}')
        
        def leave(event):
            self._set_status("status.ready", "就緒")
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def _update_admin_tab_texts(self):
        if not hasattr(self, "admin_notebook"):
            return
        tabs = [
            (0, "admin.tabUsers", "👥 使用者管理"),
            (1, "admin.tabTranslations", "🌐 翻譯管理"),
            (2, "admin.tabSettings", "⚙️ 系統設定"),
        ]
        for index, key, default in tabs:
            try:
                self.admin_notebook.tab(index, text=self._t(key, default))
            except Exception:
                continue

    def _update_shift_values(self):
        if not hasattr(self, "shift_combo") or not hasattr(self, "shift_var"):
            return
        new_values = [
            self._t("shift.day", "Day"),
            self._t("shift.night", "Night"),
        ]
        current = self.shift_var.get()
        try:
            index = self.shift_values.index(current)
        except Exception:
            index = 0
        self.shift_values = new_values
        self.shift_combo["values"] = new_values
        self.shift_var.set(new_values[index])
    
    def add_equipment_record(self):
        """添加設備記錄"""
        if not self.ensure_report_context():
            return
        self._set_status("status.equipmentAdded", "✅ 設備異常記錄已添加")
    
    def view_equipment_history(self):
        """查看設備歷史"""
        self._set_status("status.equipmentHistoryLoading", "📋 正在載入設備異常歷史...")
    
    def add_lot_record(self):
        """添加批次記錄"""
        if not self.ensure_report_context():
            return
        self._set_status("status.lotAdded", "✅ 批次異常記錄已添加")
    
    def view_lot_list(self):
        """查看批次列表"""
        self._set_status("status.lotListLoading", "📋 正在載入批次異常列表...")
    
    def browse_image(self):
        """瀏覽圖片"""
        file_path = filedialog.askopenfilename(
            title=self._t("common.selectImage", "選擇圖片文件"),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path_var.set(file_path)
            self.status_label.config(
                text=self._t("status.imageSelected", "📷 已選擇圖片: {filename}").format(
                    filename=os.path.basename(file_path)
                )
            )
    
    def save_daily_report(self):
        """儲存日報"""
        self._sync_report_context_from_form()
        self._set_status("status.dailySaved", "💾 日報已儲存")
    
    def reset_daily_report(self):
        """重置日報"""
        if hasattr(self, "date_var"):
            self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        if hasattr(self, "shift_values") and hasattr(self, "shift_var") and self.shift_values:
            self.shift_var.set(self.shift_values[0])
        if hasattr(self, "area_var"):
            self.area_var.set("etching_D")
        self._sync_report_context_from_form()
        self._set_status("status.dailyReset", "🔄 日報表單已重置")

    def _sync_report_context_from_form(self):
        if hasattr(self, "date_var"):
            self.report_context["date"] = self.date_var.get().strip()
        if hasattr(self, "shift_var"):
            self.report_context["shift"] = self.shift_var.get().strip()
        if hasattr(self, "area_var"):
            self.report_context["area"] = self.area_var.get().strip()
        self._update_report_context_label()

    def _update_report_context_label(self):
        unknown = self._t("context.unknown", "未設定")
        date = self.report_context.get("date") or unknown
        shift = self.report_context.get("shift") or unknown
        area = self.report_context.get("area") or unknown
        text = self._t("context.currentReport", "目前日報：日期 {date}｜班別 {shift}｜區域 {area}")
        self.context_label.config(text=text.format(date=date, shift=shift, area=area))

    def _apply_report_date_to_filters(self):
        report_date = self.report_context.get("date") or ""
        if report_date:
            if hasattr(self, "delay_start_var") and not self.delay_start_var.get().strip():
                self.delay_start_var.set(report_date)
            if hasattr(self, "delay_end_var") and not self.delay_end_var.get().strip():
                self.delay_end_var.set(report_date)
            if hasattr(self, "summary_start_var") and not self.summary_start_var.get().strip():
                self.summary_start_var.set(report_date)
            if hasattr(self, "summary_end_var") and not self.summary_end_var.get().strip():
                self.summary_end_var.set(report_date)

    def get_report_context(self):
        return dict(self.report_context)

    def ensure_report_context(self):
        if not all(self.report_context.get(key) for key in ("date", "shift", "area")):
            messagebox.showwarning(
                self._t("context.missingTitle", "尚未設定日報表"),
                self._t("context.missingBody", "請先在日報表設定日期、班別、區域後再繼續。")
            )
            return False
        return True

    def _update_delay_headers(self):
        if not hasattr(self, "delay_tree"):
            return
        for col, (key, default) in zip(self.delay_columns, self.delay_header_keys):
            self.delay_tree.heading(col, text=self._t(key, default))
            width = 50 if col == "id" else 110
            stretch = False if col == "id" else True
            anchor = "center" if col not in ("note", "action", "progress") else "w"
            self.delay_tree.column(col, width=width, stretch=stretch, anchor=anchor)

    def _update_summary_headers(self):
        if not hasattr(self, "summary_tree"):
            return
        for col, (key, default) in zip(self.summary_columns, self.summary_header_keys):
            self.summary_tree.heading(col, text=self._t(key, default))
            width = 50 if col == "id" else 110
            stretch = False if col == "id" else True
            anchor = "center" if col not in ("label",) else "w"
            self.summary_tree.column(col, width=width, stretch=stretch, anchor=anchor)

    def _clear_delay_view(self):
        if hasattr(self, "delay_tree"):
            self._clear_tree(self.delay_tree)
        self.delay_pending_records = []

    def _clear_summary_view(self):
        if hasattr(self, "summary_tree"):
            self._clear_tree(self.summary_tree)
        self.summary_pending_records = []

    def _render_delay_rows(self, rows, pending=False):
        self._clear_tree(self.delay_tree)
        for idx, row in enumerate(rows):
            if pending:
                row_id = f"P{idx}"
                values = (
                    row_id,
                    row["delay_date"],
                    row["time_range"],
                    row["reactor"],
                    row["process"],
                    row["lot"],
                    row["wafer"],
                    row["progress"],
                    row["prev_steps"],
                    row["prev_time"],
                    row["severity"],
                    row["action"],
                    row["note"],
                )
            else:
                values = (
                    row.id,
                    row.delay_date,
                    row.time_range,
                    row.reactor,
                    row.process,
                    row.lot,
                    row.wafer,
                    row.progress,
                    row.prev_steps,
                    row.prev_time,
                    row.severity,
                    row.action,
                    row.note,
                )
            self.delay_tree.insert("", "end", values=values)

    def _load_delay_entries(self):
        if self.delay_pending_records:
            self._render_delay_rows(self.delay_pending_records, pending=True)
            return
        start = self.delay_start_var.get().strip()
        end = self.delay_end_var.get().strip()
        start_date = end_date = None
        try:
            if start:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
            if end:
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
            return
        try:
            with SessionLocal() as db:
                query = db.query(DelayEntry)
                if start_date:
                    query = query.filter(DelayEntry.delay_date >= start_date)
                if end_date:
                    query = query.filter(DelayEntry.delay_date <= end_date)
                rows = query.order_by(DelayEntry.delay_date.desc(), DelayEntry.imported_at.desc()).all()
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")
            return
        self._render_delay_rows(rows, pending=False)

    def _import_delay_excel(self):
        path = filedialog.askopenfilename(
            title=self._t("delay.importExcel", "匯入延遲Excel"),
            filetypes=[("Excel Files", "*.xlsx;*.xls")],
        )
        if not path:
            return
        try:
            xls = pd.ExcelFile(path)
            sheet_name = xls.sheet_names[0]
            if len(xls.sheet_names) > 1:
                picker = tk.Toplevel(self.parent)
                picker.title(self._t("navigation.delayList", "延遲清單"))
                ttk.Label(picker, text=self._t("common.selectSheet", "選擇工作表")).pack(padx=10, pady=5)
                sheet_var = tk.StringVar(value=xls.sheet_names[0])
                combo = ttk.Combobox(picker, textvariable=sheet_var, values=xls.sheet_names, state="readonly")
                combo.pack(padx=10, pady=5)
                chosen = {"name": sheet_name}

                def confirm():
                    chosen["name"] = sheet_var.get()
                    picker.destroy()

                ttk.Button(picker, text=self._t("common.ok", "確定"), command=confirm).pack(pady=8)
                picker.grab_set()
                picker.wait_window()
                sheet_name = chosen["name"]

            df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")
            return

        def find_col(match):
            for col in df.columns:
                c = str(col).lower()
                if match in c:
                    return col
            return None

        col_map = {
            "date": find_col("date"),
            "time": find_col("time"),
            "reactor": find_col("reactor"),
            "process": find_col("process"),
            "lot": find_col("lot"),
            "wafer": find_col("wafer"),
            "progress": find_col("progress"),
            "prev_steps": find_col("previous"),
            "prev_time": find_col("prev"),
            "severity": find_col("severity") or find_col("caution"),
            "action": find_col("action") or find_col("対処"),
            "note": find_col("note") or find_col("備考"),
        }

        records = []
        for _, row in df.iterrows():
            raw_date = row.get(col_map["date"]) if col_map["date"] else None
            parsed_date = pd.to_datetime(raw_date, errors="coerce").date() if pd.notna(raw_date) else None
            if not parsed_date:
                continue

            def sval(key):
                col = col_map.get(key)
                if col is None:
                    return ""
                val = row.get(col)
                if pd.isna(val):
                    return ""
                return str(val).strip()

            records.append(
                {
                    "delay_date": parsed_date,
                    "time_range": sval("time"),
                    "reactor": sval("reactor"),
                    "process": sval("process"),
                    "lot": sval("lot"),
                    "wafer": sval("wafer"),
                    "progress": sval("progress"),
                    "prev_steps": sval("prev_steps"),
                    "prev_time": sval("prev_time"),
                    "severity": sval("severity"),
                    "action": sval("action"),
                    "note": sval("note"),
                }
            )

        if not records:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.emptyData", "查無資料"))
            return

        self.delay_pending_records = records
        self._render_delay_rows(records, pending=True)
        messagebox.showinfo(
            self._t("common.info", "資訊"),
            self._t("delay.importPending", "匯入完成，請確認後再點上傳"),
        )

    def _upload_delay_pending(self):
        if not self.delay_pending_records:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.emptyData", "查無資料"))
            return
        try:
            with SessionLocal() as db:
                unique_dates = {rec["delay_date"] for rec in self.delay_pending_records}
                if unique_dates:
                    db.query(DelayEntry).filter(DelayEntry.delay_date.in_(unique_dates)).delete(synchronize_session=False)
                for rec in self.delay_pending_records:
                    db.add(DelayEntry(**rec))
                db.commit()
            self.delay_pending_records = []
            self._load_delay_entries()
            messagebox.showinfo(self._t("common.success", "成功"), self._t("common.uploadSuccess", "上傳成功"))
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")

    def _edit_delay_dialog(self):
        sel = self.delay_tree.selection()
        if not sel:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.selectRow", "請先選擇一列"))
            return
        vals = self.delay_tree.item(sel[0], "values")
        if len(vals) < 13:
            return
        (
            row_id,
            d_date,
            d_time,
            reactor,
            process,
            lot,
            wafer,
            progress,
            prev_steps,
            prev_time,
            severity,
            action,
            note,
        ) = vals
        is_pending = isinstance(row_id, str) and str(row_id).startswith("P")
        dlg = tk.Toplevel(self.parent)
        dlg.title(self._t("navigation.delayList", "延遲清單"))
        dlg.columnconfigure(1, weight=1)

        fields = [
            ("date", self._t("delay.date", "日期"), d_date),
            ("time", self._t("delay.time", "時間"), d_time),
            ("reactor", self._t("delay.reactor", "設備"), reactor),
            ("process", self._t("delay.process", "製程"), process),
            ("lot", self._t("delay.lot", "批號"), lot),
            ("wafer", self._t("delay.wafer", "晶圓"), wafer),
            ("progress", self._t("delay.progress", "進行中"), progress),
            ("prev_steps", self._t("delay.prevSteps", "前站"), prev_steps),
            ("prev_time", self._t("delay.prevTime", "前站時間"), prev_time),
            ("severity", self._t("delay.severity", "嚴重度"), severity),
            ("action", self._t("delay.action", "對應內容"), action),
            ("note", self._t("delay.note", "備註"), note),
        ]
        vars_map = {}
        for idx, (key, label, value) in enumerate(fields):
            ttk.Label(dlg, text=label).grid(row=idx, column=0, padx=5, pady=4, sticky="e")
            var = tk.StringVar(value=str(value))
            ttk.Entry(dlg, textvariable=var, width=30).grid(row=idx, column=1, padx=5, pady=4, sticky="ew")
            vars_map[key] = var

        def save():
            try:
                if is_pending:
                    idx = int(str(row_id)[1:])
                    if idx < 0 or idx >= len(self.delay_pending_records):
                        messagebox.showerror(self._t("common.error", "錯誤"), self._t("common.selectRow", "請先選擇一列"))
                        return
                    try:
                        new_date = datetime.strptime(vars_map["date"].get().strip(), "%Y-%m-%d").date()
                    except Exception:
                        messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
                        return
                    rec = self.delay_pending_records[idx]
                    rec.update(
                        {
                            "delay_date": new_date,
                            "time_range": vars_map["time"].get().strip(),
                            "reactor": vars_map["reactor"].get().strip(),
                            "process": vars_map["process"].get().strip(),
                            "lot": vars_map["lot"].get().strip(),
                            "wafer": vars_map["wafer"].get().strip(),
                            "progress": vars_map["progress"].get().strip(),
                            "prev_steps": vars_map["prev_steps"].get().strip(),
                            "prev_time": vars_map["prev_time"].get().strip(),
                            "severity": vars_map["severity"].get().strip(),
                            "action": vars_map["action"].get().strip(),
                            "note": vars_map["note"].get().strip(),
                        }
                    )
                    self._render_delay_rows(self.delay_pending_records, pending=True)
                else:
                    with SessionLocal() as db:
                        row = db.query(DelayEntry).filter(DelayEntry.id == row_id).first()
                        if not row:
                            messagebox.showerror(self._t("common.error", "錯誤"), self._t("common.selectRow", "請先選擇一列"))
                            return
                        try:
                            row.delay_date = datetime.strptime(vars_map["date"].get().strip(), "%Y-%m-%d").date()
                        except Exception:
                            messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
                            return
                        row.time_range = vars_map["time"].get().strip()
                        row.reactor = vars_map["reactor"].get().strip()
                        row.process = vars_map["process"].get().strip()
                        row.lot = vars_map["lot"].get().strip()
                        row.wafer = vars_map["wafer"].get().strip()
                        row.progress = vars_map["progress"].get().strip()
                        row.prev_steps = vars_map["prev_steps"].get().strip()
                        row.prev_time = vars_map["prev_time"].get().strip()
                        row.severity = vars_map["severity"].get().strip()
                        row.action = vars_map["action"].get().strip()
                        row.note = vars_map["note"].get().strip()
                        db.commit()
                    self._load_delay_entries()
                dlg.destroy()
            except Exception as exc:
                messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")

        save_btn = ttk.Button(dlg, style='Primary.TButton', command=save)
        self._register_text(save_btn, "common.save", "儲存", scope="page")
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def _load_summary_actual(self):
        self._clear_tree(self.summary_tree)
        start = self.summary_start_var.get().strip()
        end = self.summary_end_var.get().strip()
        start_date = end_date = None
        try:
            if start:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
            if end:
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
            return

        def fmt(val):
            return "-" if val == 0 else str(val)

        if self.summary_pending_records:
            for idx, row in enumerate(self.summary_pending_records):
                self.summary_tree.insert(
                    "",
                    "end",
                    values=(
                        f"P{idx}",
                        row["summary_date"],
                        row["label"],
                        fmt(row["plan"]),
                        fmt(row["completed"]),
                        fmt(row["in_process"]),
                        fmt(row["on_track"]),
                        fmt(row["at_risk"]),
                        fmt(row["delayed"]),
                        fmt(row["no_data"]),
                        fmt(row["scrapped"]),
                    ),
                )
            return

        try:
            with SessionLocal() as db:
                query = db.query(SummaryActualEntry)
                if start_date:
                    query = query.filter(SummaryActualEntry.summary_date >= start_date)
                if end_date:
                    query = query.filter(SummaryActualEntry.summary_date <= end_date)
                rows = query.order_by(SummaryActualEntry.summary_date.desc(), SummaryActualEntry.imported_at.desc()).all()
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")
            return

        for row in rows:
            self.summary_tree.insert(
                "",
                "end",
                values=(
                    row.id,
                    row.summary_date,
                    row.label,
                    fmt(row.plan),
                    fmt(row.completed),
                    fmt(row.in_process),
                    fmt(row.on_track),
                    fmt(row.at_risk),
                    fmt(row.delayed),
                    fmt(row.no_data),
                    fmt(row.scrapped),
                ),
            )

    def _import_summary_actual_excel(self):
        path = filedialog.askopenfilename(
            title=self._t("summaryActual.importExcel", "匯入 Summary Actual"),
            filetypes=[("Excel Files", "*.xlsx;*.xls")],
        )
        if not path:
            return
        try:
            raw_sheet = pd.read_excel(path, sheet_name="Summary(Actual)", header=None)
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")
            return
        summary_date = None
        if len(raw_sheet) > 1:
            for val in raw_sheet.iloc[1].dropna().tolist():
                parsed = pd.to_datetime(val, errors="coerce")
                if pd.isna(parsed):
                    continue
                summary_date = parsed.date()
                break
        if not summary_date:
            messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
            return

        try:
            df = pd.read_excel(path, sheet_name="Summary(Actual)", header=2)
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")
            return

        def norm(col):
            return str(col).strip().lower().replace(" ", "").replace("_", "")

        col_lookup = {norm(c): c for c in df.columns}

        def get_col(key):
            return col_lookup.get(key, None)

        def get_val(row, key):
            col = get_col(key)
            if col is None:
                return 0
            val = row.get(col)
            if pd.isna(val):
                return 0
            try:
                return int(val)
            except Exception:
                try:
                    return int(float(val))
                except Exception:
                    return 0

        records = []
        for _, row in df.iterrows():
            label_val = ""
            if len(df.columns) > 2:
                part_b = row.get(df.columns[1])
                part_c = row.get(df.columns[2])
                label_val = f"{'' if pd.isna(part_b) else str(part_b).strip()} {'' if pd.isna(part_c) else str(part_c).strip()}".strip()
            if not label_val:
                continue
            records.append(
                {
                    "summary_date": summary_date,
                    "label": label_val,
                    "plan": get_val(row, "plan"),
                    "completed": get_val(row, "completed"),
                    "in_process": get_val(row, "inprocess"),
                    "on_track": get_val(row, "ontrack"),
                    "at_risk": get_val(row, "atrisk"),
                    "delayed": get_val(row, "delayed"),
                    "no_data": get_val(row, "nodata"),
                    "scrapped": get_val(row, "scrapped"),
                }
            )

        if not records:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.emptyData", "查無資料"))
            return
        self.summary_pending_records = records
        self._load_summary_actual()
        messagebox.showinfo(
            self._t("common.info", "資訊"),
            self._t("summaryActual.importPending", "匯入完成，請確認後再點上傳"),
        )

    def _upload_summary_pending(self):
        if not self.summary_pending_records:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.emptyData", "查無資料"))
            return
        try:
            with SessionLocal() as db:
                unique_dates = {rec["summary_date"] for rec in self.summary_pending_records}
                if unique_dates:
                    db.query(SummaryActualEntry).filter(SummaryActualEntry.summary_date.in_(unique_dates)).delete(
                        synchronize_session=False
                    )
                for rec in self.summary_pending_records:
                    db.add(SummaryActualEntry(**rec))
                db.commit()
            self.summary_pending_records = []
            self._load_summary_actual()
            messagebox.showinfo(self._t("common.success", "成功"), self._t("common.uploadSuccess", "上傳成功"))
        except Exception as exc:
            messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")

    def _edit_summary_dialog(self):
        sel = self.summary_tree.selection()
        if not sel:
            messagebox.showinfo(self._t("common.info", "資訊"), self._t("common.selectRow", "請先選擇一列"))
            return
        vals = self.summary_tree.item(sel[0], "values")
        if len(vals) < 10:
            return
        (
            row_id,
            d_date,
            label,
            plan,
            completed,
            in_process,
            on_track,
            at_risk,
            delayed,
            no_data,
            scrapped,
        ) = vals
        is_pending = isinstance(row_id, str) and str(row_id).startswith("P")
        dlg = tk.Toplevel(self.parent)
        dlg.title(self._t("navigation.summaryActual", "Summary Actual"))
        dlg.columnconfigure(1, weight=1)

        fields = [
            ("date", self._t("summaryActual.date", "日期"), d_date),
            ("label", self._t("summaryActual.label", "標籤"), label),
            ("plan", self._t("summaryActual.plan", "Plan"), plan),
            ("completed", self._t("summaryActual.completed", "Completed"), completed),
            ("in_process", self._t("summaryActual.inProcess", "In Process"), in_process),
            ("on_track", self._t("summaryActual.onTrack", "On Track"), on_track),
            ("at_risk", self._t("summaryActual.atRisk", "At Risk"), at_risk),
            ("delayed", self._t("summaryActual.delayed", "Delayed"), delayed),
            ("no_data", self._t("summaryActual.noData", "No Data"), no_data),
            ("scrapped", self._t("summaryActual.scrapped", "Scrapped"), scrapped),
        ]
        vars_map = {}
        for idx, (key, label_text, value) in enumerate(fields):
            ttk.Label(dlg, text=label_text).grid(row=idx, column=0, padx=5, pady=4, sticky="e")
            var = tk.StringVar(value=str(value))
            ttk.Entry(dlg, textvariable=var, width=30).grid(row=idx, column=1, padx=5, pady=4, sticky="ew")
            vars_map[key] = var

        def save():
            try:
                if is_pending:
                    idx = int(str(row_id)[1:])
                    if idx < 0 or idx >= len(self.summary_pending_records):
                        messagebox.showerror(self._t("common.error", "錯誤"), self._t("common.selectRow", "請先選擇一列"))
                        return
                    try:
                        new_date = datetime.strptime(vars_map["date"].get().strip(), "%Y-%m-%d").date()
                    except Exception:
                        messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
                        return
                    rec = self.summary_pending_records[idx]
                    rec["summary_date"] = new_date
                    rec["label"] = vars_map["label"].get().strip()
                    for key in [
                        "plan",
                        "completed",
                        "in_process",
                        "on_track",
                        "at_risk",
                        "delayed",
                        "no_data",
                        "scrapped",
                    ]:
                        try:
                            rec[key] = int(vars_map[key].get().strip() or 0)
                        except Exception:
                            rec[key] = 0
                    self._load_summary_actual()
                else:
                    with SessionLocal() as db:
                        row = db.query(SummaryActualEntry).filter(SummaryActualEntry.id == row_id).first()
                        if not row:
                            messagebox.showerror(self._t("common.error", "錯誤"), self._t("common.selectRow", "請先選擇一列"))
                            return
                        try:
                            row.summary_date = datetime.strptime(vars_map["date"].get().strip(), "%Y-%m-%d").date()
                        except Exception:
                            messagebox.showerror(self._t("common.error", "錯誤"), self._t("errors.invalidDateFormat", "日期格式需為 YYYY-MM-DD"))
                            return
                        row.label = vars_map["label"].get().strip()
                        for key, attr in [
                            ("plan", "plan"),
                            ("completed", "completed"),
                            ("in_process", "in_process"),
                            ("on_track", "on_track"),
                            ("at_risk", "at_risk"),
                            ("delayed", "delayed"),
                            ("no_data", "no_data"),
                            ("scrapped", "scrapped"),
                        ]:
                            try:
                                setattr(row, attr, int(vars_map[key].get().strip() or 0))
                            except Exception:
                                setattr(row, attr, 0)
                        db.commit()
                    self._load_summary_actual()
                dlg.destroy()
            except Exception as exc:
                messagebox.showerror(self._t("common.error", "錯誤"), f"{exc}")

        save_btn = ttk.Button(dlg, style='Primary.TButton', command=save)
        self._register_text(save_btn, "common.save", "儲存", scope="page")
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)


# 測試函數
def test_modern_ui():
    """測試現代化 UI"""
    root = tk.Tk()
    root.title("電子交接系統 - 現代化介面")
    root.geometry("1200x800")
    
    # 模擬語言管理器
    class MockLangManager:
        def __init__(self):
            self.current_lang = "zh"
        
        def get_text(self, key, default):
            return default
        
        def set_language(self, lang):
            self.current_lang = lang
        
        def get_current_language(self):
            return self.current_lang
        
        def get_widget(self):
            return None
    
    # 創建現代化主框架
    lang_manager = MockLangManager()
    modern_frame = ModernMainFrame(root, lang_manager)
    
    root.mainloop()


if __name__ == "__main__":
    test_modern_ui()
