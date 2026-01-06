"""Helpers for Excel/CSV import flows."""
import os
import tkinter as tk
from tkinter import ttk
import pandas as pd


def _select_sheet_name(parent, title, sheet_names, default, label, ok_label, theme):
    if len(sheet_names) <= 1:
        return sheet_names[0] if sheet_names else default

    picker = tk.Toplevel(parent)
    if theme and "background" in theme:
        picker.configure(background=theme["background"])
    picker.title(title)
    ttk.Label(picker, text=label).pack(padx=10, pady=5)
    sheet_var = tk.StringVar(value=default)
    combo = ttk.Combobox(picker, textvariable=sheet_var, values=sheet_names, state="readonly")
    combo.pack(padx=10, pady=5)
    chosen = {"name": default}

    def confirm():
        chosen["name"] = sheet_var.get()
        picker.destroy()

    ttk.Button(picker, text=ok_label, command=confirm).pack(pady=8)
    picker.grab_set()
    picker.wait_window()
    return chosen["name"]


def open_excel_workbook(
    path,
    *,
    parent=None,
    title=None,
    select_label=None,
    ok_label="OK",
    theme=None,
    preferred_sheet=None,
):
    xls = pd.ExcelFile(path)
    sheet_names = sorted(xls.sheet_names, key=str.lower)
    sheet_name = preferred_sheet if preferred_sheet in sheet_names else sheet_names[0]
    if parent is not None and title and select_label:
        sheet_name = _select_sheet_name(
            parent,
            title,
            sheet_names,
            sheet_name,
            select_label,
            ok_label,
            theme,
        )
    return xls, sheet_name


def read_table(path, header=None, *, xls=None, sheet_name=None):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".txt"):
        return pd.read_csv(path, header=header, sep=None, engine="python")
    if xls is None:
        xls = pd.ExcelFile(path)
    return pd.read_excel(xls, sheet_name=sheet_name, header=header)
