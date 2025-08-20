# Instagram Reels Viewer - 測試指南

## 🔧 環境準備

### 前置需求檢查

1. **Java 17+**
   ```bash
   java -version
   # 應顯示 Java 17 或更高版本
   ```

2. **Node.js 16+**
   ```bash
   node --version
   npm --version
   # 應顯示 Node.js 16 或更高版本
   ```

3. **Chrome瀏覽器**
   - 確保已安裝最新版本的Chrome瀏覽器
   - Selenium會自動下載對應的ChromeDriver

## 🚀 啟動應用程式

### 方法一：使用批次檔（Windows推薦）

1. **同時啟動前後端**
   ```bash
   # 雙擊或執行
   start.bat
   ```

2. **分別啟動**
   ```bash
   # 後端
   start-backend.bat
   
   # 前端（在新的命令提示字元視窗）
   start-frontend.bat
   ```

### 方法二：手動啟動

1. **後端服務**
   ```bash
   cd backend
   mvn spring-boot:run
   ```
   - 服務將在 `http://localhost:8080` 啟動
   - 看到 "Started IgReelsViewerApplication" 表示啟動成功

2. **前端服務**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   - 服務將在 `http://localhost:5173` 啟動
   - 看到 "Local: http://localhost:5173" 表示啟動成功

## 🧪 功能測試

### 1. 基本功能測試

1. **訪問前端介面**
   - 開啟瀏覽器訪問 `http://localhost:5173`
   - 應看到Instagram Reels Viewer主頁面

2. **檢查統計資訊**
   - 主頁應顯示任務統計卡片（初始全為0）
   - 統計包括：等待中、執行中、已完成、失敗、已取消、總計

### 2. 任務建立測試

1. **有效URL測試**
   ```
   測試URL: https://www.instagram.com/reel/C1234567890/
   觀看次數: 3
   
   預期結果: 
   - 表單驗證通過
   - 任務建立成功
   - 顯示成功訊息
   - 任務出現在最近任務列表
   ```

2. **無效URL測試**
   ```
   測試URL: https://youtube.com/watch?v=123
   
   預期結果:
   - 表單驗證失敗
   - 顯示錯誤訊息："請輸入有效的Instagram Reels或貼文網址"
   ```

3. **邊界值測試**
   ```
   觀看次數: 0 -> 應顯示錯誤
   觀看次數: 101 -> 應顯示錯誤
   觀看次數: 1 -> 應通過驗證
   觀看次數: 100 -> 應通過驗證
   ```

### 3. 任務執行測試

⚠️ **注意：實際執行任務會訪問Instagram，請謹慎測試**

1. **測試流程**
   - 建立一個觀看次數為1的任務
   - 觀察任務狀態變化：PENDING → RUNNING → COMPLETED/FAILED
   - 檢查進度更新

2. **狀態檢查**
   - 點擊"更新"按鈕檢查任務狀態
   - 檢查完成時間是否正確設置

### 4. 歷史記錄測試

1. **訪問歷史頁面**
   - 點擊導航欄的"歷史記錄"
   - 應看到所有任務列表

2. **篩選功能**
   - 測試狀態篩選下拉選單
   - 測試URL關鍵字搜尋
   - 測試清除篩選按鈕

3. **操作功能**
   - 測試取消等待中的任務
   - 測試刪除已完成的任務
   - 測試批量清理功能

### 5. API測試

使用瀏覽器開發者工具或Postman測試API：

1. **建立任務**
   ```http
   POST http://localhost:8080/api/tasks
   Content-Type: application/json

   {
     "reelsUrl": "https://www.instagram.com/reel/test123/",
     "viewCount": 3
   }
   ```

2. **取得任務列表**
   ```http
   GET http://localhost:8080/api/tasks/recent?limit=5
   ```

3. **取得統計資訊**
   ```http
   GET http://localhost:8080/api/tasks/statistics
   ```

## 🐛 故障排除

### 常見問題

1. **後端啟動失敗**
   - 檢查Java版本是否正確
   - 檢查8080端口是否被占用
   - 查看控制台錯誤訊息

2. **前端啟動失敗**
   - 執行 `npm install` 安裝依賴
   - 檢查Node.js版本
   - 清除npm快取：`npm cache clean --force`

3. **ChromeDriver錯誤**
   - 確保Chrome瀏覽器已安裝
   - 檢查網路連接（WebDriverManager需要下載驅動）
   - 查看後端控制台的詳細錯誤訊息

4. **Instagram存取問題**
   - 檢查網路連接
   - 可能的速率限制或IP封鎖
   - 檢查Instagram是否正常運作

### 日誌檢查

1. **後端日誌**
   - 在後端控制台查看Spring Boot輸出
   - 注意ERROR和WARN級別的訊息

2. **前端日誌**
   - 開啟瀏覽器開發者工具 (F12)
   - 查看Console標籤的錯誤訊息
   - 查看Network標籤的API請求狀態

3. **H2資料庫控制台**
   - 訪問 `http://localhost:8080/h2-console`
   - JDBC URL: `jdbc:h2:mem:testdb`
   - 用戶名: `sa`
   - 密碼: (空白)

## 📊 效能測試

### 負載測試

1. **並行任務測試**
   - 建立多個任務（建議不超過5個）
   - 觀察系統資源使用情況
   - 檢查任務完成時間

2. **記憶體監控**
   - 監控Java程序記憶體使用
   - 監控Chrome程序數量
   - 長時間運行測試

### 安全測試

1. **輸入驗證**
   - 測試SQL注入攻擊
   - 測試XSS攻擊
   - 測試檔案路徑遍歷

2. **API安全**
   - 測試未授權訪問
   - 測試惡意請求

## ✅ 測試檢查清單

- [ ] 環境準備完成
- [ ] 前後端成功啟動
- [ ] 主頁面正常載入
- [ ] 統計資訊顯示正確
- [ ] 表單驗證正常工作
- [ ] 任務建立成功
- [ ] 任務狀態更新正常
- [ ] 歷史記錄頁面功能正常
- [ ] 篩選和搜尋功能正常
- [ ] API回應正常
- [ ] 錯誤處理正常
- [ ] 瀏覽器相容性測試
- [ ] 響應式設計測試

## ⚠️ 重要提醒

1. **僅供測試**: 此程式僅用於學習和技術研究
2. **遵守條款**: 測試時請遵守Instagram使用條款
3. **限制使用**: 避免大量或頻繁的測試請求
4. **網路禮儀**: 尊重Instagram的服務器資源
5. **法律責任**: 使用者自行承擔使用風險

測試完成後，請記得停止所有服務並清理測試資料。
