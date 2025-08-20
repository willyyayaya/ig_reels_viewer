<template>
  <div id="app">
    <el-container>
      <!-- 頭部導航 -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon><VideoCamera /></el-icon>
            <h1>Instagram Reels Viewer</h1>
          </div>
          <nav class="nav-menu">
            <router-link to="/" class="nav-link">
              <el-button type="primary" plain>
                <el-icon><Monitor /></el-icon>
                觀看任務
              </el-button>
            </router-link>
            <router-link to="/history" class="nav-link">
              <el-button type="info" plain>
                <el-icon><Document /></el-icon>
                歷史記錄
              </el-button>
            </router-link>
          </nav>
        </div>
      </el-header>

      <!-- 主要內容 -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- 頁腳 -->
      <el-footer class="app-footer">
        <div class="footer-content">
          <p>
            <el-icon><Warning /></el-icon>
            ⚠️ 注意：此工具僅供學習研究使用，請遵守Instagram使用條款
          </p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { VideoCamera, Monitor, Document, Warning } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-menu {
  display: flex;
  gap: 16px;
}

.nav-link {
  text-decoration: none;
}

.app-main {
  min-height: calc(100vh - 120px);
  background: #f5f7fa;
  padding: 20px;
}

.app-footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  height: auto !important;
  padding: 16px;
}

.footer-content p {
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9rem;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }
  
  .logo h1 {
    font-size: 1.2rem;
  }
  
  .app-main {
    padding: 16px;
  }
}
</style>

<style>
/* 全局樣式 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app {
  min-height: 100vh;
}

/* Element Plus 組件樣式調整 */
.el-button {
  font-weight: 500;
}

.el-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-form-item__label {
  font-weight: 500;
}
</style>
