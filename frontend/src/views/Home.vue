<template>
  <div class="space-y-8">
    <!-- 功能說明卡片 -->
    <el-card class="shadow-lg">
      <template #header>
        <div class="flex items-center space-x-2">
          <el-icon class="text-2xl instagram-text-gradient">
            <VideoPlay />
          </el-icon>
          <span class="text-xl font-bold">Instagram Reels 自動觀看工具</span>
        </div>
      </template>
      <div class="text-gray-600">
        <p class="mb-4">這是一個教育性質的工具，展示如何使用自動化技術與社交媒體平台互動。</p>
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 class="font-semibold text-yellow-800 mb-2">⚠️ 重要提醒：</h4>
          <ul class="text-sm text-yellow-700 space-y-1">
            <li>• 此工具僅供學習和研究目的</li>
            <li>• 實際使用可能違反 Instagram 使用條款</li>
            <li>• 請勿用於商業用途或大量操作</li>
            <li>• 使用者需自行承擔風險</li>
          </ul>
        </div>
      </div>
    </el-card>

    <!-- 主要操作區域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 左側：新增任務 -->
      <el-card class="shadow-lg">
        <template #header>
          <div class="flex items-center space-x-2">
            <el-icon class="text-lg text-blue-500">
              <Plus />
            </el-icon>
            <span class="font-semibold">新增觀看任務</span>
          </div>
        </template>

        <el-form :model="taskForm" :rules="rules" ref="taskFormRef" label-width="120px">
          <el-form-item label="Reels 網址" prop="url">
            <el-input
              v-model="taskForm.url"
              placeholder="請輸入 Instagram Reels 網址"
              :prefix-icon="Link"
              class="w-full"
            />
            <div class="text-xs text-gray-500 mt-1">
              範例: https://www.instagram.com/reel/xxxxx/
            </div>
          </el-form-item>

          <el-form-item label="觀看次數" prop="viewCount">
            <el-input-number
              v-model="taskForm.viewCount"
              :min="1"
              :max="100"
              :step="1"
              class="w-full"
            />
            <div class="text-xs text-gray-500 mt-1">
              建議不要超過 10 次，避免被檢測
            </div>
          </el-form-item>

          <el-form-item label="延遲時間" prop="delay">
            <el-select v-model="taskForm.delay" placeholder="選擇延遲時間" class="w-full">
              <el-option label="1-3 秒 (快速)" value="fast" />
              <el-option label="3-5 秒 (正常)" value="normal" />
              <el-option label="5-10 秒 (安全)" value="safe" />
              <el-option label="10-20 秒 (超安全)" value="ultra-safe" />
            </el-select>
            <div class="text-xs text-gray-500 mt-1">
              延遲時間越長，越不容易被檢測
            </div>
          </el-form-item>

          <el-form-item label="模擬操作">
            <el-checkbox-group v-model="taskForm.simulateActions">
              <el-checkbox label="scroll" border>模擬滾動</el-checkbox>
              <el-checkbox label="pause" border>隨機暫停</el-checkbox>
              <el-checkbox label="volume" border>調整音量</el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item>
            <div class="flex space-x-4 w-full">
              <el-button
                type="primary"
                @click="submitTask"
                :loading="submitting"
                class="flex-1 instagram-gradient border-0"
              >
                <el-icon class="mr-2">
                  <VideoPlay />
                </el-icon>
                開始任務
              </el-button>
              <el-button @click="resetForm" class="flex-1">
                重置表單
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 右側：任務狀態 -->
      <el-card class="shadow-lg">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <el-icon class="text-lg text-green-500">
                <Monitor />
              </el-icon>
              <span class="font-semibold">任務狀態</span>
            </div>
            <el-button
              size="small"
              @click="refreshTasks"
              :loading="refreshing"
              circle
            >
              <el-icon>
                <Refresh />
              </el-icon>
            </el-button>
          </div>
        </template>

        <div v-if="tasks.length === 0" class="text-center text-gray-500 py-8">
          <el-icon class="text-6xl mb-4">
            <DocumentEmpty />
          </el-icon>
          <p>尚無任務記錄</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="border rounded-lg p-4 hover:shadow-md transition-shadow"
            :class="{
              'border-green-200 bg-green-50': task.status === 'completed',
              'border-blue-200 bg-blue-50': task.status === 'running',
              'border-red-200 bg-red-50': task.status === 'failed',
              'border-gray-200 bg-gray-50': task.status === 'pending'
            }"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-sm">任務 #{{ task.id }}</span>
              <el-tag
                :type="getStatusType(task.status)"
                size="small"
              >
                {{ getStatusText(task.status) }}
              </el-tag>
            </div>
            <div class="text-sm text-gray-600 mb-2">
              <div class="truncate">{{ task.url }}</div>
              <div>目標觀看次數: {{ task.target_views }} | 已完成: {{ task.completed_views }}</div>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :class="{
                  'bg-green-500': task.status === 'completed',
                  'bg-blue-500': task.status === 'running',
                  'bg-red-500': task.status === 'failed'
                }"
                :style="{ width: `${(task.completed_views / task.target_views) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t">
          <router-link to="/monitor">
            <el-button type="text" class="w-full">
              查看詳細監控 →
            </el-button>
          </router-link>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  VideoPlay,
  Plus,
  Link,
  Monitor,
  Refresh,
  DocumentEmpty
} from '@element-plus/icons-vue'
import { taskStore } from '@/stores/taskStore'

const store = taskStore()
const taskFormRef = ref()
const submitting = ref(false)
const refreshing = ref(false)

const taskForm = reactive({
  url: '',
  viewCount: 5,
  delay: 'normal',
  simulateActions: ['scroll', 'pause']
})

const rules = {
  url: [
    { required: true, message: '請輸入 Reels 網址', trigger: 'blur' },
    {
      pattern: /^https:\/\/(www\.)?instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/,
      message: '請輸入有效的 Instagram Reels 網址',
      trigger: 'blur'
    }
  ],
  viewCount: [
    { required: true, message: '請輸入觀看次數', trigger: 'blur' },
    { type: 'number', min: 1, max: 100, message: '觀看次數必須在 1-100 之間', trigger: 'blur' }
  ],
  delay: [
    { required: true, message: '請選擇延遲時間', trigger: 'change' }
  ]
}

const tasks = ref([])

const submitTask = async () => {
  if (!taskFormRef.value) return

  try {
    await taskFormRef.value.validate()
    
    // 顯示確認對話框
    await ElMessageBox.confirm(
      '您確定要執行此自動化任務嗎？請注意這可能違反 Instagram 使用條款。',
      '⚠️ 風險確認',
      {
        confirmButtonText: '我了解風險並繼續',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: true
      }
    )

    submitting.value = true
    
    const response = await store.createTask({
      url: taskForm.url,
      target_views: taskForm.viewCount,
      delay_type: taskForm.delay,
      simulate_actions: taskForm.simulateActions
    })

    if (response.success) {
      ElMessage.success('任務已成功建立！')
      resetForm()
      await refreshTasks()
    } else {
      ElMessage.error(response.message || '建立任務失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('提交失敗：' + (error.message || '未知錯誤'))
    }
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  if (taskFormRef.value) {
    taskFormRef.value.resetFields()
  }
  Object.assign(taskForm, {
    url: '',
    viewCount: 5,
    delay: 'normal',
    simulateActions: ['scroll', 'pause']
  })
}

const refreshTasks = async () => {
  refreshing.value = true
  try {
    const response = await store.getTasks()
    tasks.value = response.data || []
  } catch (error) {
    ElMessage.error('獲取任務列表失敗')
  } finally {
    refreshing.value = false
  }
}

const getStatusType = (status) => {
  const types = {
    pending: '',
    running: 'primary',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || ''
}

const getStatusText = (status) => {
  const texts = {
    pending: '等待中',
    running: '執行中',
    completed: '已完成',
    failed: '失敗'
  }
  return texts[status] || status
}

onMounted(() => {
  refreshTasks()
})
</script>

<style scoped>
.instagram-gradient {
  background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
}
</style>
