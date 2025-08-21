"""
API 資料模型 (Pydantic Schemas)
"""

from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, validator
import re

class TaskCreate(BaseModel):
    """建立任務的請求模型"""
    url: str = Field(..., description="Instagram Reels 網址")
    target_views: int = Field(..., ge=1, le=100, description="目標觀看次數")
    delay_type: str = Field(default="normal", description="延遲類型")
    simulate_actions: List[str] = Field(default=[], description="模擬操作列表")
    
    @validator('url')
    def validate_instagram_url(cls, v):
        """驗證 Instagram Reels 網址"""
        pattern = r'^https?://(www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?(\?.*)?$'
        if not re.match(pattern, v):
            raise ValueError('請輸入有效的 Instagram Reels 網址')
        return v
    
    @validator('delay_type')
    def validate_delay_type(cls, v):
        """驗證延遲類型"""
        allowed_types = ['fast', 'normal', 'safe', 'ultra-safe']
        if v not in allowed_types:
            raise ValueError(f'延遲類型必須是: {", ".join(allowed_types)}')
        return v
    
    @validator('simulate_actions')
    def validate_simulate_actions(cls, v):
        """驗證模擬操作"""
        allowed_actions = ['scroll', 'pause', 'volume', 'like', 'comment']
        for action in v:
            if action not in allowed_actions:
                raise ValueError(f'不支援的操作: {action}. 允許的操作: {", ".join(allowed_actions)}')
        return v

class TaskResponse(BaseModel):
    """任務回應模型"""
    id: int
    url: str
    target_views: int
    completed_views: int
    status: str
    delay_type: str
    simulate_actions: List[str]
    error_message: Optional[str] = None
    logs: List[dict] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """任務列表回應模型"""
    success: bool = True
    data: List[TaskResponse]
    total: int
    message: str = "獲取任務列表成功"

class TaskCreateResponse(BaseModel):
    """建立任務回應模型"""
    success: bool = True
    data: TaskResponse
    message: str = "任務建立成功"

class TaskActionResponse(BaseModel):
    """任務操作回應模型"""
    success: bool = True
    message: str
    data: Optional[dict] = None

class SystemStatusResponse(BaseModel):
    """系統狀態回應模型"""
    success: bool = True
    data: dict
    message: str = "獲取系統狀態成功"

class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    success: bool = False
    message: str
    detail: Optional[str] = None
    code: Optional[str] = None

# WebSocket 訊息模型
class WebSocketMessage(BaseModel):
    """WebSocket 訊息模型"""
    type: str  # task_update, system_status, error
    data: dict
    timestamp: datetime = Field(default_factory=datetime.now)

class TaskUpdate(BaseModel):
    """任務更新訊息"""
    task_id: int
    status: str
    completed_views: int
    progress: float
    message: Optional[str] = None

# 驗證函式
def validate_instagram_reel_url(url: str) -> bool:
    """驗證 Instagram Reels 網址格式"""
    pattern = r'^https?://(www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?(\?.*)?$'
    return bool(re.match(pattern, url))

def sanitize_url(url: str) -> str:
    """清理和標準化網址"""
    # 移除查詢參數
    if '?' in url:
        url = url.split('?')[0]
    
    # 確保以 / 結尾
    if not url.endswith('/'):
        url += '/'
    
    # 確保使用 https
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    
    return url
