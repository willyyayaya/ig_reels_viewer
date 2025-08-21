"""
系統狀態 API 路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
import psutil
import os
from datetime import datetime

from app.database.connection import get_db
from app.api.schemas import SystemStatusResponse
from app.services.task_service import TaskService

router = APIRouter()

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

@router.get("/system/status", response_model=SystemStatusResponse)
async def get_system_status(
    task_service: TaskService = Depends(get_task_service)
):
    """
    獲取系統狀態資訊
    """
    try:
        # 獲取任務統計
        task_stats = task_service.get_task_statistics()
        
        # 獲取系統資源使用情況
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 獲取進程資訊
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        status_data = {
            "system_info": {
                "timestamp": datetime.now().isoformat(),
                "uptime": datetime.now().timestamp() - process.create_time(),
                "pid": os.getpid()
            },
            "resources": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                },
                "process_memory": {
                    "rss": process_memory.rss,
                    "vms": process_memory.vms
                }
            },
            "tasks": task_stats,
            "health": {
                "status": "healthy" if cpu_percent < 80 and memory.percent < 80 else "warning",
                "database": "connected",
                "api": "running"
            }
        }
        
        return SystemStatusResponse(
            data=status_data,
            message="系統狀態獲取成功"
        )
        
    except Exception as e:
        logger.error(f"❌ 獲取系統狀態失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取系統狀態失敗: {str(e)}"
        )

@router.get("/system/logs")
async def get_system_logs(
    level: str = "INFO",
    limit: int = 100,
    task_service: TaskService = Depends(get_task_service)
):
    """
    獲取系統日誌
    """
    try:
        logs = task_service.get_system_logs(level=level, limit=limit)
        
        return {
            "success": True,
            "data": [log.to_dict() for log in logs],
            "total": len(logs),
            "message": "成功獲取系統日誌"
        }
        
    except Exception as e:
        logger.error(f"❌ 獲取系統日誌失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取系統日誌失敗: {str(e)}"
        )

@router.post("/system/cleanup")
async def cleanup_old_data(
    days: int = 7,
    task_service: TaskService = Depends(get_task_service)
):
    """
    清理舊資料
    """
    try:
        # 清理舊任務
        deleted_tasks = task_service.cleanup_old_tasks(days)
        
        # 清理舊日誌
        deleted_logs = task_service.cleanup_old_logs(days * 2)  # 日誌保留更久
        
        return {
            "success": True,
            "data": {
                "deleted_tasks": deleted_tasks,
                "deleted_logs": deleted_logs
            },
            "message": f"成功清理 {days} 天前的資料"
        }
        
    except Exception as e:
        logger.error(f"❌ 清理資料失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"清理資料失敗: {str(e)}"
        )

@router.get("/system/metrics")
async def get_metrics():
    """
    獲取系統指標（用於監控）
    """
    try:
        # 這裡可以整合 Prometheus 或其他監控工具
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "api_version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "features": {
                "task_management": True,
                "real_time_monitoring": True,
                "automation": True,
                "safety_measures": True
            }
        }
        
        return {
            "success": True,
            "data": metrics,
            "message": "成功獲取系統指標"
        }
        
    except Exception as e:
        logger.error(f"❌ 獲取系統指標失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取系統指標失敗: {str(e)}"
        )
