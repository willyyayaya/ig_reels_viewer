<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 警告提示 -->
    <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <el-icon class="h-5 w-5 text-red-500">
            <Warning />
          </el-icon>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium">
            ⚠️ 警告：此工具僅供教育和學習目的使用。自動化操作可能違反 Instagram 使用條款，可能導致帳號被封。請謹慎使用！
          </p>
        </div>
      </div>
    </div>

    <!-- Header -->
    <header class="instagram-gradient shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <h1 class="text-3xl font-bold text-white">
            📱 IG Reels Viewer
          </h1>
          <p class="text-white text-sm opacity-90">
            Educational Purpose Only
          </p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white text-center py-4 mt-auto">
      <p class="text-sm">
        © 2024 IG Reels Viewer - 僅供教育目的使用 | 請遵守 Instagram 使用條款
      </p>
    </footer>
  </div>
</template>

<script setup>
import { Warning } from '@element-plus/icons-vue'
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
}
</style>
