"""
Instagram 自動化服務
⚠️ 警告：此模組僅供教育目的使用，實際使用可能違反 Instagram 使用條款
"""

import asyncio
import random
import time
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

from app.core.config import settings, DELAY_SETTINGS, USER_AGENTS

class InstagramAutomation:
    """
    Instagram 自動化服務
    
    ⚠️ 重要警告：
    - 此類別僅供教育和研究目的使用
    - 實際使用可能違反 Instagram 使用條款
    - 可能導致帳號被暫停或永久封禁
    - 使用者需自行承擔所有風險
    """
    
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.driver = None
        self.wait = None
        self.is_running = False
        self.should_stop = False
        
    async def setup_driver(self) -> bool:
        """設置 WebDriver"""
        try:
            logger.info(f"🔧 任務 {self.task_id}: 正在設置 WebDriver...")
            
            chrome_options = Options()
            
            # 基本設定
            if settings.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            
            # 反檢測設定
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 隨機使用者代理
            if settings.USER_AGENT_ROTATION:
                user_agent = random.choice(USER_AGENTS)
                chrome_options.add_argument(f"--user-agent={user_agent}")
                logger.info(f"🎭 使用隨機 User Agent: {user_agent[:50]}...")
            
            # 視窗大小隨機化
            widths = [1366, 1920, 1440, 1280]
            heights = [768, 1080, 900, 720]
            width = random.choice(widths)
            height = random.choice(heights)
            chrome_options.add_argument(f"--window-size={width},{height}")
            
            # 其他反檢測設定
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # 提高載入速度
            
            # 建立驅動程式
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
            
            # 移除 webdriver 屬性
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 設置等待
            self.wait = WebDriverWait(self.driver, settings.WEBDRIVER_TIMEOUT)
            
            # 設置隱式等待
            self.driver.implicitly_wait(10)
            
            logger.info(f"✅ 任務 {self.task_id}: WebDriver 設置完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 任務 {self.task_id}: WebDriver 設置失敗: {str(e)}")
            return False
    
    async def navigate_to_reel(self, url: str) -> bool:
        """導航到 Reels 頁面"""
        try:
            logger.info(f"🔗 任務 {self.task_id}: 正在導航到 {url}")
            
            # 先訪問 Instagram 主頁以建立 session
            self.driver.get("https://www.instagram.com")
            await asyncio.sleep(random.uniform(2, 4))
            
            # 檢查是否需要處理 cookie 同意
            await self._handle_cookie_consent()
            
            # 導航到目標 Reel
            self.driver.get(url)
            await asyncio.sleep(random.uniform(3, 6))
            
            # 檢查頁面是否正確載入
            if await self._verify_reel_page():
                logger.info(f"✅ 任務 {self.task_id}: 成功導航到 Reel 頁面")
                return True
            else:
                logger.error(f"❌ 任務 {self.task_id}: Reel 頁面載入失敗")
                return False
                
        except Exception as e:
            logger.error(f"❌ 任務 {self.task_id}: 導航失敗: {str(e)}")
            return False
    
    async def perform_view(
        self,
        view_number: int,
        delay_type: str,
        simulate_actions: list
    ) -> bool:
        """執行一次觀看操作"""
        try:
            if self.should_stop:
                return False
            
            logger.info(f"👁️ 任務 {self.task_id}: 開始第 {view_number} 次觀看")
            
            # 刷新頁面以模擬新的觀看
            if view_number > 1:
                await self._refresh_page()
            
            # 等待視頻載入
            await self._wait_for_video_load()
            
            # 確保視頻正在播放
            await self._ensure_video_playing()
            
            # 執行模擬操作
            if simulate_actions:
                await self._perform_simulate_actions(simulate_actions)
            
            # 觀看延遲
            view_duration = await self._get_view_duration(delay_type)
            logger.info(f"⏱️ 任務 {self.task_id}: 觀看 {view_duration:.1f} 秒")
            
            await asyncio.sleep(view_duration)
            
            logger.info(f"✅ 任務 {self.task_id}: 第 {view_number} 次觀看完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 任務 {self.task_id}: 第 {view_number} 次觀看失敗: {str(e)}")
            return False
    
    async def _handle_cookie_consent(self):
        """處理 Cookie 同意對話框"""
        try:
            # 查找並點擊 "Accept All" 或類似按鈕
            cookie_buttons = [
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Allow')]",
                "//button[contains(text(), '接受')]",
                "//button[contains(text(), '同意')]"
            ]
            
            for button_xpath in cookie_buttons:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    button.click()
                    logger.info(f"🍪 任務 {self.task_id}: 已處理 Cookie 同意")
                    await asyncio.sleep(1)
                    return
                except TimeoutException:
                    continue
                    
        except Exception as e:
            logger.debug(f"任務 {self.task_id}: Cookie 對話框處理: {str(e)}")
    
    async def _verify_reel_page(self) -> bool:
        """驗證是否成功載入 Reel 頁面"""
        try:
            # 檢查是否有視頻元素
            video_selectors = [
                "video",
                "[role='button'][tabindex='0']",
                "article video"
            ]
            
            for selector in video_selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    return True
                except TimeoutException:
                    continue
            
            return False
            
        except Exception:
            return False
    
    async def _refresh_page(self):
        """刷新頁面"""
        try:
            logger.debug(f"🔄 任務 {self.task_id}: 刷新頁面")
            self.driver.refresh()
            await asyncio.sleep(random.uniform(2, 4))
            
        except Exception as e:
            logger.error(f"❌ 任務 {self.task_id}: 頁面刷新失敗: {str(e)}")
    
    async def _wait_for_video_load(self):
        """等待視頻載入"""
        try:
            # 等待視頻元素出現
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
            await asyncio.sleep(random.uniform(1, 3))
            
        except TimeoutException:
            logger.warning(f"⚠️ 任務 {self.task_id}: 視頻載入超時")
    
    async def _ensure_video_playing(self):
        """確保視頻正在播放"""
        try:
            # 嘗試點擊播放按鈕（如果存在）
            play_button_selectors = [
                "[aria-label*='play']",
                "[aria-label*='Play']",
                "button[aria-label*='播放']"
            ]
            
            for selector in play_button_selectors:
                try:
                    play_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if play_button.is_displayed():
                        play_button.click()
                        logger.debug(f"▶️ 任務 {self.task_id}: 點擊播放按鈕")
                        await asyncio.sleep(1)
                        break
                except:
                    continue
                    
        except Exception as e:
            logger.debug(f"任務 {self.task_id}: 播放按鈕處理: {str(e)}")
    
    async def _perform_simulate_actions(self, actions: list):
        """執行模擬操作"""
        try:
            for action in actions:
                if self.should_stop:
                    break
                    
                if action == "scroll":
                    await self._simulate_scroll()
                elif action == "pause":
                    await self._simulate_pause()
                elif action == "volume":
                    await self._simulate_volume_adjust()
                
                # 動作間隨機延遲
                await asyncio.sleep(random.uniform(0.5, 2))
                
        except Exception as e:
            logger.debug(f"任務 {self.task_id}: 模擬操作錯誤: {str(e)}")
    
    async def _simulate_scroll(self):
        """模擬滾動操作"""
        try:
            actions = ActionChains(self.driver)
            # 隨機滾動
            scroll_amount = random.randint(-200, 200)
            actions.scroll_by_amount(0, scroll_amount).perform()
            logger.debug(f"📜 任務 {self.task_id}: 模擬滾動")
            
        except Exception as e:
            logger.debug(f"滾動模擬失敗: {str(e)}")
    
    async def _simulate_pause(self):
        """模擬暫停操作"""
        try:
            # 隨機暫停 1-3 秒
            pause_duration = random.uniform(1, 3)
            logger.debug(f"⏸️ 任務 {self.task_id}: 模擬暫停 {pause_duration:.1f} 秒")
            await asyncio.sleep(pause_duration)
            
        except Exception as e:
            logger.debug(f"暫停模擬失敗: {str(e)}")
    
    async def _simulate_volume_adjust(self):
        """模擬音量調整"""
        try:
            # 嘗試找到音量控制並點擊
            volume_selectors = [
                "[aria-label*='volume']",
                "[aria-label*='sound']",
                "[aria-label*='音量']"
            ]
            
            for selector in volume_selectors:
                try:
                    volume_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if volume_button.is_displayed():
                        volume_button.click()
                        logger.debug(f"🔊 任務 {self.task_id}: 模擬音量調整")
                        await asyncio.sleep(0.5)
                        # 再點一次恢復
                        volume_button.click()
                        break
                except:
                    continue
                    
        except Exception as e:
            logger.debug(f"音量調整模擬失敗: {str(e)}")
    
    async def _get_view_duration(self, delay_type: str) -> float:
        """獲取觀看持續時間"""
        delay_config = DELAY_SETTINGS.get(delay_type, DELAY_SETTINGS["normal"])
        min_delay = delay_config["min"]
        max_delay = delay_config["max"]
        
        # 添加額外的隨機性
        base_duration = random.uniform(min_delay, max_delay)
        # 偶爾添加更長的觀看時間以模擬真實用戶行為
        if random.random() < 0.1:  # 10% 機率
            base_duration *= random.uniform(1.5, 2.5)
        
        return base_duration
    
    def stop(self):
        """停止自動化任務"""
        logger.info(f"🛑 任務 {self.task_id}: 收到停止信號")
        self.should_stop = True
    
    async def cleanup(self):
        """清理資源"""
        try:
            if self.driver:
                logger.info(f"🧹 任務 {self.task_id}: 正在清理 WebDriver")
                self.driver.quit()
                self.driver = None
                
        except Exception as e:
            logger.error(f"❌ 任務 {self.task_id}: 清理失敗: {str(e)}")
    
    def __del__(self):
        """析構函數"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
