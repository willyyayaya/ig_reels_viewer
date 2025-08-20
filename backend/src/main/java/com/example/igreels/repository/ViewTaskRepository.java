package com.example.igreels.repository;

import com.example.igreels.model.TaskStatus;
import com.example.igreels.model.ViewTask;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * ViewTask 資料庫存取介面
 * 
 * 提供觀看任務的CRUD操作和查詢功能
 */
@Repository
public interface ViewTaskRepository extends JpaRepository<ViewTask, Long> {
    
    /**
     * 根據狀態查詢任務
     */
    List<ViewTask> findByStatus(TaskStatus status);
    
    /**
     * 查詢等待中的任務，按建立時間排序
     */
    List<ViewTask> findByStatusOrderByCreatedAtAsc(TaskStatus status);
    
    /**
     * 查詢執行中的任務數量
     */
    long countByStatus(TaskStatus status);
    
    /**
     * 查詢指定URL的任務
     */
    List<ViewTask> findByReelsUrlContaining(String url);
    
    /**
     * 查詢最近的任務（限制筆數）
     */
    @Query("SELECT t FROM ViewTask t ORDER BY t.createdAt DESC")
    List<ViewTask> findRecentTasks(org.springframework.data.domain.Pageable pageable);
    
    /**
     * 查詢任務統計資訊
     */
    @Query("SELECT t.status, COUNT(t) FROM ViewTask t GROUP BY t.status")
    List<Object[]> getTaskStatistics();
}
