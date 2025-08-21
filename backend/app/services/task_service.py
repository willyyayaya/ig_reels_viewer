"""
任務服務 - 處理任務的 CRUD 操作
"""

from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database.models import Task, SystemLog
from app.core.config import DELAY_SETTINGS

class TaskService:
    """任務管理服務"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(
        self,
        url: str,
        target_views: int,
        delay_type: str = "normal",
        simulate_actions: List[str] = None
    ) -> Task:
        """建立新任務"""
        if simulate_actions is None:
            simulate_actions = []
            
        new_task = Task(
            url=url,
            target_views=target_views,
            delay_type=delay_type,
            simulate_actions=simulate_actions,
            status="pending"
        )
        
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        
        # 記錄日誌
        self._log_system_event(
            "INFO",
            f"新任務已建立: ID={new_task.id}, URL={url}, 目標觀看={target_views}",
            new_task.id
        )
        
        return new_task
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """根據 ID 獲取任務"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Task], int]:
        """獲取任務列表"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        
        total = query.count()
        tasks = query.order_by(desc(Task.created_at)).offset(offset).limit(limit).all()
        
        return tasks, total
    
    def get_active_task_by_url(self, url: str) -> Optional[Task]:
        """獲取指定網址的進行中任務"""
        return self.db.query(Task).filter(
            Task.url == url,
            Task.status.in_(["pending", "running"])
        ).first()
    
    def get_active_tasks_count(self) -> int:
        """獲取進行中的任務數量"""
        return self.db.query(Task).filter(
            Task.status.in_(["pending", "running"])
        ).count()
    
    def update_task_status(
        self,
        task_id: int,
        status: str,
        error_message: str = None
    ) -> bool:
        """更新任務狀態"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        old_status = task.status
        task.status = status
        task.updated_at = datetime.now()
        
        if error_message:
            task.error_message = error_message
        
        # 設定時間戳
        if status == "running" and not task.started_at:
            task.started_at = datetime.now()
        elif status in ["completed", "failed", "stopped"]:
            task.completed_at = datetime.now()
        
        self.db.commit()
        
        # 記錄狀態變更日誌
        self._log_system_event(
            "INFO",
            f"任務狀態變更: ID={task_id}, {old_status} -> {status}",
            task_id
        )
        
        return True
    
    def update_task_progress(
        self,
        task_id: int,
        completed_views: int,
        log_message: str = None
    ) -> bool:
        """更新任務進度"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        task.completed_views = completed_views
        task.updated_at = datetime.now()
        
        # 添加日誌
        if log_message:
            if not task.logs:
                task.logs = []
            task.logs.append({
                "timestamp": datetime.now().isoformat(),
                "message": log_message,
                "completed_views": completed_views
            })
        
        self.db.commit()
        return True
    
    def reset_task_for_retry(self, task_id: int) -> bool:
        """重置任務以供重試"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        task.status = "pending"
        task.completed_views = 0
        task.error_message = None
        task.started_at = None
        task.completed_at = None
        task.updated_at = datetime.now()
        
        # 清空舊日誌，但保留錯誤記錄
        if task.logs:
            task.logs = [log for log in task.logs if "錯誤" in log.get("message", "")]
        
        self.db.commit()
        
        self._log_system_event(
            "INFO",
            f"任務已重置以供重試: ID={task_id}",
            task_id
        )
        
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """刪除任務"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        # 記錄刪除日誌
        self._log_system_event(
            "INFO",
            f"任務已刪除: ID={task_id}, URL={task.url}",
            task_id
        )
        
        self.db.delete(task)
        self.db.commit()
        
        return True
    
    def get_task_statistics(self) -> dict:
        """獲取任務統計資訊"""
        total = self.db.query(Task).count()
        pending = self.db.query(Task).filter(Task.status == "pending").count()
        running = self.db.query(Task).filter(Task.status == "running").count()
        completed = self.db.query(Task).filter(Task.status == "completed").count()
        failed = self.db.query(Task).filter(Task.status == "failed").count()
        stopped = self.db.query(Task).filter(Task.status == "stopped").count()
        
        # 今日統計
        today = datetime.now().date()
        today_created = self.db.query(Task).filter(
            func.date(Task.created_at) == today
        ).count()
        
        today_completed = self.db.query(Task).filter(
            func.date(Task.completed_at) == today,
            Task.status == "completed"
        ).count()
        
        return {
            "total": total,
            "by_status": {
                "pending": pending,
                "running": running,
                "completed": completed,
                "failed": failed,
                "stopped": stopped
            },
            "today": {
                "created": today_created,
                "completed": today_completed
            },
            "active": running + pending
        }
    
    def cleanup_old_tasks(self, days: int = 7) -> int:
        """清理舊任務"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 只刪除已完成或失敗的舊任務
        deleted_count = self.db.query(Task).filter(
            Task.status.in_(["completed", "failed", "stopped"]),
            Task.created_at < cutoff_date
        ).delete()
        
        self.db.commit()
        
        if deleted_count > 0:
            self._log_system_event(
                "INFO",
                f"清理了 {deleted_count} 個超過 {days} 天的舊任務"
            )
        
        return deleted_count
    
    def get_system_logs(
        self,
        level: str = "INFO",
        limit: int = 100
    ) -> List[SystemLog]:
        """獲取系統日誌"""
        query = self.db.query(SystemLog)
        
        if level != "ALL":
            query = query.filter(SystemLog.level == level)
        
        return query.order_by(desc(SystemLog.created_at)).limit(limit).all()
    
    def cleanup_old_logs(self, days: int = 30) -> int:
        """清理舊日誌"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        deleted_count = self.db.query(SystemLog).filter(
            SystemLog.created_at < cutoff_date
        ).delete()
        
        self.db.commit()
        
        return deleted_count
    
    def _log_system_event(
        self,
        level: str,
        message: str,
        task_id: Optional[int] = None
    ):
        """記錄系統事件"""
        log_entry = SystemLog(
            level=level,
            message=message,
            task_id=task_id
        )
        
        self.db.add(log_entry)
        self.db.commit()
