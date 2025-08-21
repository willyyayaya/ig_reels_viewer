"""
任務管理器 - 負責協調和執行自動化任務
"""

import asyncio
from typing import Dict, Optional
from datetime import datetime
from loguru import logger

from app.database.connection import get_db
from app.services.task_service import TaskService
from app.services.instagram_automation import InstagramAutomation

class TaskManager:
    """
    任務管理器
    
    負責：
    - 管理並發任務執行
    - 監控任務狀態
    - 處理任務停止和清理
    """
    
    def __init__(self):
        self.active_tasks: Dict[int, InstagramAutomation] = {}
        self.task_futures: Dict[int, asyncio.Task] = {}
        self.is_running = False
        self.max_concurrent_tasks = 3
    
    async def start(self):
        """啟動任務管理器"""
        logger.info("🚀 任務管理器啟動")
        self.is_running = True
    
    async def stop(self):
        """停止任務管理器"""
        logger.info("🛑 正在停止任務管理器...")
        self.is_running = False
        
        # 停止所有活動任務
        tasks_to_stop = list(self.active_tasks.keys())
        for task_id in tasks_to_stop:
            await self.stop_task(task_id)
        
        logger.info("✅ 任務管理器已停止")
    
    async def execute_task(self, task_id: int):
        """執行任務"""
        if not self.is_running:
            logger.warning(f"⚠️ 任務管理器未運行，忽略任務 {task_id}")
            return
        
        if len(self.active_tasks) >= self.max_concurrent_tasks:
            logger.warning(f"⚠️ 達到最大並發任務數，任務 {task_id} 將等待")
            # 在實際應用中，這裡可以實現任務隊列
            return
        
        if task_id in self.active_tasks:
            logger.warning(f"⚠️ 任務 {task_id} 已在執行中")
            return
        
        # 創建自動化實例
        automation = InstagramAutomation(task_id)
        self.active_tasks[task_id] = automation
        
        # 創建並啟動任務
        task_future = asyncio.create_task(self._run_task(task_id, automation))
        self.task_futures[task_id] = task_future
        
        logger.info(f"🎬 任務 {task_id} 已加入執行隊列 (活動任務: {len(self.active_tasks)})")
    
    async def stop_task(self, task_id: int) -> bool:
        """停止指定任務"""
        try:
            if task_id in self.active_tasks:
                logger.info(f"🛑 正在停止任務 {task_id}")
                
                # 發送停止信號
                automation = self.active_tasks[task_id]
                automation.stop()
                
                # 取消任務 Future
                if task_id in self.task_futures:
                    task_future = self.task_futures[task_id]
                    if not task_future.done():
                        task_future.cancel()
                
                # 等待任務清理完成
                await asyncio.sleep(2)
                
                # 強制清理
                await self._cleanup_task(task_id)
                
                return True
            else:
                logger.warning(f"⚠️ 任務 {task_id} 不在活動列表中")
                return False
                
        except Exception as e:
            logger.error(f"❌ 停止任務 {task_id} 失敗: {str(e)}")
            return False
    
    async def _run_task(self, task_id: int, automation: InstagramAutomation):
        """執行單個任務的完整流程"""
        db = next(get_db())
        task_service = TaskService(db)
        
        try:
            # 更新任務狀態為執行中
            task_service.update_task_status(task_id, "running")
            
            # 獲取任務詳情
            task = task_service.get_task_by_id(task_id)
            if not task:
                raise Exception(f"找不到任務 {task_id}")
            
            logger.info(f"🎯 開始執行任務 {task_id}: {task.url}")
            
            # 設置 WebDriver
            if not await automation.setup_driver():
                raise Exception("WebDriver 設置失敗")
            
            # 導航到目標頁面
            if not await automation.navigate_to_reel(task.url):
                raise Exception("無法導航到目標 Reel")
            
            # 執行觀看循環
            for view_count in range(1, task.target_views + 1):
                if automation.should_stop:
                    logger.info(f"🛑 任務 {task_id} 收到停止信號，中止執行")
                    break
                
                # 執行觀看
                success = await automation.perform_view(
                    view_count,
                    task.delay_type,
                    task.simulate_actions or []
                )
                
                if success:
                    # 更新進度
                    task_service.update_task_progress(
                        task_id,
                        view_count,
                        f"完成第 {view_count} 次觀看"
                    )
                    
                    logger.info(f"✅ 任務 {task_id}: 進度 {view_count}/{task.target_views}")
                else:
                    logger.warning(f"⚠️ 任務 {task_id}: 第 {view_count} 次觀看失敗")
                    # 可以選擇繼續或停止
                    
                # 檢查是否應該停止
                if automation.should_stop:
                    break
                
                # 觀看間隔延遲
                if view_count < task.target_views:
                    delay = self._get_between_views_delay(task.delay_type)
                    logger.debug(f"⏱️ 任務 {task_id}: 觀看間隔延遲 {delay:.1f} 秒")
                    await asyncio.sleep(delay)
            
            # 檢查任務是否完成
            if not automation.should_stop and task_service.get_task_by_id(task_id).completed_views == task.target_views:
                task_service.update_task_status(task_id, "completed")
                logger.info(f"🎉 任務 {task_id} 已完成！")
            else:
                task_service.update_task_status(task_id, "stopped", "任務被手動停止")
                logger.info(f"🛑 任務 {task_id} 已停止")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 任務 {task_id} 執行失敗: {error_msg}")
            task_service.update_task_status(task_id, "failed", error_msg)
            
        finally:
            # 清理資源
            await self._cleanup_task(task_id)
            db.close()
    
    async def _cleanup_task(self, task_id: int):
        """清理任務資源"""
        try:
            # 清理自動化實例
            if task_id in self.active_tasks:
                automation = self.active_tasks[task_id]
                await automation.cleanup()
                del self.active_tasks[task_id]
            
            # 清理 Future
            if task_id in self.task_futures:
                del self.task_futures[task_id]
            
            logger.info(f"🧹 任務 {task_id} 資源已清理")
            
        except Exception as e:
            logger.error(f"❌ 清理任務 {task_id} 失敗: {str(e)}")
    
    def _get_between_views_delay(self, delay_type: str) -> float:
        """獲取觀看之間的延遲時間"""
        import random
        from app.core.config import DELAY_SETTINGS
        
        delay_config = DELAY_SETTINGS.get(delay_type, DELAY_SETTINGS["normal"])
        
        # 觀看間隔比單次觀看時間稍長
        min_delay = delay_config["max"]
        max_delay = delay_config["max"] * 2
        
        return random.uniform(min_delay, max_delay)
    
    def get_active_task_count(self) -> int:
        """獲取活動任務數量"""
        return len(self.active_tasks)
    
    def get_task_status(self, task_id: int) -> Optional[str]:
        """獲取任務狀態"""
        if task_id in self.active_tasks:
            return "running"
        return None
    
    def get_current_time(self) -> str:
        """獲取當前時間"""
        return datetime.now().isoformat()
