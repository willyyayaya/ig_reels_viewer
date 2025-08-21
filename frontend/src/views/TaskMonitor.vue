<template>
  <div class="space-y-6">
    <!-- 頁面標題 -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">任務監控中心</h1>
      <div class="flex space-x-2">
        <el-button @click="refreshTasks" :loading="loading" size="small">
          <el-icon class="mr-1">
            <Refresh />
          </el-icon>
          刷新
        </el-button>
        <router-link to="/">
          <el-button type="primary" size="small">
            <el-icon class="mr-1">
              <Back />
            </el-icon>
            返回首頁
          </el-button>
        </router-link>
      </div>
    </div>

    <!-- 統計卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <el-card class="text-center">
        <div class="text-3xl font-bold text-blue-600">{{ stats.total }}</div>
        <div class="text-sm text-gray-500">總任務數</div>
      </el-card>
      <el-card class="text-center">
        <div class="text-3xl font-bold text-yellow-600">{{ stats.running }}</div>
        <div class="text-sm text-gray-500">執行中</div>
      </el-card>
      <el-card class="text-center">
        <div class="text-3xl font-bold text-green-600">{{ stats.completed }}</div>
        <div class="text-sm text-gray-500">已完成</div>
      </el-card>
      <el-card class="text-center">
        <div class="text-3xl font-bold text-red-600">{{ stats.failed }}</div>
        <div class="text-sm text-gray-500">失敗</div>
      </el-card>
    </div>

    <!-- 任務列表 -->
    <el-card>
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-semibold">任務詳情</span>
          <div class="flex items-center space-x-2">
            <el-select v-model="filterStatus" placeholder="篩選狀態" size="small" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="等待中" value="pending" />
              <el-option label="執行中" value="running" />
              <el-option label="已完成" value="completed" />
              <el-option label="失敗" value="failed" />
            </el-select>
            <el-switch
              v-model="autoRefresh"
              @change="toggleAutoRefresh"
              active-text="自動刷新"
              size="small"
            />
          </div>
        </div>
      </template>

      <el-table :data="filteredTasks" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="網址" min-width="300">
          <template #default="scope">
            <div class="flex items-center space-x-2">
              <el-link :href="scope.row.url" target="_blank" type="primary" class="truncate">
                {{ scope.row.url }}
              </el-link>
              <el-button
                size="small"
                @click="copyUrl(scope.row.url)"
                circle
                type="text"
              >
                <el-icon>
                  <CopyDocument />
                </el-icon>
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="進度" width="200">
          <template #default="scope">
            <div class="space-y-1">
              <div class="flex justify-between text-sm">
                <span>{{ scope.row.completed_views }}/{{ scope.row.target_views }}</span>
                <span>{{ Math.round((scope.row.completed_views / scope.row.target_views) * 100) }}%</span>
              </div>
              <el-progress
                :percentage="Math.round((scope.row.completed_views / scope.row.target_views) * 100)"
                :status="getProgressStatus(scope.row.status)"
                :stroke-width="6"
                :show-text="false"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="狀態" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="延遲設置" width="120">
          <template #default="scope">
            <el-tag type="info" size="small">
              {{ getDelayText(scope.row.delay_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="建立時間" width="180">
          <template #default="scope">
            <div class="text-sm text-gray-600">
              {{ formatDate(scope.row.created_at) }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <div class="flex space-x-1">
              <el-button
                v-if="scope.row.status === 'running'"
                size="small"
                type="danger"
                @click="stopTask(scope.row.id)"
              >
                停止
              </el-button>
              <el-button
                v-if="scope.row.status === 'failed'"
                size="small"
                type="warning"
                @click="retryTask(scope.row.id)"
              >
                重試
              </el-button>
              <el-button
                size="small"
                @click="viewTaskDetails(scope.row)"
              >
                詳情
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 任務詳情對話框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="任務詳情"
      width="600px"
    >
      <div v-if="selectedTask" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">任務ID</label>
            <p class="mt-1 text-sm text-gray-900">{{ selectedTask.id }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">狀態</label>
            <el-tag :type="getStatusType(selectedTask.status)" class="mt-1">
              {{ getStatusText(selectedTask.status) }}
            </el-tag>
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700">目標網址</label>
            <p class="mt-1 text-sm text-gray-900 break-all">{{ selectedTask.url }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">目標觀看次數</label>
            <p class="mt-1 text-sm text-gray-900">{{ selectedTask.target_views }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">已完成次數</label>
            <p class="mt-1 text-sm text-gray-900">{{ selectedTask.completed_views }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">延遲設置</label>
            <p class="mt-1 text-sm text-gray-900">{{ getDelayText(selectedTask.delay_type) }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">建立時間</label>
            <p class="mt-1 text-sm text-gray-900">{{ formatDate(selectedTask.created_at) }}</p>
          </div>
        </div>
        
        <div v-if="selectedTask.error_message">
          <label class="block text-sm font-medium text-gray-700">錯誤訊息</label>
          <div class="mt-1 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-800">{{ selectedTask.error_message }}</p>
          </div>
        </div>

        <div v-if="selectedTask.logs && selectedTask.logs.length > 0">
          <label class="block text-sm font-medium text-gray-700 mb-2">執行日誌</label>
          <div class="max-h-40 overflow-y-auto bg-gray-50 border rounded-lg p-3">
            <div
              v-for="(log, index) in selectedTask.logs"
              :key="index"
              class="text-xs text-gray-600 mb-1"
            >
              <span class="font-mono">{{ formatDate(log.timestamp) }}</span>
              <span class="ml-2">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Refresh,
  Back,
  CopyDocument
} from '@element-plus/icons-vue'
import { taskStore } from '@/stores/taskStore'

const store = taskStore()
const loading = ref(false)
const autoRefresh = ref(false)
const refreshInterval = ref(null)
const filterStatus = ref('')
const detailDialogVisible = ref(false)
const selectedTask = ref(null)
const tasks = ref([])

const stats = computed(() => {
  const total = tasks.value.length
  const running = tasks.value.filter(t => t.status === 'running').length
  const completed = tasks.value.filter(t => t.status === 'completed').length
  const failed = tasks.value.filter(t => t.status === 'failed').length
  
  return { total, running, completed, failed }
})

const filteredTasks = computed(() => {
  if (!filterStatus.value) return tasks.value
  return tasks.value.filter(task => task.status === filterStatus.value)
})

const refreshTasks = async () => {
  loading.value = true
  try {
    const response = await store.getTasks()
    tasks.value = response.data || []
  } catch (error) {
    ElMessage.error('獲取任務列表失敗')
  } finally {
    loading.value = false
  }
}

const toggleAutoRefresh = (enabled) => {
  if (enabled) {
    refreshInterval.value = setInterval(refreshTasks, 5000) // 每5秒刷新
    ElMessage.success('已開啟自動刷新（每5秒）')
  } else {
    if (refreshInterval.value) {
      clearInterval(refreshInterval.value)
      refreshInterval.value = null
    }
    ElMessage.info('已關閉自動刷新')
  }
}

const stopTask = async (taskId) => {
  try {
    await ElMessageBox.confirm('確定要停止此任務嗎？', '確認停止', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await store.stopTask(taskId)
    ElMessage.success('任務已停止')
    await refreshTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('停止任務失敗')
    }
  }
}

const retryTask = async (taskId) => {
  try {
    await store.retryTask(taskId)
    ElMessage.success('任務已重新開始')
    await refreshTasks()
  } catch (error) {
    ElMessage.error('重試任務失敗')
  }
}

const viewTaskDetails = (task) => {
  selectedTask.value = task
  detailDialogVisible.value = true
}

const copyUrl = async (url) => {
  try {
    await navigator.clipboard.writeText(url)
    ElMessage.success('網址已複製到剪貼簿')
  } catch (error) {
    ElMessage.error('複製失敗')
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

const getProgressStatus = (status) => {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return null
}

const getDelayText = (delayType) => {
  const texts = {
    fast: '快速',
    normal: '正常',
    safe: '安全',
    'ultra-safe': '超安全'
  }
  return texts[delayType] || delayType
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-TW')
}

onMounted(() => {
  refreshTasks()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>
