"""UI helper functions for shared layout patterns."""
import tkinter as tk
from tkinter import ttk


def create_section_header(parent, text, *, style=None, font=None):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=text, style=style, font=font)
    label.pack(side="left")
    return frame, label


def create_labeled_input(
    parent,
    row,
    text,
    *,
    label_column=0,
    field_column=1,
    variable=None,
    widget_type="entry",
    width=20,
    values=None,
    label_font=None,
    entry_style=None,
    label_padx=0,
    label_pady=0,
    field_padx=0,
    field_pady=0,
    column_span=1,
    state=None,
    widget_kwargs=None,
):
    label = ttk.Label(parent, text=text, font=label_font)
    label.grid(
        row=row,
        column=label_column,
        sticky="w",
        padx=label_padx,
        pady=label_pady,
    )

    if variable is None:
        variable = tk.StringVar()

    widget_opts = dict(widget_kwargs or {})
    if widget_type == "combo":
        widget = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values or [],
            state=state or "readonly",
            width=width,
            **widget_opts,
        )
    else:
        widget = ttk.Entry(
            parent,
            textvariable=variable,
            width=width,
            style=entry_style,
            **widget_opts,
        )
        if state:
            widget.configure(state=state)

    widget.grid(
        row=row,
        column=field_column,
        sticky="ew",
        padx=(field_padx, 0),
        pady=field_pady,
        columnspan=column_span,
    )
    parent.columnconfigure(field_column, weight=1)
    return label, widget, variable


def build_button_row(parent, specs, *, default_side=tk.LEFT):
    frame = ttk.Frame(parent)
    buttons = {}
    for spec in specs:
        key = spec.get("key")
        options = dict(spec.get("options", {}))
        btn = ttk.Button(frame, **options)
        pack_opts = dict(spec.get("pack", {}))
        if "side" not in pack_opts:
            pack_opts["side"] = spec.get("side", default_side)
        btn.pack(**pack_opts)
        if key:
            buttons[key] = btn
    return frame, buttons
