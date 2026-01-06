"""Settings storage helpers for handover_system."""
from pathlib import Path
import json

try:
    from models import _get_app_root
except Exception:
    _get_app_root = None


def get_settings_path():
    if _get_app_root is not None:
        root_dir = _get_app_root()
    else:
        root_dir = Path(__file__).resolve().parents[3]
    return Path(root_dir) / "handover_settings.json"


def load_settings_data():
    path = get_settings_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_settings_data(data):
    path = get_settings_path()
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False
