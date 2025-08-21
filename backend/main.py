"""
Instagram Reels 自動觀看系統 - 後端 API
⚠️ 警告：此工具僅供教育目的使用，請勿用於違反 Instagram 使用條款的行為
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import engine, get_db
from app.database.models import Base
from app.api.routes import tasks, system
from app.core.config import settings
from app.services.task_manager import TaskManager

# 配置日誌
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days"
)

# 任務管理器實例
task_manager = TaskManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時執行
    logger.info("🚀 啟動 Instagram Reels Viewer API...")
    
    # 創建資料庫表
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 資料庫初始化完成")
    
    # 啟動任務管理器
    await task_manager.start()
    logger.info("✅ 任務管理器啟動完成")
    
    yield
    
    # 關閉時執行
    logger.info("🛑 正在關閉 Instagram Reels Viewer API...")
    await task_manager.stop()
    logger.info("✅ 任務管理器已停止")

# 創建 FastAPI 應用程式
app = FastAPI(
    title="Instagram Reels Viewer API",
    description="""
    🎬 Instagram Reels 自動觀看系統 API
    
    ⚠️ **重要警告**：
    - 此 API 僅供教育和學習目的使用
    - 自動化操作可能違反 Instagram 使用條款
    - 使用者需自行承擔所有風險
    - 請勿用於商業用途或大量操作
    
    ## 功能特色
    - 🔧 任務管理：建立、監控、停止觀看任務
    - 📊 即時監控：查看任務執行狀態和進度
    - 🛡️ 安全機制：內建延遲和反檢測措施
    - 📝 日誌記錄：完整的操作記錄和錯誤追蹤
    """,
    version="1.0.0",
    contact={
        "name": "開發者",
        "email": "developer@example.com"
    },
    license_info={
        "name": "Educational Use Only",
        "url": "https://example.com/license"
    },
    lifespan=lifespan
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全域異常處理器
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全域異常: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "內部伺服器錯誤",
            "detail": str(exc) if settings.DEBUG else "請聯繫系統管理員"
        }
    )

# 健康檢查端點
@app.get("/", tags=["健康檢查"])
async def root():
    """根端點 - 系統健康檢查"""
    return {
        "message": "🎬 Instagram Reels Viewer API 正在運行",
        "status": "healthy",
        "version": "1.0.0",
        "warning": "⚠️ 此 API 僅供教育目的使用，請勿違反 Instagram 使用條款"
    }

@app.get("/health", tags=["健康檢查"])
async def health_check():
    """詳細健康檢查"""
    try:
        # 檢查資料庫連接
        db = next(get_db())
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"資料庫健康檢查失敗: {e}")
        db_status = "unhealthy"
    
    # 檢查任務管理器狀態
    task_manager_status = "healthy" if task_manager.is_running else "stopped"
    
    return {
        "status": "healthy",
        "timestamp": task_manager.get_current_time(),
        "components": {
            "database": db_status,
            "task_manager": task_manager_status,
            "api": "healthy"
        },
        "active_tasks": len(task_manager.active_tasks)
    }

# 註冊路由
app.include_router(tasks.router, prefix="/api", tags=["任務管理"])
app.include_router(system.router, prefix="/api", tags=["系統狀態"])

# 中間件：請求日誌
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📨 {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 回應狀態: {response.status_code}")
    return response

if __name__ == "__main__":
    logger.info("🎯 直接執行模式 - 啟動開發伺服器")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
