"""
任務管理 API 路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from sqlalchemy.orm import Session
from loguru import logger

from app.database.connection import get_db
from app.database.models import Task
from app.api.schemas import (
    TaskCreate, TaskResponse, TaskListResponse, 
    TaskCreateResponse, TaskActionResponse, sanitize_url
)
from app.services.task_service import TaskService
from app.services.task_manager import TaskManager

router = APIRouter()

# 依賴注入
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

def get_task_manager() -> TaskManager:
    # 這裡需要從主應用程式獲取單例實例
    from main import task_manager
    return task_manager

@router.post("/tasks", response_model=TaskCreateResponse)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    task_service: TaskService = Depends(get_task_service),
    task_manager: TaskManager = Depends(get_task_manager)
):
    """
    建立新的觀看任務
    
    ⚠️ **警告**: 此功能可能違反 Instagram 使用條款，請謹慎使用！
    """
    try:
        logger.info(f"📝 建立新任務: {task_data.url}")
        
        # 清理和驗證網址
        cleaned_url = sanitize_url(task_data.url)
        
        # 檢查是否已存在相同的進行中任務
        existing_task = task_service.get_active_task_by_url(cleaned_url)
        if existing_task:
            raise HTTPException(
                status_code=400,
                detail=f"該網址已有進行中的任務 (ID: {existing_task.id})"
            )
        
        # 檢查並發任務數量限制
        active_count = task_service.get_active_tasks_count()
        if active_count >= 3:  # 最大並發數
            raise HTTPException(
                status_code=429,
                detail="同時進行的任務數量已達上限，請等待其他任務完成"
            )
        
        # 建立任務
        new_task = task_service.create_task(
            url=cleaned_url,
            target_views=task_data.target_views,
            delay_type=task_data.delay_type,
            simulate_actions=task_data.simulate_actions
        )
        
        # 將任務加入執行隊列
        background_tasks.add_task(
            task_manager.execute_task,
            new_task.id
        )
        
        logger.info(f"✅ 任務 {new_task.id} 已建立並加入執行隊列")
        
        return TaskCreateResponse(
            data=TaskResponse.from_orm(new_task),
            message="任務已成功建立並開始執行"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 建立任務失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"建立任務失敗: {str(e)}"
        )

@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    status: Optional[str] = Query(None, description="篩選狀態"),
    limit: int = Query(50, ge=1, le=100, description="每頁數量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    task_service: TaskService = Depends(get_task_service)
):
    """
    獲取任務列表
    """
    try:
        tasks, total = task_service.get_tasks(
            status=status,
            limit=limit,
            offset=offset
        )
        
        return TaskListResponse(
            data=[TaskResponse.from_orm(task) for task in tasks],
            total=total,
            message=f"成功獲取 {len(tasks)} 個任務"
        )
        
    except Exception as e:
        logger.error(f"❌ 獲取任務列表失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取任務列表失敗: {str(e)}"
        )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int = Path(..., description="任務ID"),
    task_service: TaskService = Depends(get_task_service)
):
    """
    獲取單個任務詳情
    """
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"找不到 ID 為 {task_id} 的任務"
            )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 獲取任務失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取任務失敗: {str(e)}"
        )

@router.post("/tasks/{task_id}/stop", response_model=TaskActionResponse)
async def stop_task(
    task_id: int = Path(..., description="任務ID"),
    task_service: TaskService = Depends(get_task_service),
    task_manager: TaskManager = Depends(get_task_manager)
):
    """
    停止指定任務
    """
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"找不到 ID 為 {task_id} 的任務"
            )
        
        if task.status not in ['pending', 'running']:
            raise HTTPException(
                status_code=400,
                detail=f"任務狀態為 {task.status}，無法停止"
            )
        
        # 停止任務執行
        success = await task_manager.stop_task(task_id)
        
        if success:
            # 更新任務狀態
            task_service.update_task_status(task_id, "stopped")
            logger.info(f"🛑 任務 {task_id} 已停止")
            
            return TaskActionResponse(
                message=f"任務 {task_id} 已成功停止"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="停止任務失敗"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 停止任務失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"停止任務失敗: {str(e)}"
        )

@router.post("/tasks/{task_id}/retry", response_model=TaskActionResponse)
async def retry_task(
    task_id: int = Path(..., description="任務ID"),
    background_tasks: BackgroundTasks,
    task_service: TaskService = Depends(get_task_service),
    task_manager: TaskManager = Depends(get_task_manager)
):
    """
    重試失敗的任務
    """
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"找不到 ID 為 {task_id} 的任務"
            )
        
        if task.status not in ['failed', 'stopped']:
            raise HTTPException(
                status_code=400,
                detail=f"任務狀態為 {task.status}，無法重試"
            )
        
        # 重置任務狀態
        task_service.reset_task_for_retry(task_id)
        
        # 重新加入執行隊列
        background_tasks.add_task(
            task_manager.execute_task,
            task_id
        )
        
        logger.info(f"🔄 任務 {task_id} 已重新開始")
        
        return TaskActionResponse(
            message=f"任務 {task_id} 已重新開始執行"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 重試任務失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"重試任務失敗: {str(e)}"
        )

@router.delete("/tasks/{task_id}", response_model=TaskActionResponse)
async def delete_task(
    task_id: int = Path(..., description="任務ID"),
    task_service: TaskService = Depends(get_task_service),
    task_manager: TaskManager = Depends(get_task_manager)
):
    """
    刪除任務（僅限已完成或失敗的任務）
    """
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"找不到 ID 為 {task_id} 的任務"
            )
        
        if task.status in ['running', 'pending']:
            raise HTTPException(
                status_code=400,
                detail="無法刪除進行中的任務，請先停止任務"
            )
        
        # 確保任務不在執行隊列中
        await task_manager.stop_task(task_id)
        
        # 刪除任務
        task_service.delete_task(task_id)
        
        logger.info(f"🗑️ 任務 {task_id} 已刪除")
        
        return TaskActionResponse(
            message=f"任務 {task_id} 已成功刪除"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 刪除任務失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"刪除任務失敗: {str(e)}"
        )

@router.get("/tasks/stats/summary")
async def get_task_stats(
    task_service: TaskService = Depends(get_task_service)
):
    """
    獲取任務統計資訊
    """
    try:
        stats = task_service.get_task_statistics()
        return {
            "success": True,
            "data": stats,
            "message": "成功獲取任務統計"
        }
        
    except Exception as e:
        logger.error(f"❌ 獲取任務統計失敗: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"獲取任務統計失敗: {str(e)}"
        )
