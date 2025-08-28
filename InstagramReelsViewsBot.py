# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 01:06:53 2021

@author: VICKY JUNGHARE
"""
#importing required python packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains 
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import json

username= "qqqqqwerty201" #Instagram Username
password= "a130629925" #Instagram Password

def ensure_video_playing():
    """確保視頻開始播放以計算觀看次數"""
    global driver
    try:
        print("▶️ 確保視頻播放中...")
        
        # 等待視頻元素載入
        video_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        # 滾動到視頻中央確保完全可見
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", video_element)
        time.sleep(2)
        
        # 點擊視頻區域確保播放
        actions = ActionChains(driver)
        actions.move_to_element(video_element).click().perform()
        time.sleep(1)
        
        # 檢查視頻是否真的在播放
        is_playing = driver.execute_script("""
            var video = arguments[0];
            return !video.paused && !video.ended && video.readyState > 2;
        """, video_element)
        
        if not is_playing:
            print("🔄 視頻未播放，嘗試手動啟動...")
            # 強制播放視頻
            driver.execute_script("arguments[0].play();", video_element)
            time.sleep(1)
            
            # 檢查是否有播放按鈕需要點擊
            play_selectors = [
                '[aria-label*="播放"]',
                '[aria-label*="Play"]',
                '[aria-label*="play"]',
                'button[aria-label*="播放"]',
                'svg[aria-label*="播放"]',
                '.x1i10hfl[role="button"]'  # Instagram 通用播放按鈕
            ]
            
            for selector in play_selectors:
                try:
                    play_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    if play_btn.is_displayed():
                        play_btn.click()
                        print("✅ 點擊播放按鈕")
                        time.sleep(2)
                        break
                except:
                    continue
        
        # 再次確認播放狀態
        time.sleep(2)
        final_status = driver.execute_script("""
            var video = arguments[0];
            return {
                playing: !video.paused && !video.ended && video.readyState > 2,
                currentTime: video.currentTime,
                duration: video.duration,
                muted: video.muted
            };
        """, video_element)
        
        if final_status['playing']:
            print(f"✅ 視頻正在播放 - 時長: {final_status['duration']:.1f}s, 當前: {final_status['currentTime']:.1f}s")
            
            # 確保音量開啟（某些情況下靜音可能影響計算）
            if final_status['muted']:
                driver.execute_script("arguments[0].muted = false;", video_element)
                print("🔊 取消靜音")
        else:
            print("⚠️ 視頻播放狀態確認失敗")
            
        # 模擬真實觀看行為 - 短暫滾動
        driver.execute_script("window.scrollBy(0, 50);")
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -50);")
        
        print("✅ 視頻播放確認完成")
        
    except Exception as e:
        print(f"⚠️ 視頻播放確認失敗: {e}")

def simulate_human_behavior():
    """模擬人類瀏覽行為"""
    global driver
    actions = ActionChains(driver)
    
    print("🤖 模擬人類行為...")
    
    # 更豐富的行為模式
    behaviors = []
    
    # 滾動行為 (90% 機率)
    if random.random() < 0.9:
        behaviors.append("scroll")
    
    # 滑鼠移動 (70% 機率)
    if random.random() < 0.7:
        behaviors.append("mouse_move")
    
    # 暫停行為 (40% 機率)
    if random.random() < 0.4:
        behaviors.append("pause")
    
    # 視頻互動 (30% 機率)
    if random.random() < 0.3:
        behaviors.append("video_interact")
    
    for behavior in behaviors:
        if behavior == "scroll":
            # 模擬真實滾動模式
            scroll_patterns = [
                lambda: driver.execute_script("window.scrollBy(0, 150);"),  # 向下
                lambda: driver.execute_script("window.scrollBy(0, -100);"), # 向上
                lambda: driver.execute_script("window.scrollBy(0, 300);"),  # 快速向下
            ]
            pattern = random.choice(scroll_patterns)
            pattern()
            time.sleep(random.uniform(0.8, 2.5))
            
        elif behavior == "mouse_move":
            # 隨機滑鼠移動（模擬真實用戶）
            try:
                actions.move_by_offset(
                    random.randint(-200, 200), 
                    random.randint(-150, 150)
                ).perform()
                time.sleep(random.uniform(0.3, 1))
            except:
                pass
            
        elif behavior == "pause":
            # 隨機暫停（模擬用戶思考）
            pause_time = random.uniform(1.5, 5)
            print(f"⏸️ 暫停 {pause_time:.1f} 秒（模擬思考）")
            time.sleep(pause_time)
            
        elif behavior == "video_interact":
            # 與視頻相關的互動
            try:
                video_element = driver.find_element(By.TAG_NAME, "video")
                
                # 隨機選擇互動類型
                interactions = [
                    lambda: actions.move_to_element(video_element).perform(),  # 懸停
                    lambda: actions.double_click(video_element).perform(),     # 雙擊
                    lambda: actions.context_click(video_element).perform(),    # 右鍵（但立即取消）
                ]
                
                interaction = random.choice(interactions)
                interaction()
                time.sleep(random.uniform(0.5, 1.5))
                
                # 如果是右鍵，按 ESC 取消
                if interaction == interactions[2]:
                    actions.send_keys(Keys.ESCAPE).perform()
                    
            except:
                pass
    
    print("✅ 人類行為模擬完成")

# 人性化設定
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

# 反檢測設定
chrome_options = Options()
chrome_options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# 減少日誌輸出
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-gpu-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")

# 提升穩定性
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--disable-ipc-flooding-protection")

print("🚀 正在啟動 Chrome 瀏覽器...")

try:
    # 直接使用系統 PATH 中的 chromedriver（避免 WebDriverManager 的問題）
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ 使用系統 ChromeDriver 成功啟動")
except Exception as e1:
    print(f"⚠️ 系統 ChromeDriver 失敗: {e1}")
    print("🔄 嘗試使用 WebDriverManager...")
    try:
        # 備用方案：使用 WebDriverManager
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print("✅ 使用 WebDriverManager 成功啟動")
    except Exception as e2:
        print(f"❌ WebDriverManager 也失敗: {e2}")
        print("📋 解決方案：")
        print("1. 確保已安裝 Chrome 瀏覽器")
        print("2. 下載對應版本的 ChromeDriver 並放入 PATH")
        print("3. 或使用 'pip install webdriver-manager' 重新安裝")
        exit(1)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get("https://www.instagram.com/")
enter_username = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'username')))
enter_username.send_keys(username)
   
enter_password = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'password')))
enter_password.send_keys(password)
enter_password.send_keys(Keys.RETURN)
time.sleep(random.randint(1,4))

try:
    not_now = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mt3GC')))
    a= not_now.find_elements_by_tag_name("button")[1]
    actions = ActionChains(driver)
    actions.click(a)
    actions.perform()
except:
    pass
   
finally:
    # 先模擬正常瀏覽行為
    print("🔄 開始模擬正常用戶行為...")
    
    # 瀏覽首頁
    driver.get("https://www.instagram.com/")
    time.sleep(random.randint(3, 8))
    
    # 隨機滾動首頁
    for _ in range(random.randint(2, 5)):
        driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(300, 800))
        time.sleep(random.randint(1, 3))
    
    # 目標 Reel 網址列表（混合不同內容）
    target_reels = [
        "https://www.instagram.com/reel/DNKYwvRxtBd/",  # 主要目標
        
        # 可以添加其他 reels 作為混淆
    ]
    
    # 減少觀看次數以降低風險
    max_views = 120  # 從 500 降到 20
    target_views = 50  # 目標 reel 的觀看次數
    
    for i in range(max_views):
        print(f"📺 第 {i+1}/{max_views} 次觀看")
        
        # 60% 機率觀看目標 reel，40% 觀看其他內容
        if random.random() < 0.6 and target_views < 100:  # 最多 100 次觀看目標
            url = target_reels[0]
            target_views += 1
            print(f"🎯 觀看目標內容 (第 {target_views} 次)")
        else:
            # 瀏覽探索頁面或其他用戶內容
            explore_urls = [
                "https://www.instagram.com/explore/",
                "https://www.instagram.com/reels/",
            ]
            url = random.choice(explore_urls)
            print(f"🔍 瀏覽其他內容: {url}")
        
        try:
            print(f"🌐 導航至: {url}")
            driver.get(url)
            
            # 等待頁面載入
            time.sleep(random.randint(2, 5))
            
            # 檢查是否成功載入頁面
            current_url = driver.current_url
            if "instagram.com" not in current_url:
                print(f"⚠️ 頁面載入異常，當前 URL: {current_url}")
                continue
            else:
                print(f"✅ 頁面載入成功")
                
        except Exception as e:
            print(f"❌ 導航失敗: {e}")
            print("🔄 跳過此次觀看，繼續下一個...")
            continue
        
        # 如果是 reel 或貼文，確保視頻開始播放
        if "reel" in url or "p/" in url:
            ensure_video_playing()
        
        # 模擬人類行為
        simulate_human_behavior()
        
        # 觀看時間：確保足夠長以計算觀看次數
        if "reel" in url or "p/" in url:
            # Instagram Reels 觀看次數計算標準：
            # - 至少 3 秒連續播放
            # - 視頻必須在可視區域
            # - 真實的用戶互動
            watch_time = random.randint(15, 45)  # 增加觀看時間確保計算
            print(f"🎯 目標內容觀看時間: {watch_time} 秒")
            
            # 分段觀看，模擬真實用戶行為
            segments = random.randint(2, 4)
            time_per_segment = watch_time // segments
            
            for segment in range(segments):
                print(f"📺 觀看片段 {segment + 1}/{segments} ({time_per_segment}秒)")
                
                # 每個片段中間添加微互動
                if segment > 0:
                    # 輕微滾動
                    scroll_amount = random.randint(-100, 100)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(0.5)
                    
                    # 隨機點擊視頻區域（重新確認播放）
                    try:
                        video_element = driver.find_element(By.TAG_NAME, "video")
                        actions = ActionChains(driver)
                        actions.move_to_element(video_element).click().perform()
                        time.sleep(0.5)
                    except:
                        pass
                
                time.sleep(time_per_segment)
                
        else:
            # 探索頁面瀏覽時間
            watch_time = random.randint(15, 20)
            print(f"🔍 探索頁面瀏覽時間: {watch_time} 秒")
            time.sleep(watch_time)
        
        # 觀看間隔：更長的隨機延遲
        if i < max_views - 1:  # 最後一次不需要延遲
            interval = random.randint(5, 30)  # 30秒到2分鐘
            print(f"💤 休息 {interval} 秒...")
            time.sleep(interval)