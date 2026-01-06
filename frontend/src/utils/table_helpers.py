"""Treeview helpers for table setup and cleanup."""
import tkinter as tk
from tkinter import ttk


def clear_tree(tree):
    if tree is None:
        return
    if not tree.winfo_exists():
        return
    for item in tree.get_children():
        tree.delete(item)


def configure_treeview_columns(tree, columns, headers, widths=None):
    width_map = widths or {}
    default_width = width_map.get("__default__")
    for col in columns:
        tree.heading(col, text=headers.get(col, col))
        width = width_map.get(col, default_width)
        if width:
            tree.column(col, width=width)


def attach_vertical_scrollbar(parent, tree):
    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    return scrollbar


def bind_treeview_context_menu(tree, build_menu):
    def handler(event):
        row_id = tree.identify_row(event.y)
        if row_id and row_id not in tree.selection():
            tree.selection_set(row_id)
        menu = build_menu()
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    tree.bind("<Button-3>", handler)
    return handler
