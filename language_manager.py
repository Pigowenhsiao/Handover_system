"""
語言資源管理系統 - 基於 Python 和 SQLite
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, Dict, List
import threading
import time

class LanguageResourceManager:
    """
    語言資源管理類
    用於管理多語言翻譯資源
    """
    
    def __init__(self, db_path="language_resources.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化數據庫表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 創建語言資源表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS language_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_code TEXT NOT NULL,
                resource_key TEXT NOT NULL,
                resource_value TEXT NOT NULL,
                namespace TEXT DEFAULT 'common',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by INTEGER DEFAULT NULL,
                UNIQUE(language_code, resource_key, namespace)
            )
        """)
        
        # 創建語言設置表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS language_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                language_code TEXT NOT NULL,
                is_default BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, language_code)
            )
        """)
        
        # 創建語言包表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS language_packs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_code TEXT NOT NULL,
                pack_name TEXT NOT NULL,
                version TEXT DEFAULT '1.0.0',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 初始化默認語言設置 (默認為日文)
        cursor.execute("""
            INSERT OR IGNORE INTO language_settings 
            (user_id, language_code, is_default, is_active) 
            VALUES (NULL, 'ja', TRUE, TRUE)
        """)
        
        # 初始化默認語言包
        default_packs = [
            ('ja', 'Japanese Pack'),
            ('en', 'English Pack'),
            ('zh', 'Chinese Pack')
        ]
        for code, name in default_packs:
            cursor.execute("""
                INSERT OR IGNORE INTO language_packs 
                (language_code, pack_name, is_active) 
                VALUES (?, ?, TRUE)
            """, (code, name))
        
        conn.commit()
        conn.close()
    
    def get_language_resources(self, language_code: str, namespace: str = 'common') -> Dict:
        """獲取指定語言和命名空間的翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT resource_key, resource_value 
            FROM language_resources 
            WHERE language_code = ? AND namespace = ?
        """, (language_code, namespace))
        
        results = cursor.fetchall()
        conn.close()
        
        # 將結果轉換為字典格式
        resources = {}
        for key, value in results:
            # 處理嵌套鍵（用點號分隔）
            keys = key.split('.')
            current_dict = resources
            
            # 遞歸構建嵌套字典結構
            for k in keys[:-1]:
                if k not in current_dict:
                    current_dict[k] = {}
                current_dict = current_dict[k]
            
            # 設置最終值
            current_dict[keys[-1]] = value
        
        return resources
    
    def get_resource(self, language_code: str, resource_key: str, namespace: str = 'common') -> Optional[str]:
        """獲取單個翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT resource_value 
            FROM language_resources 
            WHERE language_code = ? AND resource_key = ? AND namespace = ?
        """, (language_code, resource_key, namespace))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def add_resource(self, language_code: str, resource_key: str, resource_value: str, namespace: str = 'common'):
        """添加翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO language_resources 
                (language_code, resource_key, resource_value, namespace) 
                VALUES (?, ?, ?, ?)
            """, (language_code, resource_key, resource_value, namespace))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 如果資源已存在，則更新它
            cursor.execute("""
                UPDATE language_resources 
                SET resource_value = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE language_code = ? AND resource_key = ? AND namespace = ?
            """, (resource_value, language_code, resource_key, namespace))
            
            conn.commit()
            return True
        finally:
            conn.close()
    
    def update_resource(self, resource_id: int, resource_value: str):
        """更新翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE language_resources 
            SET resource_value = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (resource_value, resource_id))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    
    def delete_resource(self, resource_id: int):
        """刪除翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM language_resources WHERE id = ?", (resource_id,))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    
    def search_resources(self, search_term: str = "", language_code: str = "", namespace: str = "") -> List[Dict]:
        """搜索翻譯資源"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT id, language_code, resource_key, resource_value, namespace FROM language_resources WHERE 1=1"
        params = []
        
        if search_term:
            query += " AND (resource_key LIKE ? OR resource_value LIKE ?)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
        
        if language_code:
            query += " AND language_code = ?"
            params.append(language_code)
        
        if namespace:
            query += " AND namespace = ?"
            params.append(namespace)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'language_code': row[1],
                'resource_key': row[2],
                'resource_value': row[3],
                'namespace': row[4]
            }
            for row in results
        ]
    
    def get_all_languages(self) -> List[str]:
        """獲取所有支援的語言代碼"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT language_code FROM language_resources")
        results = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in results if row[0]]


class TranslationManager:
    """
    翻譯管理類
    提供應用程序中的翻譯功能
    """
    
    def __init__(self, resource_manager: LanguageResourceManager):
        self.resource_manager = resource_manager
        self.current_language = "ja"  # 默認為日文
        self.resources_cache = {}
        self.supported_languages = ["ja", "en", "zh"]
        
        # 預加載默認語言資源
        self.load_language_resources(self.current_language)
    
    def change_language(self, language_code: str) -> bool:
        """切換當前語言"""
        if language_code not in self.supported_languages:
            return False
        
        self.current_language = language_code
        self.load_language_resources(language_code)
        return True
    
    def load_language_resources(self, language_code: str):
        """載入指定語言的資源到緩存"""
        resources = self.resource_manager.get_language_resources(language_code)
        self.resources_cache[language_code] = resources
    
    def t(self, key: str, default_value: str = "") -> str:
        """獲取翻譯文本"""
        # 檢查緩存中是否有當前語言的資源
        if self.current_language not in self.resources_cache:
            self.load_language_resources(self.current_language)
        
        # 從緩存中獲取資源
        resources = self.resources_cache.get(self.current_language, {})
        
        # 使用鍵路徑獲取值 (支持嵌套鍵，如 'header.title')
        keys = key.split('.')
        current = resources
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                # 如果在當前語言中找不到，嘗試回退到日文
                ja_resources = self.resources_cache.get('ja', {})
                ja_current = ja_resources
                for jk in keys:
                    if isinstance(ja_current, dict) and jk in ja_current:
                        ja_current = ja_current[jk]
                    else:
                        return default_value or key
                return ja_current
        
        return str(current) if current is not None else (default_value or key)
    
    def get_current_language(self) -> str:
        """獲取當前語言"""
        return self.current_language
    
    def get_supported_languages(self) -> List[str]:
        """獲取支援的語言列表"""
        return self.supported_languages


class AppLanguageManager:
    """
    應用程序語言管理器
    結合資源管理和翻譯功能
    """
    
    def __init__(self, db_path="language_resources.db"):
        self.resource_manager = LanguageResourceManager(db_path)
        self.translation_manager = TranslationManager(self.resource_manager)
        
        # 初始化默認翻譯資源
        self._init_default_translations()
    
    def _init_default_translations(self):
        """初始化默認翻譯資源"""
        default_translations = {
            "ja": {
                "common": {
                    "title": "電子交接系統",
                    "language": "言語",
                    "switchLanguage": "言語切替",
                    "settings": "設定",
                    "logout": "ログアウト",
                    "login": "ログイン",
                    "username": "ユーザー名",
                    "password": "パスワード",
                    "save": "保存",
                    "cancel": "キャンセル",
                    "create": "新規作成",
                    "update": "更新",
                    "delete": "削除",
                    "search": "検索",
                    "edit": "編集",
                    "confirm": "確認",
                    "yes": "はい",
                    "no": "いいえ",
                    "loading": "読み込み中...",
                    "error": "エラー",
                    "success": "成功"
                },
                "header": {
                    "title": "電子交接システム",
                    "languageSwitch": "言語切替",
                    "login": "ログイン",
                    "logout": "ログアウト"
                },
                "navigation": {
                    "home": "ホーム",
                    "reports": "レポート",
                    "settings": "設定",
                    "admin": "管理"
                }
            },
            "en": {
                "common": {
                    "title": "Digital Handover System",
                    "language": "Language",
                    "switchLanguage": "Switch Language",
                    "settings": "Settings",
                    "logout": "Logout",
                    "login": "Login",
                    "username": "Username",
                    "password": "Password",
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
                    "success": "Success"
                },
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
                }
            },
            "zh": {
                "common": {
                    "title": "電子交接系統",
                    "language": "語言",
                    "switchLanguage": "切換語言",
                    "settings": "設定",
                    "logout": "登出",
                    "login": "登入",
                    "username": "使用者名稱",
                    "password": "密碼",
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
                    "success": "成功"
                },
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
                }
            }
        }
        
        # 添加默認翻譯到數據庫
        for lang_code, namespaces in default_translations.items():
            for namespace, translations in namespaces.items():
                for key, value in translations.items():
                    full_key = f"{namespace}.{key}" if namespace != "common" else key
                    self.resource_manager.add_resource(lang_code, full_key, value, namespace)
    
    def translate(self, key: str, default_value: str = "") -> str:
        """翻譯文本"""
        return self.translation_manager.t(key, default_value)
    
    def change_language(self, language_code: str) -> bool:
        """切換語言"""
        return self.translation_manager.change_language(language_code)
    
    def get_current_language(self) -> str:
        """獲取當前語言"""
        return self.translation_manager.get_current_language()
    
    def get_supported_languages(self) -> List[str]:
        """獲取支援語言"""
        return self.translation_manager.get_supported_languages()
    
    def get_resource_manager(self) -> LanguageResourceManager:
        """獲取資源管理器"""
        return self.resource_manager