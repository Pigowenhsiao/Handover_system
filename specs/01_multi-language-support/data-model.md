# 多語言支持功能數據模型 (Data Model)

## 1. 語言資源模型 (LanguageResource Model)
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- language_code (VARCHAR(10), NOT NULL)  # 例如: "zh", "ja", "en"
- resource_key (VARCHAR(255), NOT NULL)  # 翻譯鍵，例如: "header.title", "button.save"
- resource_value (TEXT, NOT NULL)        # 翻譯值，例如: "標題", "タイトル", "Title"
- namespace (VARCHAR(100), DEFAULT 'common') # 命名空間，例如: "common", "validation", "dashboard"
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- updated_by (INTEGER, FOREIGN KEY → User.id) # 更新此翻譯的用戶

### 關係
- 多對一關係: LanguageResource → User (updated_by)

## 2. 語言設置模型 (LanguageSetting Model)
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- user_id (INTEGER, FOREIGN KEY → User.id)  # 關聯到用戶，可選，NULL 表示系統範圍設置
- language_code (VARCHAR(10), NOT NULL)     # 例如: "zh", "ja", "en"
- is_default (BOOLEAN, DEFAULT FALSE)      # 是否為默認語言
- is_active (BOOLEAN, DEFAULT TRUE)         # 該語言是否啟用
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)

### 關係
- 多對一關係: LanguageSetting → User (user_id)

## 3. 界面組件模型 (UIComponent Model) - 參考用
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- component_name (VARCHAR(100), NOT NULL)  # 例如: "Header", "Button", "FormLabel"
- component_path (VARCHAR(255))            # 組件在應用中的路徑
- supported_languages (JSON)               # 支援的語言列表，例如: ["zh", "ja", "en"]
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)

## 4. 語言包模型 (LanguagePack Model)
### 欄位定義
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- language_code (VARCHAR(10), NOT NULL)      # 例如: "zh", "ja", "en"
- pack_name (VARCHAR(100), NOT NULL)         # 語言包名稱，例如: "Chinese Pack", "Japanese Pack"
- version (VARCHAR(20), DEFAULT "1.0.0")     # 語言包版本
- is_active (BOOLEAN, DEFAULT TRUE)          # 該語言包是否啟用
- created_at (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- updated_at (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)

## 5. 數據驗證規則
- LanguageResource.language_code: 限制為 'zh', 'ja', 'en' 三種值
- LanguageResource.resource_key: 必須符合命名規則 (字母、數字、點號、下劃線)
- LanguageSetting.language_code: 限制為 'zh', 'ja', 'en' 三種值
- LanguageSetting.is_default: 在同一用戶或系統範圍內只能有一個語言設為默認

## 6. 索引建議
- LanguageResource.language_code: 提升按語言查詢翻譯的性能
- LanguageResource.resource_key: 提升按鍵查詢翻譯的性能
- LanguageSetting.user_id: 提升用戶語言設置查詢性能
- LanguageResource.namespace: 提升按命名空間查詢翻譯的性能