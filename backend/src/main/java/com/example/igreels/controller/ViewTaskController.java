package com.example.igreels.controller;

import com.example.igreels.model.TaskStatus;
import com.example.igreels.model.ViewTask;
import com.example.igreels.service.ViewTaskService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

/**
 * 觀看任務控制器
 * 
 * 提供REST API接口供前端呼叫，管理Instagram Reels觀看任務
 */
@RestController
@RequestMapping("/api/tasks")
@CrossOrigin(origins = "http://localhost:5173") // Vue開發伺服器預設端口
public class ViewTaskController {
    
    @Autowired
    private ViewTaskService viewTaskService;
    
    /**
     * 建立新的觀看任務
     */
    @PostMapping
    public ResponseEntity<?> createTask(@Valid @RequestBody CreateTaskRequest request) {
        try {
            ViewTask task = viewTaskService.createAndExecuteTask(
                request.getReelsUrl(), 
                request.getViewCount()
            );
            return ResponseEntity.ok(task);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                .body(new ErrorResponse("輸入錯誤", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new ErrorResponse("伺服器錯誤", "建立任務時發生錯誤"));
        }
    }
    
    /**
     * 取得所有任務列表
     */
    @GetMapping
    public ResponseEntity<List<ViewTask>> getAllTasks() {
        List<ViewTask> tasks = viewTaskService.getAllTasks();
        return ResponseEntity.ok(tasks);
    }
    
    /**
     * 取得最近的任務列表
     */
    @GetMapping("/recent")
    public ResponseEntity<List<ViewTask>> getRecentTasks(
            @RequestParam(defaultValue = "10") int limit) {
        List<ViewTask> tasks = viewTaskService.getRecentTasks(limit);
        return ResponseEntity.ok(tasks);
    }
    
    /**
     * 根據ID取得特定任務
     */
    @GetMapping("/{id}")
    public ResponseEntity<?> getTask(@PathVariable Long id) {
        Optional<ViewTask> task = viewTaskService.getTask(id);
        if (task.isPresent()) {
            return ResponseEntity.ok(task.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 根據狀態取得任務列表
     */
    @GetMapping("/status/{status}")
    public ResponseEntity<List<ViewTask>> getTasksByStatus(@PathVariable TaskStatus status) {
        List<ViewTask> tasks = viewTaskService.getTasksByStatus(status);
        return ResponseEntity.ok(tasks);
    }
    
    /**
     * 取消任務
     */
    @PutMapping("/{id}/cancel")
    public ResponseEntity<?> cancelTask(@PathVariable Long id) {
        boolean success = viewTaskService.cancelTask(id);
        if (success) {
            return ResponseEntity.ok(new SuccessResponse("任務已取消"));
        } else {
            return ResponseEntity.badRequest()
                .body(new ErrorResponse("取消失敗", "無法取消該任務，可能任務不存在或已在執行中"));
        }
    }
    
    /**
     * 刪除任務
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTask(@PathVariable Long id) {
        boolean success = viewTaskService.deleteTask(id);
        if (success) {
            return ResponseEntity.ok(new SuccessResponse("任務已刪除"));
        } else {
            return ResponseEntity.badRequest()
                .body(new ErrorResponse("刪除失敗", "無法刪除該任務"));
        }
    }
    
    /**
     * 取得任務統計資訊
     */
    @GetMapping("/statistics")
    public ResponseEntity<ViewTaskService.TaskStatistics> getTaskStatistics() {
        ViewTaskService.TaskStatistics stats = viewTaskService.getTaskStatistics();
        return ResponseEntity.ok(stats);
    }
    
    /**
     * 取得執行中的任務數量
     */
    @GetMapping("/running/count")
    public ResponseEntity<RunningTaskCountResponse> getRunningTaskCount() {
        long count = viewTaskService.getRunningTaskCount();
        return ResponseEntity.ok(new RunningTaskCountResponse(count));
    }
    
    // DTO Classes
    
    /**
     * 建立任務請求DTO
     */
    public static class CreateTaskRequest {
        private String reelsUrl;
        private Integer viewCount;
        
        // Getters and Setters
        public String getReelsUrl() { return reelsUrl; }
        public void setReelsUrl(String reelsUrl) { this.reelsUrl = reelsUrl; }
        
        public Integer getViewCount() { return viewCount; }
        public void setViewCount(Integer viewCount) { this.viewCount = viewCount; }
    }
    
    /**
     * 錯誤回應DTO
     */
    public static class ErrorResponse {
        private final String error;
        private final String message;
        
        public ErrorResponse(String error, String message) {
            this.error = error;
            this.message = message;
        }
        
        // Getters
        public String getError() { return error; }
        public String getMessage() { return message; }
    }
    
    /**
     * 成功回應DTO
     */
    public static class SuccessResponse {
        private final String message;
        
        public SuccessResponse(String message) {
            this.message = message;
        }
        
        // Getter
        public String getMessage() { return message; }
    }
    
    /**
     * 執行中任務數量回應DTO
     */
    public static class RunningTaskCountResponse {
        private final long count;
        
        public RunningTaskCountResponse(long count) {
            this.count = count;
        }
        
        // Getter
        public long getCount() { return count; }
    }
}
