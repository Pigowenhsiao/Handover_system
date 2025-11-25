# 多語言支持功能快速入門指南 (Quickstart Guide)

## 1. 系統架構概覽

多語言支持功能採用前端國際化和後端管理相結合的方式：
- 前端：使用 React-i18next 實現界面翻譯和即時語言切換
- 後端：提供 API 端點管理翻譯資源和語言設置
- 存儲：使用數據庫存儲翻譯內容，支持系統管理員維護

## 2. 開發環境設置

### 前端設置
1. 安裝依賴：
```bash
npm install i18next i18next-http-backend i18next-browser-languagedetector react-i18next
```

2. 配置 i18next (i18n.js):
```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)  // 從後端加載翻譯
  .use(LanguageDetector)  // 自動檢測語言
  .use(initReactI18next)
  .init({
    fallbackLng: 'ja',  // 默認為日文
    debug: true,
    interpolation: {
      escapeValue: false,  // React 會自動轉義
    },
    backend: {
      loadPath: '/api/languages/resources?lang={{lng}}&namespace={{ns}}',
    },
  });

export default i18n;
```

### 後端設置 (FastAPI)
1. 安裝依賴：
```bash
# 已包含在主項目中
```

2. 創建語言資源模型和端點 (已定義在 API 合約中)

## 3. 主要功能實現

### 1. 語言切換組件
- 實現按鈕或下拉選單讓用戶選擇語言
- 切換語言時更新界面內容
- 將用戶偏好保存到瀏覽器本地存儲

### 2. 翻譯資源管理
- 管理員界面可上傳、編輯、刪除翻譯資源
- 支援 JSON 格式的翻譯文件匯入/匯出
- 版本控制管理翻譯變更歷史

### 3. 界面組件國際化
- 匯現有組件以使用翻譯鍵而非硬編碼文本
- 確保界面支援不同語言文字長度變化
- 處理數字和日期格式本地化

## 4. 開發指南

### 添加新的翻譯鍵
1. 在對應語言的 JSON 文件中添加新的鍵值對
2. 在組件中使用 t() 函數引用翻譯鍵
3. 測試所有支援的語言確保正確翻譯

### 管理翻譯資源
1. 使用管理員界面或 API 端點進行翻譯資源的維護
2. 按功能模組組織翻譯鍵到不同的命名空間
3. 定期備份翻譯資源文件

## 5. 部署考量

### 性能優化
- 實施延遲載入策略，只載入當前語言資源
- 實施緩存策略以減少重複請求
- 優化翻譯文件大小以減少載入時間

### 安全性
- 確保只有管理員可以修改翻譯資源
- 驗證上傳的翻譯文件格式
- 防止惡意代碼注入翻譯內容

## 6. 測試指南

### 功能測試
- 驗證語言切換功能是否正常工作
- 檢查所有界面元素是否正確翻譯
- 測試默認語言設置是否正確

### 效能測試
- 測試語言切換的響應時間是否小於 500 毫秒
- 測試初次載入多語言資源的時間是否小於 1 秒
- 測試翻譯資源的緩存機制是否有效