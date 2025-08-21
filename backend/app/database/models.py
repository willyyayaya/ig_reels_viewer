"""
資料庫模型定義
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.database.connection import Base

class Task(Base):
    """任務模型"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False, index=True)
    target_views = Column(Integer, nullable=False)
    completed_views = Column(Integer, default=0)
    status = Column(String(20), default="pending", index=True)  # pending, running, completed, failed, stopped
    delay_type = Column(String(20), default="normal")
    simulate_actions = Column(JSON, default=list)
    error_message = Column(Text, nullable=True)
    logs = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "url": self.url,
            "target_views": self.target_views,
            "completed_views": self.completed_views,
            "status": self.status,
            "delay_type": self.delay_type,
            "simulate_actions": self.simulate_actions or [],
            "error_message": self.error_message,
            "logs": self.logs or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class SystemLog(Base):
    """系統日誌模型"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, DEBUG
    message = Column(Text, nullable=False)
    task_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "task_id": self.task_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class SystemStatus(Base):
    """系統狀態模型"""
    __tablename__ = "system_status"
    
    id = Column(Integer, primary_key=True, index=True)
    active_tasks = Column(Integer, default=0)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    system_load = Column(String(50), nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            "id": self.id,
            "active_tasks": self.active_tasks,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "system_load": self.system_load,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
