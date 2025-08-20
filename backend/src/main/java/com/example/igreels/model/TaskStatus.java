package com.example.igreels.model;

/**
 * 任務狀態列舉
 * 
 * 定義Instagram Reels觀看任務的各種狀態
 */
public enum TaskStatus {
    PENDING("等待中"),
    RUNNING("執行中"), 
    COMPLETED("已完成"),
    FAILED("失敗"),
    CANCELLED("已取消");
    
    private final String description;
    
    TaskStatus(String description) {
        this.description = description;
    }
    
    public String getDescription() {
        return description;
    }
}
