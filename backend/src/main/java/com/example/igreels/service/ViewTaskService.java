package com.example.igreels.service;

import com.example.igreels.model.TaskStatus;
import com.example.igreels.model.ViewTask;
import com.example.igreels.repository.ViewTaskRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

/**
 * 觀看任務服務類別
 * 
 * 負責管理Instagram Reels觀看任務的建立、執行和狀態管理
 */
@Service
@Transactional
public class ViewTaskService {
    
    private static final Logger logger = LoggerFactory.getLogger(ViewTaskService.class);
    
    @Autowired
    private ViewTaskRepository viewTaskRepository;
    
    @Autowired
    private InstagramViewerService instagramViewerService;
    
    /**
     * 建立新的觀看任務
     */
    public ViewTask createTask(String reelsUrl, Integer viewCount) {
        // 驗證輸入
        if (reelsUrl == null || reelsUrl.trim().isEmpty()) {
            throw new IllegalArgumentException("Reels URL不能為空");
        }
        
        if (viewCount == null || viewCount <= 0) {
            throw new IllegalArgumentException("觀看次數必須大於0");
        }
        
        // 建立任務
        ViewTask task = new ViewTask(reelsUrl.trim(), viewCount);
        ViewTask savedTask = viewTaskRepository.save(task);
        
        logger.info("建立新任務: ID={}, URL={}, 觀看次數={}", 
                   savedTask.getId(), savedTask.getReelsUrl(), savedTask.getViewCount());
        
        return savedTask;
    }
    
    /**
     * 執行觀看任務（異步）
     */
    @Async
    public CompletableFuture<Void> executeTask(Long taskId) {
        Optional<ViewTask> taskOpt = viewTaskRepository.findById(taskId);
        if (taskOpt.isEmpty()) {
            logger.error("找不到任務: ID={}", taskId);
            return CompletableFuture.completedFuture(null);
        }
        
        ViewTask task = taskOpt.get();
        
        try {
            // 更新狀態為執行中
            task.setStatus(TaskStatus.RUNNING);
            task.setStartedAt(LocalDateTime.now());
            viewTaskRepository.save(task);
            
            logger.info("開始執行任務: ID={}, URL={}", task.getId(), task.getReelsUrl());
            
            // 執行觀看
            instagramViewerService.viewReels(task.getReelsUrl(), task.getViewCount());
            
            // 更新狀態為完成
            task.setStatus(TaskStatus.COMPLETED);
            task.setCompletedCount(task.getViewCount());
            task.setCompletedAt(LocalDateTime.now());
            task.setErrorMessage(null);
            
            logger.info("任務執行完成: ID={}", task.getId());
            
        } catch (Exception e) {
            // 更新狀態為失敗
            task.setStatus(TaskStatus.FAILED);
            task.setErrorMessage(e.getMessage());
            task.setCompletedAt(LocalDateTime.now());
            
            logger.error("任務執行失敗: ID={}, 錯誤: {}", task.getId(), e.getMessage(), e);
        } finally {
            viewTaskRepository.save(task);
        }
        
        return CompletableFuture.completedFuture(null);
    }
    
    /**
     * 建立並立即執行任務
     */
    public ViewTask createAndExecuteTask(String reelsUrl, Integer viewCount) {
        ViewTask task = createTask(reelsUrl, viewCount);
        executeTask(task.getId());
        return task;
    }
    
    /**
     * 取得任務詳情
     */
    public Optional<ViewTask> getTask(Long taskId) {
        return viewTaskRepository.findById(taskId);
    }
    
    /**
     * 取得所有任務列表
     */
    public List<ViewTask> getAllTasks() {
        return viewTaskRepository.findAll();
    }
    
    /**
     * 取得最近的任務列表
     */
    public List<ViewTask> getRecentTasks(int limit) {
        return viewTaskRepository.findRecentTasks(PageRequest.of(0, limit));
    }
    
    /**
     * 根據狀態取得任務列表
     */
    public List<ViewTask> getTasksByStatus(TaskStatus status) {
        return viewTaskRepository.findByStatus(status);
    }
    
    /**
     * 取得執行中的任務數量
     */
    public long getRunningTaskCount() {
        return viewTaskRepository.countByStatus(TaskStatus.RUNNING);
    }
    
    /**
     * 取消任務
     */
    public boolean cancelTask(Long taskId) {
        Optional<ViewTask> taskOpt = viewTaskRepository.findById(taskId);
        if (taskOpt.isEmpty()) {
            return false;
        }
        
        ViewTask task = taskOpt.get();
        if (task.getStatus() == TaskStatus.PENDING) {
            task.setStatus(TaskStatus.CANCELLED);
            task.setCompletedAt(LocalDateTime.now());
            viewTaskRepository.save(task);
            
            logger.info("任務已取消: ID={}", taskId);
            return true;
        }
        
        return false;
    }
    
    /**
     * 刪除任務
     */
    public boolean deleteTask(Long taskId) {
        try {
            viewTaskRepository.deleteById(taskId);
            logger.info("任務已刪除: ID={}", taskId);
            return true;
        } catch (Exception e) {
            logger.error("刪除任務失敗: ID={}, 錯誤: {}", taskId, e.getMessage());
            return false;
        }
    }
    
    /**
     * 取得任務統計資訊
     */
    public TaskStatistics getTaskStatistics() {
        List<Object[]> stats = viewTaskRepository.getTaskStatistics();
        
        TaskStatistics statistics = new TaskStatistics();
        for (Object[] stat : stats) {
            TaskStatus status = (TaskStatus) stat[0];
            Long count = (Long) stat[1];
            
            switch (status) {
                case PENDING -> statistics.setPendingCount(count.intValue());
                case RUNNING -> statistics.setRunningCount(count.intValue());
                case COMPLETED -> statistics.setCompletedCount(count.intValue());
                case FAILED -> statistics.setFailedCount(count.intValue());
                case CANCELLED -> statistics.setCancelledCount(count.intValue());
            }
        }
        
        return statistics;
    }
    
    /**
     * 任務統計資料類別
     */
    public static class TaskStatistics {
        private int pendingCount = 0;
        private int runningCount = 0;
        private int completedCount = 0;
        private int failedCount = 0;
        private int cancelledCount = 0;
        
        // Getters and Setters
        public int getPendingCount() { return pendingCount; }
        public void setPendingCount(int pendingCount) { this.pendingCount = pendingCount; }
        
        public int getRunningCount() { return runningCount; }
        public void setRunningCount(int runningCount) { this.runningCount = runningCount; }
        
        public int getCompletedCount() { return completedCount; }
        public void setCompletedCount(int completedCount) { this.completedCount = completedCount; }
        
        public int getFailedCount() { return failedCount; }
        public void setFailedCount(int failedCount) { this.failedCount = failedCount; }
        
        public int getCancelledCount() { return cancelledCount; }
        public void setCancelledCount(int cancelledCount) { this.cancelledCount = cancelledCount; }
        
        public int getTotalCount() {
            return pendingCount + runningCount + completedCount + failedCount + cancelledCount;
        }
    }
}
