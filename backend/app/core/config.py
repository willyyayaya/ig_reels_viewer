"""
應用程式配置設定
"""

import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """應用程式設定"""
    
    # 基本設定
    APP_NAME: str = "Instagram Reels Viewer"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 伺服器設定
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS 設定
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite 預設埠
        "http://127.0.0.1:5173"
    ]
    
    # 資料庫設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ig_reels_viewer.db")
    
    # 安全設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    
    # Instagram 自動化設定
    MAX_CONCURRENT_TASKS: int = int(os.getenv("MAX_CONCURRENT_TASKS", 3))
    DEFAULT_VIEW_DELAY: int = int(os.getenv("DEFAULT_VIEW_DELAY", 5))  # 秒
    MAX_VIEWS_PER_TASK: int = int(os.getenv("MAX_VIEWS_PER_TASK", 100))
    
    # WebDriver 設定
    WEBDRIVER_TIMEOUT: int = int(os.getenv("WEBDRIVER_TIMEOUT", 30))
    HEADLESS_MODE: bool = os.getenv("HEADLESS_MODE", "True").lower() == "true"
    
    # 反檢測設定
    USE_PROXY: bool = os.getenv("USE_PROXY", "False").lower() == "true"
    PROXY_LIST: str = os.getenv("PROXY_LIST", "")
    USER_AGENT_ROTATION: bool = os.getenv("USER_AGENT_ROTATION", "True").lower() == "true"
    
    # 任務設定
    TASK_CLEANUP_DAYS: int = int(os.getenv("TASK_CLEANUP_DAYS", 7))
    LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", 30))
    
    # Redis 設定 (如果使用 Celery)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # 監控設定
    METRICS_ENABLED: bool = os.getenv("METRICS_ENABLED", "False").lower() == "true"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# 創建設定實例
settings = Settings()

# 常用的使用者代理字串列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# 延遲設定對應表
DELAY_SETTINGS = {
    "fast": {"min": 1, "max": 3},
    "normal": {"min": 3, "max": 5},
    "safe": {"min": 5, "max": 10},
    "ultra-safe": {"min": 10, "max": 20}
}
