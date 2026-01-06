"""Shared registry for translated widgets."""


class I18nRegistry:
    def __init__(self):
        self._global = []
        self._page = []

    def register(self, widget, key, default, *, scope="global", translate=None):
        entry = {"widget": widget, "key": key, "default": default}
        if scope == "page":
            self._page.append(entry)
        else:
            self._global.append(entry)
        if translate is not None:
            widget.config(text=translate(key, default))
        return entry

    def apply(self, translate):
        for entry in self._global + self._page:
            widget = entry["widget"]
            if widget.winfo_exists():
                widget.config(text=translate(entry["key"], entry["default"]))

    def clear_page(self):
        self._page = []
