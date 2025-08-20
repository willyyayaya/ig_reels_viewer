package com.example.igreels.service;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.Random;

/**
 * Instagram 觀看服務
 * 
 * 使用Selenium WebDriver自動化瀏覽Instagram Reels
 * 
 * ⚠️ 注意：此服務可能違反Instagram使用條款，請謹慎使用
 */
@Service
public class InstagramViewerService {
    
    private static final Logger logger = LoggerFactory.getLogger(InstagramViewerService.class);
    
    private static final int MIN_VIEW_DURATION = 3000; // 最小觀看時間 3秒
    private static final int MAX_VIEW_DURATION = 8000; // 最大觀看時間 8秒
    private static final int MIN_INTERVAL = 2000;      // 最小間隔時間 2秒
    private static final int MAX_INTERVAL = 5000;      // 最大間隔時間 5秒
    
    private final Random random = new Random();
    
    /**
     * 觀看指定的Instagram Reels
     * 
     * @param reelsUrl Instagram Reels URL
     * @param viewCount 觀看次數
     * @throws Exception 觀看過程中發生的異常
     */
    public void viewReels(String reelsUrl, int viewCount) throws Exception {
        if (!isValidInstagramUrl(reelsUrl)) {
            throw new IllegalArgumentException("無效的Instagram URL: " + reelsUrl);
        }
        
        WebDriver driver = null;
        try {
            driver = createWebDriver();
            logger.info("開始觀看 Reels: {} (目標次數: {})", reelsUrl, viewCount);
            
            for (int i = 1; i <= viewCount; i++) {
                logger.info("第 {}/{} 次觀看", i, viewCount);
                
                // 導航到Reels頁面
                driver.get(reelsUrl);
                
                // 等待頁面載入
                waitForPageLoad(driver);
                
                // 模擬真實使用者行為
                simulateUserBehavior(driver);
                
                // 隨機間隔時間
                if (i < viewCount) {
                    Thread.sleep(getRandomInterval());
                }
            }
            
            logger.info("成功完成觀看任務: {}", reelsUrl);
            
        } catch (Exception e) {
            logger.error("觀看Reels時發生錯誤: {}", e.getMessage(), e);
            throw e;
        } finally {
            if (driver != null) {
                try {
                    driver.quit();
                } catch (Exception e) {
                    logger.warn("關閉WebDriver時發生錯誤: {}", e.getMessage());
                }
            }
        }
    }
    
    /**
     * 建立WebDriver實例
     */
    private WebDriver createWebDriver() {
        // 自動管理ChromeDriver
        WebDriverManager.chromedriver().setup();
        
        ChromeOptions options = new ChromeOptions();
        
        // 無頭模式（背景執行）
        options.addArguments("--headless");
        
        // 防止被偵測為自動化程式
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.addArguments("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
        
        // 性能優化
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-gpu");
        options.addArguments("--disable-images");
        options.addArguments("--disable-javascript");
        
        // 視窗大小
        options.addArguments("--window-size=1920,1080");
        
        return new ChromeDriver(options);
    }
    
    /**
     * 等待頁面載入完成
     */
    private void waitForPageLoad(WebDriver driver) throws Exception {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        
        try {
            // 等待Instagram內容載入
            wait.until(ExpectedConditions.or(
                ExpectedConditions.presenceOfElementLocated(By.cssSelector("article")),
                ExpectedConditions.presenceOfElementLocated(By.cssSelector("video")),
                ExpectedConditions.presenceOfElementLocated(By.cssSelector("[role='main']"))
            ));
            
            // 額外等待確保內容完全載入
            Thread.sleep(2000);
            
        } catch (Exception e) {
            logger.warn("等待頁面載入時發生問題，可能是網路問題或頁面結構改變");
            // 即使等待失敗也繼續執行，避免因小問題中斷整個流程
        }
    }
    
    /**
     * 模擬真實使用者行為
     */
    private void simulateUserBehavior(WebDriver driver) throws InterruptedException {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        
        // 隨機滾動
        js.executeScript("window.scrollBy(0, " + random.nextInt(200) + ");");
        
        // 隨機等待時間，模擬觀看
        int viewDuration = MIN_VIEW_DURATION + random.nextInt(MAX_VIEW_DURATION - MIN_VIEW_DURATION);
        Thread.sleep(viewDuration);
        
        // 隨機滾動回原位
        js.executeScript("window.scrollBy(0, -" + random.nextInt(100) + ");");
    }
    
    /**
     * 獲取隨機間隔時間
     */
    private int getRandomInterval() {
        return MIN_INTERVAL + random.nextInt(MAX_INTERVAL - MIN_INTERVAL);
    }
    
    /**
     * 驗證Instagram URL格式
     */
    private boolean isValidInstagramUrl(String url) {
        if (url == null || url.trim().isEmpty()) {
            return false;
        }
        
        return url.matches("^https://www\\.instagram\\.com/(reel|p)/[a-zA-Z0-9_-]+/?.*$");
    }
    
    /**
     * 檢查網站是否可訪問
     */
    public boolean isInstagramAccessible() {
        WebDriver driver = null;
        try {
            driver = createWebDriver();
            driver.get("https://www.instagram.com");
            
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            wait.until(ExpectedConditions.titleContains("Instagram"));
            
            return true;
        } catch (Exception e) {
            logger.error("Instagram無法訪問: {}", e.getMessage());
            return false;
        } finally {
            if (driver != null) {
                try {
                    driver.quit();
                } catch (Exception e) {
                    logger.warn("關閉測試WebDriver時發生錯誤");
                }
            }
        }
    }
}
