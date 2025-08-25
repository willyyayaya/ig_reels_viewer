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

def simulate_human_behavior():
    """模擬人類瀏覽行為"""
    global driver
    actions = ActionChains(driver)
    
    # 隨機選擇 1-3 種行為
    behaviors = []
    
    # 滾動行為 (80% 機率)
    if random.random() < 0.8:
        behaviors.append("scroll")
    
    # 暫停行為 (30% 機率)
    if random.random() < 0.3:
        behaviors.append("pause")
    
    # 點擊行為 (20% 機率)
    if random.random() < 0.2:
        behaviors.append("click")
    
    for behavior in behaviors:
        if behavior == "scroll":
            # 隨機滾動
            scroll_amount = random.randint(-300, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 2))
            
        elif behavior == "pause":
            # 隨機暫停
            time.sleep(random.uniform(1, 4))
            
        elif behavior == "click":
            # 嘗試點擊無害的元素（如空白區域）
            try:
                actions.move_by_offset(
                    random.randint(100, 400), 
                    random.randint(100, 400)
                ).click().perform()
                time.sleep(random.uniform(0.5, 1.5))
            except:
                pass

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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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
        "https://www.instagram.com/p/DNpRhVMpyS0/",  # 主要目標
        "https://www.instagram.com/reel/DNkEYnFpzXH/",
        "https://www.instagram.com/reel/DNXhuRKpuG5/"
        # 可以添加其他 reels 作為混淆
    ]
    
    # 減少觀看次數以降低風險
    max_views = 20  # 從 500 降到 20
    target_views = 0  # 目標 reel 的觀看次數
    
    for i in range(max_views):
        print(f"📺 第 {i+1}/{max_views} 次觀看")
        
        # 60% 機率觀看目標 reel，40% 觀看其他內容
        if random.random() < 0.6 and target_views < 12:  # 最多 12 次觀看目標
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
        
        driver.get(url)
        
        # 等待頁面載入
        time.sleep(random.randint(2, 5))
        
        # 模擬人類行為
        simulate_human_behavior()
        
        # 觀看時間：確保足夠長以計算觀看次數
        if "reel" in url or "p/" in url:
            # Reels/貼文需要至少 3-5 秒才計算觀看，我們設 8-25 秒更安全
            watch_time = random.randint(8, 25)
            print(f"🎯 目標內容觀看時間: {watch_time} 秒")
        else:
            # 探索頁面瀏覽時間
            watch_time = random.randint(15, 45)
            print(f"🔍 探索頁面瀏覽時間: {watch_time} 秒")
            
        print(f"⏰ 觀看 {watch_time} 秒")
        time.sleep(watch_time)
        
        # 觀看間隔：更長的隨機延遲
        if i < max_views - 1:  # 最後一次不需要延遲
            interval = random.randint(30, 120)  # 30秒到2分鐘
            print(f"💤 休息 {interval} 秒...")
            time.sleep(interval)