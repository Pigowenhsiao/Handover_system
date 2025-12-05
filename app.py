from __future__ import annotations

import csv
import os
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auth import verify_password, hash_password
from models import (
    AttendanceEntry,
    DailyReport,
    EquipmentLog,
    LotLog,
    SessionLocal,
    User,
    init_db,
)


SHIFT_OPTIONS = ["Day", "Night"]
AREA_OPTIONS = ["etching_D", "etching_E", "litho", "thin_film"]


class HandoverApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("電子交接本系統（桌面版）")
        self.geometry("1100x720")
        self.resizable(True, True)
        self.session_user: Optional[Dict[str, str]] = None
        init_db()
        self._build_login()

    def _build_login(self) -> None:
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(expand=True)

        ttk.Label(self.login_frame, text="電子交接本系統", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.login_frame, text="帳號").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self.login_frame, text="密碼").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.username_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="登入", command=self._handle_login).grid(row=3, column=0, columnspan=2, pady=10)

    def _handle_login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showerror("登入失敗", "帳號與密碼不可為空。")
            return
        try:
            with SessionLocal() as db:
                user = db.query(User).filter(User.username == username).first()
                if user and verify_password(password, user.password_hash):
                    self.session_user = {"id": user.id, "username": user.username, "role": user.role}
                else:
                    self.session_user = None
        except Exception as exc:
            messagebox.showerror("登入失敗", f"資料庫錯誤：{exc}")
            return

        if self.session_user:
            self.login_frame.destroy()
            self._build_main_ui()
        else:
            messagebox.showerror("登入失敗", "帳號或密碼錯誤。")

    def _build_main_ui(self) -> None:
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x")
        ttk.Label(top_bar, text=f"使用者：{self.session_user['username']}（{self.session_user['role']}）").pack(side="left", padx=10, pady=5)
        ttk.Button(top_bar, text="登出", command=self._logout).pack(side="right", padx=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.daily_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)
        self.user_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.daily_frame, text="填寫日報")
        self.notebook.add(self.report_frame, text="報表")
        if self.session_user.get("role") == "admin":
            self.notebook.add(self.user_frame, text="使用者管理")

        self._build_daily_tab()
        self._build_report_tab()
        if self.session_user.get("role") == "admin":
            self._build_user_tab()

    def _logout(self) -> None:
        self.session_user = None
        for widget in self.winfo_children():
            widget.destroy()
        self._build_login()

    def _clear_tree(self, tree: ttk.Treeview) -> None:
        for item in tree.get_children():
            tree.delete(item)

    def _embed_chart(self, frame: ttk.Frame, fig_attr: str, fig: plt.Figure) -> None:
        # Destroy previous canvas if exists
        old = getattr(self, fig_attr, None)
        if old:
            old.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        setattr(self, fig_attr, canvas)

    # ================= 報表：出勤 =================
    def _build_attendance_report_tab(self) -> None:
        control = ttk.Frame(self.att_tab)
        control.pack(fill="x", padx=10, pady=5)

        ttk.Label(control, text="期間類型").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.att_mode_var = tk.StringVar(value="日")
        ttk.Combobox(control, textvariable=self.att_mode_var, values=["日", "週", "月", "自訂"], width=8, state="readonly").grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(control, text="起始日 YYYY-MM-DD").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Label(control, text="結束日 YYYY-MM-DD").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.att_start_var = tk.StringVar()
        self.att_end_var = tk.StringVar()
        ttk.Entry(control, textvariable=self.att_start_var, width=12).grid(row=0, column=3, padx=5, pady=5)
        ttk.Entry(control, textvariable=self.att_end_var, width=12).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(control, text="查詢", command=self._load_attendance_report).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(control, text="匯出 CSV", command=self._export_attendance_csv).grid(row=0, column=7, padx=5, pady=5)

        self.att_tree = ttk.Treeview(
            self.att_tab,
            columns=("period", "scheduled", "present", "absent", "rate"),
            show="headings",
            height=12,
        )
        for col, text in zip(self.att_tree["columns"], ["期間", "應出勤", "實際出勤", "缺勤", "出勤率(%)"]):
            self.att_tree.heading(col, text=text)
            self.att_tree.column(col, width=140)
        self.att_tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.att_chart_frame = ttk.LabelFrame(self.att_tab, text="出勤率趨勢")
        self.att_chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def _load_attendance_report(self) -> None:
        mode = self.att_mode_var.get()
        start_str = self.att_start_var.get().strip()
        end_str = self.att_end_var.get().strip()
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
        except ValueError:
            messagebox.showerror("錯誤", "日期格式應為 YYYY-MM-DD")
            return

        try:
            with SessionLocal() as db:
                query = (
                    db.query(AttendanceEntry, DailyReport)
                    .join(DailyReport, AttendanceEntry.report_id == DailyReport.id)
                )
                if start_date:
                    query = query.filter(DailyReport.date >= start_date)
                if end_date:
                    query = query.filter(DailyReport.date <= end_date)
                rows = query.all()
        except Exception as exc:
            messagebox.showerror("查詢失敗", f"{exc}")
            return

        data = []
        for att, rep in rows:
            data.append(
                {
                    "date": rep.date,
                    "scheduled": att.scheduled_count,
                    "present": att.present_count,
                    "absent": att.absent_count,
                }
            )
        if not data:
            self._clear_tree(self.att_tree)
            messagebox.showinfo("提示", "查無資料")
            return

        df = pd.DataFrame(data)

        def start_of_week(d: date) -> date:
            return d - timedelta(days=d.weekday())

        if mode == "日":
            grouped = df.groupby("date", as_index=False).sum()
            grouped["period"] = grouped["date"].astype(str)
        elif mode == "週":
            df["week_start"] = df["date"].apply(start_of_week)
            grouped = df.groupby("week_start", as_index=False).sum()
            grouped["period"] = grouped["week_start"].astype(str)
        elif mode == "月":
            df["month"] = df["date"].apply(lambda d: d.strftime("%Y-%m"))
            grouped = df.groupby("month", as_index=False).sum()
            grouped["period"] = grouped["month"]
        else:  # 自訂
            grouped = df.groupby("date", as_index=False).sum()
            grouped["period"] = grouped["date"].astype(str)

        grouped["rate"] = grouped.apply(lambda r: "" if r["scheduled"] == 0 else round(r["present"] * 100 / r["scheduled"], 1), axis=1)

        self._clear_tree(self.att_tree)
        for _, r in grouped.iterrows():
            self.att_tree.insert("", "end", values=(r["period"], r["scheduled"], r["present"], r["absent"], r["rate"]))

        # Chart
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(grouped["period"], [r if r != "" else 0 for r in grouped["rate"]], marker="o")
        ax.set_ylabel("出勤率(%)")
        ax.set_xlabel("期間")
        ax.set_title("出勤率趨勢")
        ax.grid(True, linestyle="--", alpha=0.4)
        plt.xticks(rotation=45, ha="right")
        self._embed_chart(self.att_chart_frame, "att_chart_canvas", fig)

    def _export_attendance_csv(self) -> None:
        rows = [self.att_tree.item(i, "values") for i in self.att_tree.get_children()]
        if not rows:
            messagebox.showinfo("匯出", "沒有資料可匯出")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="匯出出勤報表")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["期間", "應出勤", "實際出勤", "缺勤", "出勤率(%)"])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("匯出", "匯出成功")
        except Exception as exc:
            messagebox.showerror("匯出失敗", f"{exc}")

    # ================= 報表：設備異常 =================
    def _build_equipment_report_tab(self) -> None:
        control = ttk.Frame(self.equip_tab)
        control.pack(fill="x", padx=10, pady=5)
        ttk.Label(control, text="期間類型").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.equip_mode_var = tk.StringVar(value="日")
        ttk.Combobox(control, textvariable=self.equip_mode_var, values=["日", "週", "月", "自訂"], width=8, state="readonly").grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(control, text="起始日 YYYY-MM-DD").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Label(control, text="結束日 YYYY-MM-DD").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.equip_start_var = tk.StringVar()
        self.equip_end_var = tk.StringVar()
        ttk.Entry(control, textvariable=self.equip_start_var, width=12).grid(row=0, column=3, padx=5, pady=5)
        ttk.Entry(control, textvariable=self.equip_end_var, width=12).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(control, text="查詢", command=self._load_equipment_report).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(control, text="匯出 CSV", command=self._export_equipment_csv).grid(row=0, column=7, padx=5, pady=5)

        self.equip_tree_detail = ttk.Treeview(
            self.equip_tab,
            columns=("date", "area", "equip", "desc", "impact", "action"),
            show="headings",
            height=8,
        )
        for col, text in zip(self.equip_tree_detail["columns"], ["日期", "區域", "設備", "異常內容", "影響數量", "對應內容"]):
            self.equip_tree_detail.heading(col, text=text)
            self.equip_tree_detail.column(col, width=140)
        self.equip_tree_detail.pack(fill="both", expand=True, padx=10, pady=5)

        agg_frame = ttk.LabelFrame(self.equip_tab, text="彙總")
        agg_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.equip_tree_agg = ttk.Treeview(
            agg_frame,
            columns=("period", "count"),
            show="headings",
            height=6,
        )
        for col, text in zip(self.equip_tree_agg["columns"], ["期間", "筆數"]):
            self.equip_tree_agg.heading(col, text=text)
            self.equip_tree_agg.column(col, width=150)
        self.equip_tree_agg.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ttk.Scrollbar(agg_frame, orient="vertical", command=self.equip_tree_agg.yview).pack(side="left", fill="y")

        self.equip_chart_frame = ttk.LabelFrame(self.equip_tab, text="設備異常趨勢")
        self.equip_chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def _load_equipment_report(self) -> None:
        mode = self.equip_mode_var.get()
        start_str = self.equip_start_var.get().strip()
        end_str = self.equip_end_var.get().strip()
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
        except ValueError:
            messagebox.showerror("錯誤", "日期格式應為 YYYY-MM-DD")
            return
        try:
            with SessionLocal() as db:
                query = db.query(EquipmentLog, DailyReport).join(DailyReport, EquipmentLog.report_id == DailyReport.id)
                if start_date:
                    query = query.filter(DailyReport.date >= start_date)
                if end_date:
                    query = query.filter(DailyReport.date <= end_date)
                rows = query.all()
        except Exception as exc:
            messagebox.showerror("查詢失敗", f"{exc}")
            return

        detail = []
        for eq, rep in rows:
            detail.append(
                {
                    "date": rep.date,
                    "area": rep.area,
                    "equip": eq.equip_id,
                    "desc": eq.description,
                    "impact": eq.impact_qty,
                    "action": eq.action_taken,
                }
            )
        if not detail:
            self._clear_tree(self.equip_tree_detail)
            self._clear_tree(self.equip_tree_agg)
            messagebox.showinfo("提示", "查無資料")
            return

        df = pd.DataFrame(detail)
        self._clear_tree(self.equip_tree_detail)
        for _, r in df.iterrows():
            self.equip_tree_detail.insert("", "end", values=(r["date"], r["area"], r["equip"], r["desc"], r["impact"], r["action"]))

        def start_of_week(d: date) -> date:
            return d - timedelta(days=d.weekday())

        if mode == "日":
            grouped = df.groupby("date", as_index=False).size()
            grouped["period"] = grouped["date"].astype(str)
        elif mode == "週":
            df["week_start"] = df["date"].apply(start_of_week)
            grouped = df.groupby("week_start", as_index=False).size()
            grouped["period"] = grouped["week_start"].astype(str)
        elif mode == "月":
            df["month"] = df["date"].apply(lambda d: d.strftime("%Y-%m"))
            grouped = df.groupby("month", as_index=False).size()
            grouped["period"] = grouped["month"]
        else:
            grouped = df.groupby("date", as_index=False).size()
            grouped["period"] = grouped["date"].astype(str)

        self._clear_tree(self.equip_tree_agg)
        for _, r in grouped.iterrows():
            self.equip_tree_agg.insert("", "end", values=(r["period"], r["size"]))

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(grouped["period"], grouped["size"])
        ax.set_ylabel("筆數")
        ax.set_xlabel("期間")
        ax.set_title("設備異常趨勢")
        plt.xticks(rotation=45, ha="right")
        self._embed_chart(self.equip_chart_frame, "equip_chart_canvas", fig)

    def _export_equipment_csv(self) -> None:
        rows = [self.equip_tree_detail.item(i, "values") for i in self.equip_tree_detail.get_children()]
        if not rows:
            messagebox.showinfo("匯出", "沒有資料可匯出")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="匯出設備異常報表")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["日期", "區域", "設備", "異常內容", "影響數量", "對應內容"])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("匯出", "匯出成功")
        except Exception as exc:
            messagebox.showerror("匯出失敗", f"{exc}")

    # ================= 報表：異常 LOT =================
    def _build_lot_report_tab(self) -> None:
        control = ttk.Frame(self.lot_tab)
        control.pack(fill="x", padx=10, pady=5)
        ttk.Label(control, text="期間類型").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.lot_mode_var = tk.StringVar(value="日")
        ttk.Combobox(control, textvariable=self.lot_mode_var, values=["日", "週", "月", "自訂"], width=8, state="readonly").grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(control, text="起始日 YYYY-MM-DD").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Label(control, text="結束日 YYYY-MM-DD").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.lot_start_var = tk.StringVar()
        self.lot_end_var = tk.StringVar()
        ttk.Entry(control, textvariable=self.lot_start_var, width=12).grid(row=0, column=3, padx=5, pady=5)
        ttk.Entry(control, textvariable=self.lot_end_var, width=12).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(control, text="查詢", command=self._load_lot_report).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(control, text="匯出 CSV", command=self._export_lot_csv).grid(row=0, column=7, padx=5, pady=5)

        self.lot_tree_detail = ttk.Treeview(
            self.lot_tab,
            columns=("date", "area", "lot", "desc", "status", "notes"),
            show="headings",
            height=8,
        )
        for col, text in zip(self.lot_tree_detail["columns"], ["日期", "區域", "批號", "異常內容", "處置狀況", "特記事項"]):
            self.lot_tree_detail.heading(col, text=text)
            self.lot_tree_detail.column(col, width=140)
        self.lot_tree_detail.pack(fill="both", expand=True, padx=10, pady=5)

        agg_frame = ttk.LabelFrame(self.lot_tab, text="彙總")
        agg_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.lot_tree_agg = ttk.Treeview(
            agg_frame,
            columns=("period", "count"),
            show="headings",
            height=6,
        )
        for col, text in zip(self.lot_tree_agg["columns"], ["期間", "筆數"]):
            self.lot_tree_agg.heading(col, text=text)
            self.lot_tree_agg.column(col, width=150)
        self.lot_tree_agg.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ttk.Scrollbar(agg_frame, orient="vertical", command=self.lot_tree_agg.yview).pack(side="left", fill="y")

        self.lot_chart_frame = ttk.LabelFrame(self.lot_tab, text="異常 LOT 趨勢")
        self.lot_chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def _load_lot_report(self) -> None:
        mode = self.lot_mode_var.get()
        start_str = self.lot_start_var.get().strip()
        end_str = self.lot_end_var.get().strip()
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
        except ValueError:
            messagebox.showerror("錯誤", "日期格式應為 YYYY-MM-DD")
            return
        try:
            with SessionLocal() as db:
                query = db.query(LotLog, DailyReport).join(DailyReport, LotLog.report_id == DailyReport.id)
                if start_date:
                    query = query.filter(DailyReport.date >= start_date)
                if end_date:
                    query = query.filter(DailyReport.date <= end_date)
                rows = query.all()
        except Exception as exc:
            messagebox.showerror("查詢失敗", f"{exc}")
            return

        detail = []
        for lot, rep in rows:
            detail.append(
                {
                    "date": rep.date,
                    "area": rep.area,
                    "lot": lot.lot_id,
                    "desc": lot.description,
                    "status": lot.status,
                    "notes": lot.notes,
                }
            )
        if not detail:
            self._clear_tree(self.lot_tree_detail)
            self._clear_tree(self.lot_tree_agg)
            messagebox.showinfo("提示", "查無資料")
            return

        df = pd.DataFrame(detail)
        self._clear_tree(self.lot_tree_detail)
        for _, r in df.iterrows():
            self.lot_tree_detail.insert("", "end", values=(r["date"], r["area"], r["lot"], r["desc"], r["status"], r["notes"]))

        def start_of_week(d: date) -> date:
            return d - timedelta(days=d.weekday())

        if mode == "日":
            grouped = df.groupby("date", as_index=False).size()
            grouped["period"] = grouped["date"].astype(str)
        elif mode == "週":
            df["week_start"] = df["date"].apply(start_of_week)
            grouped = df.groupby("week_start", as_index=False).size()
            grouped["period"] = grouped["week_start"].astype(str)
        elif mode == "月":
            df["month"] = df["date"].apply(lambda d: d.strftime("%Y-%m"))
            grouped = df.groupby("month", as_index=False).size()
            grouped["period"] = grouped["month"]
        else:
            grouped = df.groupby("date", as_index=False).size()
            grouped["period"] = grouped["date"].astype(str)

        self._clear_tree(self.lot_tree_agg)
        for _, r in grouped.iterrows():
            self.lot_tree_agg.insert("", "end", values=(r["period"], r["size"]))

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(grouped["period"], grouped["size"])
        ax.set_ylabel("筆數")
        ax.set_xlabel("期間")
        ax.set_title("異常 LOT 趨勢")
        plt.xticks(rotation=45, ha="right")
        self._embed_chart(self.lot_chart_frame, "lot_chart_canvas", fig)

    def _export_lot_csv(self) -> None:
        rows = [self.lot_tree_detail.item(i, "values") for i in self.lot_tree_detail.get_children()]
        if not rows:
            messagebox.showinfo("匯出", "沒有資料可匯出")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="匯出異常 LOT 報表")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["日期", "區域", "批號", "異常內容", "處置狀況", "特記事項"])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("匯出", "匯出成功")
        except Exception as exc:
            messagebox.showerror("匯出失敗", f"{exc}")

    # Daily tab
    def _build_daily_tab(self) -> None:
        info_frame = ttk.LabelFrame(self.daily_frame, text="基礎資訊")
        info_frame.pack(fill="x", padx=10, pady=5)

        self.date_var = tk.StringVar(value=str(date.today()))
        self.shift_var = tk.StringVar(value=SHIFT_OPTIONS[0])
        self.area_var = tk.StringVar(value=AREA_OPTIONS[0])

        ttk.Label(info_frame, text="日期 YYYY-MM-DD").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(info_frame, textvariable=self.date_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(info_frame, text="班別").grid(row=0, column=2, padx=5, pady=5)
        ttk.Combobox(info_frame, textvariable=self.shift_var, values=SHIFT_OPTIONS, width=10, state="readonly").grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(info_frame, text="區域").grid(row=0, column=4, padx=5, pady=5)
        ttk.Combobox(info_frame, textvariable=self.area_var, values=AREA_OPTIONS, width=12, state="readonly").grid(row=0, column=5, padx=5, pady=5)

        # Attendance
        att_frame = ttk.LabelFrame(self.daily_frame, text="出勤狀況")
        att_frame.pack(fill="x", padx=10, pady=5)
        self.att_tree = ttk.Treeview(att_frame, columns=("category", "scheduled", "present", "absent", "reason"), show="headings", height=3)
        for col, text in zip(self.att_tree["columns"], ["分類", "定員", "出勤", "欠勤", "理由"]):
            self.att_tree.heading(col, text=text)
            self.att_tree.column(col, width=100)
        self.att_tree.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        att_scroll = ttk.Scrollbar(att_frame, orient="vertical", command=self.att_tree.yview)
        self.att_tree.configure(yscroll=att_scroll.set)
        att_scroll.pack(side="right", fill="y")

        # Prepopulate
        self.att_tree.insert("", "end", values=("正社員", 0, 0, 0, ""))
        self.att_tree.insert("", "end", values=("契約/派遣", 0, 0, 0, ""))

        # Equipment logs
        equip_frame = ttk.LabelFrame(self.daily_frame, text="設備異常")
        equip_frame.pack(fill="x", padx=10, pady=5)
        self.equip_tree = ttk.Treeview(
            equip_frame,
            columns=("equip_id", "description", "start_time", "impact_qty", "action_taken", "image_path"),
            show="headings",
            height=4,
        )
        for col, text in zip(
            self.equip_tree["columns"],
            ["設備番号", "異常內容", "發生時刻", "影響數量", "對應內容", "圖片路徑"],
        ):
            self.equip_tree.heading(col, text=text)
            self.equip_tree.column(col, width=120)
        self.equip_tree.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Scrollbar(equip_frame, orient="vertical", command=self.equip_tree.yview).pack(side="right", fill="y")
        ttk.Button(equip_frame, text="新增", command=self._add_equipment_dialog).pack(side="right", padx=5, pady=5)

        # Lot logs
        lot_frame = ttk.LabelFrame(self.daily_frame, text="本日異常批次")
        lot_frame.pack(fill="x", padx=10, pady=5)
        self.lot_tree = ttk.Treeview(
            lot_frame,
            columns=("lot_id", "description", "status", "notes"),
            show="headings",
            height=4,
        )
        for col, text in zip(self.lot_tree["columns"], ["批號", "異常內容", "處置狀況", "特記事項"]):
            self.lot_tree.heading(col, text=text)
            self.lot_tree.column(col, width=150)
        self.lot_tree.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Scrollbar(lot_frame, orient="vertical", command=self.lot_tree.yview).pack(side="right", fill="y")
        ttk.Button(lot_frame, text="新增", command=self._add_lot_dialog).pack(side="right", padx=5, pady=5)

        # Summary
        summary_frame = ttk.LabelFrame(self.daily_frame, text="總結")
        summary_frame.pack(fill="x", padx=10, pady=5)
        self.summary_key = tk.Text(summary_frame, height=4)
        self.summary_issues = tk.Text(summary_frame, height=4)
        self.summary_counter = tk.Text(summary_frame, height=4)
        ttk.Label(summary_frame, text="Key Machine Output").grid(row=0, column=0, sticky="w")
        ttk.Label(summary_frame, text="Key Issues").grid(row=0, column=1, sticky="w")
        ttk.Label(summary_frame, text="Countermeasures").grid(row=0, column=2, sticky="w")
        self.summary_key.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.summary_issues.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.summary_counter.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        for i in range(3):
            summary_frame.columnconfigure(i, weight=1)

        # Actions
        action_frame = ttk.Frame(self.daily_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(action_frame, text="匯入 Excel（即將提供）", command=self._import_placeholder).pack(side="left", padx=5)
        ttk.Button(action_frame, text="提交", command=self._save_report).pack(side="right", padx=5)

    def _import_placeholder(self) -> None:
        messagebox.showinfo("匯入", "匯入功能將依指定格式完成後提供。")

    def _add_equipment_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("新增設備異常")
        entries: Dict[str, tk.Entry] = {}
        labels = ["設備番号", "異常內容", "發生時刻", "影響數量", "對應內容", "圖片檔路徑"]
        keys = ["equip_id", "description", "start_time", "impact_qty", "action_taken", "image_path"]
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(dialog, text=lbl).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            ent = ttk.Entry(dialog, width=40)
            ent.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = ent

        def select_image() -> None:
            path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")])
            if path:
                entries["image_path"].delete(0, tk.END)
                entries["image_path"].insert(0, path)

        ttk.Button(dialog, text="選擇圖片", command=select_image).grid(row=5, column=2, padx=5, pady=5)

        def confirm() -> None:
            values = [entries[k].get() for k in keys]
            self.equip_tree.insert("", "end", values=values)
            dialog.destroy()

        ttk.Button(dialog, text="新增", command=confirm).grid(row=6, column=0, columnspan=3, pady=10)

    def _add_lot_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("新增異常批次")
        labels = ["批號", "異常內容", "處置狀況", "特記事項"]
        entries: List[tk.Entry] = []
        for i, lbl in enumerate(labels):
            ttk.Label(dialog, text=lbl).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            ent = ttk.Entry(dialog, width=40)
            ent.grid(row=i, column=1, padx=5, pady=5)
            entries.append(ent)

        def confirm() -> None:
            values = [e.get() for e in entries]
            self.lot_tree.insert("", "end", values=values)
            dialog.destroy()

        ttk.Button(dialog, text="新增", command=confirm).grid(row=4, column=0, columnspan=2, pady=10)

    def _collect_attendance(self) -> List[Dict[str, str]]:
        data = []
        for item in self.att_tree.get_children():
            vals = self.att_tree.item(item, "values")
            data.append(
                {
                    "category": vals[0],
                    "scheduled_count": vals[1],
                    "present_count": vals[2],
                    "absent_count": vals[3],
                    "reason": vals[4],
                }
            )
        return data

    def _collect_equipment(self) -> List[Dict[str, str]]:
        data = []
        for item in self.equip_tree.get_children():
            vals = self.equip_tree.item(item, "values")
            data.append(
                {
                    "equip_id": vals[0],
                    "description": vals[1],
                    "start_time": vals[2],
                    "impact_qty": vals[3],
                    "action_taken": vals[4],
                    "image_path": vals[5] if len(vals) > 5 else None,
                }
            )
        return data

    def _collect_lots(self) -> List[Dict[str, str]]:
        data = []
        for item in self.lot_tree.get_children():
            vals = self.lot_tree.item(item, "values")
            data.append(
                {
                    "lot_id": vals[0],
                    "description": vals[1],
                    "status": vals[2],
                    "notes": vals[3],
                }
            )
        return data

    def _save_report(self) -> None:
        try:
            report_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("錯誤", "日期格式需為 YYYY-MM-DD")
            return

        attendance = self._collect_attendance()
        equipment = self._collect_equipment()
        lots = self._collect_lots()

        # Basic validation
        for idx, row in enumerate(attendance):
            for field in ["scheduled_count", "present_count", "absent_count"]:
                try:
                    val = int(row[field] or 0)
                    if val < 0:
                        messagebox.showerror("錯誤", f"出勤第 {idx+1} 列 {field} 不可為負數")
                        return
                    row[field] = val
                except ValueError:
                    messagebox.showerror("錯誤", f"出勤第 {idx+1} 列 {field} 需為數字")
                    return
        for idx, row in enumerate(equipment):
            try:
                val = int(row["impact_qty"] or 0)
                if val < 0:
                    messagebox.showerror("錯誤", f"設備異常第 {idx+1} 列影響數量不可為負數")
                    return
                row["impact_qty"] = val
            except ValueError:
                messagebox.showerror("錯誤", f"設備異常第 {idx+1} 列影響數量需為數字")
                return

        key_output = self.summary_key.get("1.0", tk.END).strip()
        issues = self.summary_issues.get("1.0", tk.END).strip()
        counter = self.summary_counter.get("1.0", tk.END).strip()

        try:
            with SessionLocal() as db:
                report = DailyReport(
                    date=report_date,
                    shift=self.shift_var.get(),
                    area=self.area_var.get(),
                    author_id=self.session_user["id"],
                    summary_key_output=key_output,
                    summary_issues=issues,
                    summary_countermeasures=counter,
                )
                db.add(report)
                db.flush()

                for row in attendance:
                    db.add(
                        AttendanceEntry(
                            report_id=report.id,
                            category=row["category"],
                            scheduled_count=row["scheduled_count"],
                            present_count=row["present_count"],
                            absent_count=row["absent_count"],
                            reason=row["reason"],
                        )
                    )
                for row in equipment:
                    db.add(
                        EquipmentLog(
                            report_id=report.id,
                            equip_id=row["equip_id"],
                            description=row["description"],
                            start_time=row["start_time"],
                            impact_qty=row["impact_qty"],
                            action_taken=row["action_taken"],
                            image_path=row["image_path"],
                        )
                    )
                for row in lots:
                    db.add(
                        LotLog(
                            report_id=report.id,
                            lot_id=row["lot_id"],
                            description=row["description"],
                            status=row["status"],
                            notes=row["notes"],
                        )
                    )

                db.commit()
            messagebox.showinfo("成功", "提交成功！")
        except Exception as exc:
            messagebox.showerror("錯誤", f"提交失敗：{exc}")

    # Report tab
    def _build_report_tab(self) -> None:
        self.report_notebook = ttk.Notebook(self.report_frame)
        self.report_notebook.pack(fill="both", expand=True)

        self.att_tab = ttk.Frame(self.report_notebook)
        self.equip_tab = ttk.Frame(self.report_notebook)
        self.lot_tab = ttk.Frame(self.report_notebook)

        self.report_notebook.add(self.att_tab, text="人員出勤報表")
        self.report_notebook.add(self.equip_tab, text="設備異常報表")
        self.report_notebook.add(self.lot_tab, text="異常 LOT 報表")

        self._build_attendance_report_tab()
        self._build_equipment_report_tab()
        self._build_lot_report_tab()

    def _load_reports(self) -> None:
        pass

    def _export_csv(self) -> None:
        pass

    # User management tab
    def _build_user_tab(self) -> None:
        frame = ttk.Frame(self.user_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.user_tree = ttk.Treeview(frame, columns=("id", "username", "role"), show="headings")
        for col, text in zip(self.user_tree["columns"], ["ID", "帳號", "角色"]):
            self.user_tree.heading(col, text=text)
            self.user_tree.column(col, width=120)
        self.user_tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(frame, orient="vertical", command=self.user_tree.yview).pack(side="left", fill="y")

        form = ttk.Frame(frame)
        form.pack(side="right", fill="y", padx=10)
        ttk.Label(form, text="帳號").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(form, text="密碼").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(form, text="角色").grid(row=2, column=0, padx=5, pady=5)
        self.new_user_var = tk.StringVar()
        self.new_pass_var = tk.StringVar()
        self.new_role_var = tk.StringVar(value="user")
        ttk.Entry(form, textvariable=self.new_user_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.new_pass_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.new_role_var, values=["user", "admin"], state="readonly").grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(form, text="新增使用者", command=self._add_user).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(form, text="重設密碼", command=self._reset_password).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(form, text="刪除使用者", command=self._delete_user).grid(row=5, column=0, columnspan=2, pady=5)

        self._refresh_users()

    def _refresh_users(self) -> None:
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        with SessionLocal() as db:
            users = db.query(User).all()
            for u in users:
                self.user_tree.insert("", "end", values=(u.id, u.username, u.role))

    def _add_user(self) -> None:
        username = self.new_user_var.get().strip()
        password = self.new_pass_var.get()
        role = self.new_role_var.get()
        if not username or not password:
            messagebox.showerror("錯誤", "帳號與密碼不可為空")
            return
        try:
            with SessionLocal() as db:
                exists = db.query(User).filter(User.username == username).first()
                if exists:
                    messagebox.showerror("錯誤", "帳號已存在")
                    return
                user = User(username=username, password_hash=hash_password(password), role=role)
                db.add(user)
                db.commit()
            self._refresh_users()
            messagebox.showinfo("成功", "已新增使用者")
        except Exception as exc:
            messagebox.showerror("錯誤", f"新增失敗：{exc}")

    def _reset_password(self) -> None:
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "請先選擇使用者")
            return
        item = self.user_tree.item(selected[0])
        user_id = item["values"][0]
        new_pw = self.new_pass_var.get()
        if not new_pw:
            messagebox.showerror("錯誤", "請輸入新密碼")
            return
        try:
            with SessionLocal() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    messagebox.showerror("錯誤", "找不到使用者")
                    return
                user.password_hash = hash_password(new_pw)
                db.commit()
            messagebox.showinfo("成功", "密碼已更新")
            self.new_pass_var.set("")
        except Exception as exc:
            messagebox.showerror("錯誤", f"更新失敗：{exc}")

    def _delete_user(self) -> None:
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "請先選擇使用者")
            return
        item = self.user_tree.item(selected[0])
        user_id = item["values"][0]
        if not messagebox.askyesno("確認", "確定要刪除該使用者？"):
            return
        try:
            with SessionLocal() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    messagebox.showerror("錯誤", "找不到使用者")
                    return
                db.delete(user)
                db.commit()
            self._refresh_users()
            messagebox.showinfo("成功", "已刪除使用者")
        except Exception as exc:
            messagebox.showerror("錯誤", f"刪除失敗：{exc}")


if __name__ == "__main__":
    app = HandoverApp()
    app.mainloop()
