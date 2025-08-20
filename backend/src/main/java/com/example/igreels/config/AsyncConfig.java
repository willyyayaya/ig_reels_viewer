package com.example.igreels.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

/**
 * 異步處理配置類別
 * 
 * 配置線程池用於背景執行觀看任務，避免阻塞主線程
 */
@Configuration
@EnableAsync
public class AsyncConfig {
    
    /**
     * 配置任務執行器
     * 
     * 限制同時執行的瀏覽器實例數量，避免系統資源過度消耗
     */
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        
        // 核心線程數：同時執行的瀏覽器實例數量
        executor.setCorePoolSize(2);
        
        // 最大線程數：系統忙碌時的最大瀏覽器實例
        executor.setMaxPoolSize(4);
        
        // 隊列容量：等待執行的任務數量
        executor.setQueueCapacity(20);
        
        // 線程名稱前綴
        executor.setThreadNamePrefix("IG-Viewer-");
        
        // 關閉時等待任務完成
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(60);
        
        executor.initialize();
        return executor;
    }
}
