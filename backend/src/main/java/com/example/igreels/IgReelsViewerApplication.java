package com.example.igreels;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Instagram Reels Viewer 應用程式主類別
 * 
 * 功能：
 * 1. 啟動Spring Boot應用程式
 * 2. 啟用異步處理支援（用於背景執行觀看任務）
 */
@SpringBootApplication
@EnableAsync
public class IgReelsViewerApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(IgReelsViewerApplication.class, args);
    }
}
