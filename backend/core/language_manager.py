"""
語言管理器模組
實現多語言支持功能
"""
import json
import os
from typing import Dict, Optional


class LanguageManager:
    """
    語言管理器
    負責管理多語言資源並提供翻譯功能
    """

    def __init__(self, locales_dir: str = "frontend/public/locales"):
        self.locales_dir = locales_dir
        self.current_language = "ja"  # 默認為日文
        self.translations = {}

        # 支援的語言
        self.supported_languages = ["ja", "zh", "en"]

        # 加載所有語言資源
        self.load_all_translations()

    def load_all_translations(self):
        """加載所有支援語言的翻譯資源"""
        for lang_code in self.supported_languages:
            self.translations[lang_code] = self.load_language_translations(lang_code)

    def load_language_translations(self, lang_code: str) -> Dict:
        """加載特定語言的翻譯資源"""
        try:
            file_path = os.path.join(self.locales_dir, f"{lang_code}.json")
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 找不到語言文件 {file_path}")
            # 返回默認翻譯
            return self.get_default_translations(lang_code)
        except json.JSONDecodeError:
            print(f"錯誤: 語言文件 {file_path} 格式無效")
            return {}

    def get_default_translations(self, lang_code: str) -> Dict:
        """獲取默認翻譯資源"""
        defaults = {
            "ja": {
                "header": {
                    "title": "電子交接系統",
                    "languageSwitch": "言語切替",
                    "login": "ログイン",
                    "logout": "ログアウト"
                },
                "navigation": {
                    "home": "ホーム",
                    "reports": "レポート",
                    "settings": "設定",
                    "admin": "管理"
                },
                "common": {
                    "date": "日付",
                    "shift": "シフト",
                    "area": "区域",
                    "save": "保存",
                    "cancel": "キャンセル",
                    "create": "作成",
                    "update": "更新",
                    "delete": "削除",
                    "search": "検索",
                    "edit": "編集",
                    "confirm": "確認",
                    "yes": "はい",
                    "no": "いいえ",
                    "loading": "読み込み中...",
                    "error": "エラー",
                    "success": "成功",
                    "scheduled": "定員",
                    "present": "出勤",
                    "absent": "欠勤",
                    "reason": "理由",
                    "regular": "正社員",
                    "contractor": "契約社員"
                },
                "attendance": {
                    "regular": "正社員",
                    "contractor": "契約社員",
                    "input": "出勤入力",
                    "records": "出勤記録"
                },
                "equipment": {
                    "equipId": "設備ID",
                    "startTime": "発生時刻",
                    "description": "異常内容",
                    "impactQty": "影響数量",
                    "actionTaken": "対応内容",
                    "image": "画像"
                },
                "lot": {
                    "lotId": "ロットNO",
                    "status": "処置状況",
                    "notes": "特記事項"
                },
                "summary": {
                    "keyOutput": "Key Machine Output",
                    "issues": "Key Issues",
                    "countermeasures": "Countermeasures"
                }
            },
            "zh": {
                "header": {
                    "title": "電子交接系統",
                    "languageSwitch": "語言切換",
                    "login": "登入",
                    "logout": "登出"
                },
                "navigation": {
                    "home": "首頁",
                    "reports": "報表",
                    "settings": "設定",
                    "admin": "管理"
                },
                "common": {
                    "date": "日期",
                    "shift": "班別",
                    "area": "區域",
                    "save": "保存",
                    "cancel": "取消",
                    "create": "新增",
                    "update": "更新",
                    "delete": "刪除",
                    "search": "搜尋",
                    "edit": "編輯",
                    "confirm": "確認",
                    "yes": "是",
                    "no": "否",
                    "loading": "載入中...",
                    "error": "錯誤",
                    "success": "成功",
                    "scheduled": "定員",
                    "present": "出勤",
                    "absent": "欠勤",
                    "reason": "理由",
                    "regular": "正社員",
                    "contractor": "契約社員"
                },
                "attendance": {
                    "regular": "正社員",
                    "contractor": "契約社員",
                    "input": "出勤輸入",
                    "records": "出勤記錄"
                },
                "equipment": {
                    "equipId": "設備ID",
                    "startTime": "發生時刻",
                    "description": "異常內容",
                    "impactQty": "影響數量",
                    "actionTaken": "對應內容",
                    "image": "圖片"
                },
                "lot": {
                    "lotId": "批號",
                    "status": "處置狀況",
                    "notes": "特記事項"
                },
                "summary": {
                    "keyOutput": "Key Machine Output",
                    "issues": "Key Issues",
                    "countermeasures": "Countermeasures"
                }
            },
            "en": {
                "header": {
                    "title": "Digital Handover System",
                    "languageSwitch": "Language Switch",
                    "login": "Login",
                    "logout": "Logout"
                },
                "navigation": {
                    "home": "Home",
                    "reports": "Reports",
                    "settings": "Settings",
                    "admin": "Admin"
                },
                "common": {
                    "date": "Date",
                    "shift": "Shift",
                    "area": "Area",
                    "save": "Save",
                    "cancel": "Cancel",
                    "create": "Create",
                    "update": "Update",
                    "delete": "Delete",
                    "search": "Search",
                    "edit": "Edit",
                    "confirm": "Confirm",
                    "yes": "Yes",
                    "no": "No",
                    "loading": "Loading...",
                    "error": "Error",
                    "success": "Success",
                    "scheduled": "Scheduled",
                    "present": "Present",
                    "absent": "Absent",
                    "reason": "Reason",
                    "regular": "Regular Staff",
                    "contractor": "Contractor Staff"
                },
                "attendance": {
                    "regular": "Regular",
                    "contractor": "Contractor",
                    "input": "Attendance Input",
                    "records": "Attendance Records"
                },
                "equipment": {
                    "equipId": "Equipment ID",
                    "startTime": "Start Time",
                    "description": "Description",
                    "impactQty": "Impact Qty",
                    "actionTaken": "Action Taken",
                    "image": "Image"
                },
                "lot": {
                    "lotId": "Lot ID",
                    "status": "Status",
                    "notes": "Notes"
                },
                "summary": {
                    "keyOutput": "Key Machine Output",
                    "issues": "Key Issues",
                    "countermeasures": "Countermeasures"
                }
            }
        }

        return defaults.get(lang_code, {})

    def get_text(self, key: str, default_text: str = None) -> str:
        """
        獲取指定鍵的翻譯文本
        :param key: 翻譯鍵 (例如: "header.title")
        :param default_text: 默認文本
        :return: 翻譯後的文本或默認文本
        """
        try:
            # 分割鍵以支持嵌套結構 (例如: "header.title")
            keys = key.split('.')
            current_dict = self.translations[self.current_language]

            for k in keys:
                current_dict = current_dict.get(k, {})

            if isinstance(current_dict, str):
                return current_dict
            else:
                # 如果找不到確切的鍵，返回默認值或鍵本身
                return default_text or key
        except (AttributeError, TypeError):
            # 如果當前語言中找不到翻譯，則檢查其他語言
            for lang_code in self.supported_languages:
                if lang_code != self.current_language:
                    try:
                        current_dict = self.translations[lang_code]
                        for k in keys:
                            current_dict = current_dict.get(k, {})
                        
                        if isinstance(current_dict, str):
                            return current_dict
                    except (KeyError, TypeError, AttributeError):
                        continue

            # 如果所有語言都沒有找到，返回默認文本或鍵值
            return default_text or key

    def set_language(self, language_code: str) -> bool:
        """
        設置當前語言
        :param language_code: 語言代碼
        :return: 設置成功與否
        """
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        else:
            print(f"不支援的語言代碼: {language_code}")
            return False

    def get_current_language(self) -> str:
        """
        獲取當前語言代碼
        :return: 當前語言代碼
        """
        return self.current_language

    def get_supported_languages(self) -> list:
        """
        獲取支援的語言列表
        :return: 支援的語言代碼列表
        """
        return self.supported_languages

    def refresh_translations(self):
        """刷新所有翻譯資源（從文件重新加載）"""
        self.load_all_translations()

    def update_translation(self, key: str, new_text: str, language_code: str = None):
        """
        更新翻譯資源
        :param key: 翻譯鍵
        :param new_text: 新的翻譯文本
        :param language_code: 語言代碼，默認為當前語言
        """
        lang_code = language_code or self.current_language
        if lang_code not in self.supported_languages:
            print(f"不支援的語言代碼: {lang_code}")
            return False

        # 分割鍵以支持嵌套結構
        keys = key.split('.')
        current_dict = self.translations[lang_code]

        # 導航到最終字典位置（除了最後一個鍵）
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = {}
            current_dict = current_dict[k]

        # 設置最終值
        current_dict[keys[-1]] = new_text

        return True


# 創建全局語言管理器實例
lang_manager = LanguageManager()