# Instagram Reels Viewer

> ⚠️ **重要聲明**: 此專案僅供學習研究使用，請遵守Instagram使用條款和相關法律法規。

## 專案簡介

Instagram Reels Viewer 是一個自動化觀看Instagram Reels的程式，支援：

- 🎯 輸入Instagram Reels網址和觀看次數
- 🤖 自動執行觀看任務
- 📊 即時追蹤任務執行狀態
- 📈 統計資料分析
- 🎨 現代化的網頁介面

## 技術架構

### 後端 (Java Spring Boot)
- **框架**: Spring Boot 3.2.0
- **自動化**: Selenium WebDriver
- **資料庫**: H2 (記憶體資料庫)
- **API**: REST API
- **異步處理**: Spring @Async

### 前端 (Vue.js)
- **框架**: Vue 3 + Composition API
- **UI庫**: Element Plus
- **狀態管理**: Pinia
- **路由**: Vue Router
- **HTTP客戶端**: Axios
- **建構工具**: Vite

## 功能特點

### 🎯 核心功能
1. **任務建立**: 輸入Instagram Reels URL和觀看次數
2. **自動觀看**: 使用無頭瀏覽器模擬真實使用者觀看
3. **狀態追蹤**: 即時更新任務執行狀態
4. **歷史記錄**: 完整的任務執行歷史

### 📊 管理功能
- 任務狀態監控（等待中、執行中、已完成、失敗、已取消）
- 統計資料儀表板
- 任務篩選和搜尋
- 批量操作

### 🛡️ 安全特性
- URL格式驗證
- 觀看次數限制
- 錯誤處理和重試機制
- 防止過度使用

## 快速開始

### 前置需求
- Java 17+
- Node.js 16+
- Maven 3.6+
- Chrome瀏覽器 (用於Selenium)

### 1. 啟動後端服務

```bash
cd backend
mvn spring-boot:run
```

後端服務將在 `http://localhost:8080` 啟動

### 2. 啟動前端服務

```bash
cd frontend
npm install
npm run dev
```

前端服務將在 `http://localhost:5173` 啟動

### 3. 訪問應用

開啟瀏覽器訪問 `http://localhost:5173`

## API文檔

### 任務管理
- `POST /api/tasks` - 建立新任務
- `GET /api/tasks` - 取得所有任務
- `GET /api/tasks/recent` - 取得最近任務
- `GET /api/tasks/{id}` - 取得特定任務
- `PUT /api/tasks/{id}/cancel` - 取消任務
- `DELETE /api/tasks/{id}` - 刪除任務

### 統計資訊
- `GET /api/tasks/statistics` - 取得統計資料
- `GET /api/tasks/running/count` - 取得執行中任務數量

## 項目結構

```
ig_reels_viewer/
├── backend/                    # Java Spring Boot後端
│   ├── src/main/java/
│   │   └── com/example/igreels/
│   │       ├── IgReelsViewerApplication.java
│   │       ├── config/         # 配置類別
│   │       ├── controller/     # REST控制器
│   │       ├── model/          # 資料模型
│   │       ├── repository/     # 資料存取層
│   │       └── service/        # 業務邏輯層
│   ├── src/main/resources/
│   │   └── application.yml     # 應用配置
│   └── pom.xml                # Maven依賴配置
│
├── frontend/                   # Vue.js前端
│   ├── src/
│   │   ├── components/         # Vue組件
│   │   ├── services/          # API服務
│   │   ├── stores/            # Pinia狀態管理
│   │   ├── views/             # 頁面組件
│   │   ├── router/            # 路由配置
│   │   ├── App.vue            # 根組件
│   │   └── main.js            # 應用入口
│   ├── package.json           # npm依賴配置
│   └── vite.config.js         # Vite建構配置
│
└── README.md                  # 專案說明
```

## 開發指南

### 後端開發
- 使用Spring Boot DevTools進行熱重載
- H2控制台: `http://localhost:8080/h2-console`
- API文檔: `http://localhost:8080/swagger-ui.html` (如已配置)

### 前端開發
- 使用Vite熱重載
- Vue DevTools擴展程式用於除錯
- Element Plus組件庫文檔: https://element-plus.org/

### 程式碼風格
- Java: 遵循Google Java Style Guide
- JavaScript/Vue: 使用ESLint + Prettier

## 注意事項

### ⚠️ 重要警告
1. **使用條款**: 此工具可能違反Instagram使用條款，請謹慎使用
2. **法律責任**: 使用者需自行承擔使用此工具的法律責任
3. **速率限制**: 避免過度使用，以免IP被封鎖
4. **僅供學習**: 此專案僅用於技術學習和研究目的

### 🛡️ 最佳實踐
- 限制觀看次數（建議不超過20次）
- 設置合理的間隔時間
- 監控系統資源使用
- 定期清理任務歷史

## 故障排除

### 常見問題
1. **ChromeDriver錯誤**: 確保Chrome瀏覽器已安裝
2. **網路連接問題**: 檢查Instagram是否可訪問
3. **記憶體不足**: 調整JVM記憶體設置
4. **埠號衝突**: 修改配置檔案中的埠號設置

### 日誌檢查
- 後端日誌: 在控制台查看Spring Boot輸出
- 前端日誌: 在瀏覽器開發者工具Console查看

## 貢獻指南

1. Fork此專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟Pull Request

## 授權

此專案採用MIT授權條款 - 詳見[LICENSE](LICENSE)檔案

## 免責聲明

此軟體僅供教育和研究目的。使用者使用此軟體時需遵守所有相關的法律法規和服務條款。開發者不對使用此軟體造成的任何後果負責。
