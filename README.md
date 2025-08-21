# 🎬 Instagram Reels 自動觀看系統

> ⚠️ **重要警告**: 此專案僅供教育和學習目的使用，實際使用可能違反 Instagram 使用條款，可能導致帳號被封。請謹慎使用並自行承擔風險。

## 🔥 功能特色

- 🎯 **任務管理**: 建立、監控、停止觀看任務
- 📊 **即時監控**: 查看任務執行狀態和進度
- 🛡️ **安全機制**: 內建延遲和反檢測措施
- 📝 **日誌記錄**: 完整的操作記錄和錯誤追蹤
- 🎨 **現代 UI**: 使用 Vue 3 + Element Plus 構建
- ⚡ **高性能後端**: FastAPI + SQLAlchemy

## 🏗️ 技術架構

### 前端技術棧
- **框架**: Vue 3 + Vite
- **UI 組件**: Element Plus
- **狀態管理**: Pinia
- **樣式**: Tailwind CSS
- **HTTP 客戶端**: Axios

### 後端技術棧
- **框架**: FastAPI
- **資料庫**: SQLAlchemy + SQLite
- **自動化**: Selenium WebDriver
- **任務管理**: AsyncIO
- **日誌**: Loguru

## 📋 系統需求

- Python 3.8+
- Node.js 16+
- Chrome 瀏覽器 (用於 WebDriver)

## 🚀 快速開始

### 1. 克隆專案

```bash
git clone <repository-url>
cd ig_reels_viewer
```

### 2. 後端設置

```bash
cd backend

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 複製環境配置
cp ../.env.example .env
# 編輯 .env 檔案以符合你的設定

# 啟動後端服務
python main.py
```

### 3. 前端設置

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發服務器
npm run dev
```

### 4. 訪問應用

- 前端界面: http://localhost:3000
- 後端 API: http://localhost:8000
- API 文檔: http://localhost:8000/docs

## ⚙️ 配置選項

### 延遲設定
- **快速** (1-3秒): 適合測試，風險較高
- **正常** (3-5秒): 平衡的選擇
- **安全** (5-10秒): 較安全的設定
- **超安全** (10-20秒): 最安全但較慢

### 模擬操作
- **滾動**: 模擬用戶滾動行為
- **暫停**: 隨機暫停以模擬真實觀看
- **音量**: 調整音量控制

## 🛡️ 安全措施

### 反檢測機制
- 隨機 User Agent
- 隨機視窗大小
- 延遲隨機化
- 模擬人類行為
- 移除 WebDriver 標識

### 使用限制
- 最大並發任務數: 3
- 每任務最大觀看次數: 100
- 強制延遲機制

## 📊 監控功能

### 任務狀態
- ⏳ 等待中
- ▶️ 執行中
- ✅ 已完成
- ❌ 失敗
- 🛑 已停止

### 系統監控
- CPU 和記憶體使用率
- 任務統計
- 錯誤日誌
- 系統健康狀態

## 🔧 開發指南

### 項目結構

```
ig_reels_viewer/
├── frontend/                 # Vue 前端
│   ├── src/
│   │   ├── components/      # UI 組件
│   │   ├── views/          # 頁面組件
│   │   ├── stores/         # Pinia 狀態管理
│   │   └── services/       # API 服務
│   └── package.json
├── backend/                 # Python 後端
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── database/      # 資料庫模型
│   │   ├── services/      # 業務邏輯
│   │   └── core/          # 核心配置
│   ├── main.py           # 應用程式入口
│   └── requirements.txt
└── README.md
```

### API 端點

#### 任務管理
- `POST /api/tasks` - 建立新任務
- `GET /api/tasks` - 獲取任務列表
- `GET /api/tasks/{id}` - 獲取任務詳情
- `POST /api/tasks/{id}/stop` - 停止任務
- `POST /api/tasks/{id}/retry` - 重試任務
- `DELETE /api/tasks/{id}` - 刪除任務

#### 系統狀態
- `GET /api/system/status` - 系統狀態
- `GET /api/system/logs` - 系統日誌
- `POST /api/system/cleanup` - 清理舊資料

## ⚠️ 重要提醒

### 法律和倫理考量
1. **使用條款違反**: 自動化操作違反 Instagram 使用條款
2. **帳號風險**: 可能導致帳號被暫停或永久封禁
3. **法律責任**: 使用者需自行承擔所有法律責任
4. **倫理問題**: 人工增加觀看次數影響平台公平性

### 建議用途
- 學習 Web 自動化技術
- 研究反檢測機制
- 了解社交媒體平台運作
- 技術概念驗證

### 不建議用途
- 商業用途
- 大量操作
- 惡意行為
- 違法活動

## 🤝 貢獻指南

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 📄 許可證

此專案僅供教育目的使用。請查看 [LICENSE](LICENSE) 檔案了解詳細資訊。

## 📞 支援

如有問題，請：
1. 查看 [常見問題](docs/FAQ.md)
2. 搜尋現有 [Issues](issues)
3. 建立新的 Issue

---

**免責聲明**: 此工具僅供教育和學習目的。開發者不對因使用此工具而導致的任何後果負責。使用前請詳細閱讀 Instagram 使用條款並自行評估風險。
