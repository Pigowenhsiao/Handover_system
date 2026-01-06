"""Helpers for report context and shift display mapping."""


def build_shift_display_options(shift_options, translate):
    day_label = translate("shift.day", "Day")
    night_label = translate("shift.night", "Night")
    code_map = {}
    display_map = {}
    display_values = []
    for code in shift_options:
        if code == "Day":
            display = day_label
        elif code == "Night":
            display = night_label
        else:
            display = code
        code_map[display] = code
        display_map[code] = display
        display_values.append(display)
    return display_values, code_map, display_map


def resolve_shift_code(display_value, code_map):
    return code_map.get(display_value, display_value)


def format_report_context_label(report_context, translate):
    unknown = translate("context.unknown", "未設定")
    date = report_context.get("date") or unknown
    shift = report_context.get("shift") or unknown
    area = report_context.get("area") or unknown
    template = translate(
        "context.currentReport",
        "目前日報：日期 {date}｜班別 {shift}｜區域 {area}",
    )
    return template.format(date=date, shift=shift, area=area)
