package com.example.igreels.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

import java.time.LocalDateTime;

/**
 * 觀看任務實體類別
 * 
 * 用於記錄每個Instagram Reels觀看任務的詳細資訊
 */
@Entity
@Table(name = "view_tasks")
public class ViewTask {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Reels URL不能為空")
    @Pattern(regexp = "^https://www\\.instagram\\.com/(reel|p)/.*", 
             message = "必須是有效的Instagram Reels URL")
    @Column(name = "reels_url", nullable = false, length = 500)
    private String reelsUrl;
    
    @Min(value = 1, message = "觀看次數必須大於0")
    @Column(name = "view_count", nullable = false)
    private Integer viewCount;
    
    @Column(name = "completed_count", nullable = false)
    private Integer completedCount = 0;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private TaskStatus status = TaskStatus.PENDING;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "started_at")
    private LocalDateTime startedAt;
    
    @Column(name = "completed_at")
    private LocalDateTime completedAt;
    
    @Column(name = "error_message", length = 1000)
    private String errorMessage;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
    
    // Constructors
    public ViewTask() {}
    
    public ViewTask(String reelsUrl, Integer viewCount) {
        this.reelsUrl = reelsUrl;
        this.viewCount = viewCount;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getReelsUrl() {
        return reelsUrl;
    }
    
    public void setReelsUrl(String reelsUrl) {
        this.reelsUrl = reelsUrl;
    }
    
    public Integer getViewCount() {
        return viewCount;
    }
    
    public void setViewCount(Integer viewCount) {
        this.viewCount = viewCount;
    }
    
    public Integer getCompletedCount() {
        return completedCount;
    }
    
    public void setCompletedCount(Integer completedCount) {
        this.completedCount = completedCount;
    }
    
    public TaskStatus getStatus() {
        return status;
    }
    
    public void setStatus(TaskStatus status) {
        this.status = status;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getStartedAt() {
        return startedAt;
    }
    
    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }
    
    public LocalDateTime getCompletedAt() {
        return completedAt;
    }
    
    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
    
    /**
     * 計算進度百分比
     */
    public double getProgress() {
        if (viewCount == 0) return 0.0;
        return (double) completedCount / viewCount * 100.0;
    }
    
    /**
     * 是否已完成
     */
    public boolean isCompleted() {
        return status == TaskStatus.COMPLETED;
    }
    
    /**
     * 是否執行中
     */
    public boolean isRunning() {
        return status == TaskStatus.RUNNING;
    }
}


