<template>
  <div class="home-view">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h2>
        <el-icon><VideoCamera /></el-icon>
        Instagram Reels 自動觀看
      </h2>
      <p class="page-description">
        輸入Instagram Reels連結和觀看次數，系統將自動執行觀看任務
      </p>
    </div>

    <!-- 統計資訊 -->
    <div class="statistics-section">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card pending">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.pendingCount }}</div>
              <div class="stat-label">等待中</div>
            </div>
            <el-icon class="stat-icon"><Clock /></el-icon>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card running">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.runningCount }}</div>
              <div class="stat-label">執行中</div>
            </div>
            <el-icon class="stat-icon"><VideoPlay /></el-icon>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card completed">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.completedCount }}</div>
              <div class="stat-label">已完成</div>
            </div>
            <el-icon class="stat-icon"><CircleCheck /></el-icon>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card failed">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.failedCount }}</div>
              <div class="stat-label">失敗</div>
            </div>
            <el-icon class="stat-icon"><CircleClose /></el-icon>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card cancelled">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.cancelledCount }}</div>
              <div class="stat-label">已取消</div>
            </div>
            <el-icon class="stat-icon"><Remove /></el-icon>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6" :lg="4">
          <el-card class="stat-card total">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.totalCount }}</div>
              <div class="stat-label">總計</div>
            </div>
            <el-icon class="stat-icon"><DataBoard /></el-icon>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 建立任務表單 -->
    <el-card class="task-form-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><Plus /></el-icon> 建立新的觀看任務</span>
        </div>
      </template>

      <el-form 
        ref="taskFormRef" 
        :model="taskForm" 
        :rules="taskRules" 
        label-width="120px"
        label-position="top"
        class="task-form"
      >
        <el-row :gutter="20">
          <el-col :xs="24" :sm="24" :md="16">
            <el-form-item label="Instagram Reels 網址" prop="reelsUrl">
              <el-input
                v-model="taskForm.reelsUrl"
                type="url"
                placeholder="請輸入 Instagram Reels 網址，例如：https://www.instagram.com/reel/abc123/"
                clearable
                size="large"
              >
                <template #prefix>
                  <el-icon><Link /></el-icon>
                </template>
              </el-input>
              <div class="form-help-text">
                支援格式：https://www.instagram.com/reel/xxx 或 https://www.instagram.com/p/xxx
              </div>
            </el-form-item>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="觀看次數" prop="viewCount">
              <el-input-number
                v-model="taskForm.viewCount"
                :min="1"
                :max="100"
                size="large"
                style="width: 100%"
                controls-position="right"
              />
              <div class="form-help-text">
                建議範圍：1-20次，避免過度使用
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button 
            type="primary" 
            size="large"
            :loading="loading"
            @click="submitTask"
            class="submit-btn"
          >
            <el-icon v-if="!loading"><VideoPlay /></el-icon>
            {{ loading ? '建立中...' : '開始觀看任務' }}
          </el-button>
          
          <el-button 
            size="large"
            @click="resetForm"
            :disabled="loading"
          >
            <el-icon><RefreshLeft /></el-icon>
            重設
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 最近任務列表 -->
    <el-card class="recent-tasks-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><Document /></el-icon> 最近任務</span>
          <el-button 
            type="primary" 
            plain 
            size="small"
            @click="refreshTasks"
            :loading="loading"
          >
            <el-icon><Refresh /></el-icon>
            重新整理
          </el-button>
        </div>
      </template>

      <div v-if="recentTasks.length === 0" class="empty-state">
        <el-empty description="尚無任務記錄">
          <el-button type="primary" @click="() => $refs.taskFormRef.$el.scrollIntoView()">
            建立第一個任務
          </el-button>
        </el-empty>
      </div>

      <div v-else class="tasks-list">
        <div 
          v-for="task in recentTasks" 
          :key="task.id" 
          class="task-item"
        >
          <div class="task-content">
            <div class="task-header">
              <el-tag 
                :type="getTaskStatusColor(task.status)" 
                size="small"
                class="task-status"
              >
                {{ getTaskStatusText(task.status) }}
              </el-tag>
              <span class="task-time">{{ formatDateTime(task.createdAt) }}</span>
            </div>
            
            <div class="task-url">
              <el-icon><Link /></el-icon>
              <a 
                :href="task.reelsUrl" 
                target="_blank" 
                class="reels-link"
              >
                {{ task.reelsUrl }}
              </a>
            </div>
            
            <div class="task-progress">
              <div class="progress-text">
                進度：{{ task.completedCount }} / {{ task.viewCount }} 次
                ({{ formatProgress(task) }}%)
              </div>
              <el-progress 
                :percentage="formatProgress(task)"
                :status="task.status === 'COMPLETED' ? 'success' : 
                         task.status === 'FAILED' ? 'exception' : 'primary'"
                :stroke-width="6"
              />
            </div>
            
            <div v-if="task.errorMessage" class="task-error">
              <el-alert
                :title="task.errorMessage"
                type="error"
                show-icon
                :closable="false"
                size="small"
              />
            </div>
          </div>
          
          <div class="task-actions">
            <el-button 
              v-if="task.status === 'PENDING'"
              type="warning" 
              size="small"
              @click="cancelTask(task.id)"
            >
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            
            <el-button 
              v-if="task.status === 'RUNNING'"
              type="primary" 
              size="small"
              @click="refreshTask(task.id)"
            >
              <el-icon><Refresh /></el-icon>
              更新
            </el-button>
            
            <el-popconfirm
              title="確定要刪除這個任務嗎？"
              @confirm="deleteTask(task.id)"
            >
              <template #reference>
                <el-button 
                  type="danger" 
                  size="small"
                  :disabled="task.status === 'RUNNING'"
                >
                  <el-icon><Delete /></el-icon>
                  刪除
                </el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTaskStore } from '@/stores/taskStore'
import {
  VideoCamera, VideoPlay, Clock, CircleCheck, CircleClose, Remove, DataBoard,
  Plus, Link, RefreshLeft, Refresh, Document, Close, Delete
} from '@element-plus/icons-vue'

// Store
const taskStore = useTaskStore()

// 響應式數據
const taskFormRef = ref()
const loading = ref(false)

const taskForm = reactive({
  reelsUrl: '',
  viewCount: 5
})

const taskRules = {
  reelsUrl: [
    { required: true, message: '請輸入Instagram Reels網址', trigger: 'blur' },
    { 
      pattern: /^https:\/\/www\.instagram\.com\/(reel|p)\/[a-zA-Z0-9_-]+\/?.*$/,
      message: '請輸入有效的Instagram Reels或貼文網址',
      trigger: 'blur'
    }
  ],
  viewCount: [
    { required: true, message: '請輸入觀看次數', trigger: 'blur' },
    { type: 'number', min: 1, max: 100, message: '觀看次數必須在1-100之間', trigger: 'blur' }
  ]
}

// 計算屬性
const { statistics, recentTasks } = taskStore
const { 
  getTaskStatusText, 
  getTaskStatusColor, 
  formatDateTime, 
  formatProgress 
} = taskStore

// 方法
const submitTask = async () => {
  try {
    await taskFormRef.value.validate()
    
    loading.value = true
    
    await taskStore.createTask(taskForm.reelsUrl, taskForm.viewCount)
    
    ElMessage.success('任務建立成功！系統將在背景執行觀看任務。')
    resetForm()
    
  } catch (error) {
    if (error.errors) {
      // 表單驗證錯誤
      return
    }
    
    console.error('建立任務失敗:', error)
    ElMessage.error(error.message || '建立任務失敗，請稍後再試')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  taskFormRef.value?.resetFields()
  taskForm.reelsUrl = ''
  taskForm.viewCount = 5
}

const refreshTasks = async () => {
  try {
    loading.value = true
    await taskStore.refreshAllTasks()
    ElMessage.success('資料已更新')
  } catch (error) {
    ElMessage.error('更新失敗：' + error.message)
  } finally {
    loading.value = false
  }
}

const refreshTask = async (taskId) => {
  try {
    await taskStore.refreshTask(taskId)
    ElMessage.success('任務狀態已更新')
  } catch (error) {
    ElMessage.error('更新失敗：' + error.message)
  }
}

const cancelTask = async (taskId) => {
  try {
    await taskStore.cancelTask(taskId)
    ElMessage.success('任務已取消')
  } catch (error) {
    ElMessage.error('取消失敗：' + error.message)
  }
}

const deleteTask = async (taskId) => {
  try {
    await taskStore.deleteTask(taskId)
    ElMessage.success('任務已刪除')
  } catch (error) {
    ElMessage.error('刪除失敗：' + error.message)
  }
}

// 生命週期
onMounted(async () => {
  try {
    await taskStore.refreshAllTasks()
  } catch (error) {
    console.error('載入資料失敗:', error)
  }
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 0 0 12px 0;
  font-size: 2rem;
  color: #2c3e50;
}

.page-description {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin: 0;
}

.statistics-section {
  margin-bottom: 32px;
}

.stat-card {
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  position: relative;
  z-index: 2;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.stat-icon {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 1.5rem;
  opacity: 0.3;
}

.stat-card.pending .stat-number { color: #e6a23c; }
.stat-card.running .stat-number { color: #409eff; }
.stat-card.completed .stat-number { color: #67c23a; }
.stat-card.failed .stat-number { color: #f56c6c; }
.stat-card.cancelled .stat-number { color: #909399; }
.stat-card.total .stat-number { color: #606266; }

.task-form-card,
.recent-tasks-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.task-form {
  margin-top: 16px;
}

.form-help-text {
  font-size: 0.8rem;
  color: #909399;
  margin-top: 4px;
}

.submit-btn {
  font-size: 1rem;
  padding: 12px 24px;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fafafa;
  transition: all 0.2s;
}

.task-item:hover {
  background: #f5f7fa;
  border-color: #c6e2ff;
}

.task-content {
  flex: 1;
  margin-right: 16px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.task-time {
  font-size: 0.9rem;
  color: #909399;
}

.task-url {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.reels-link {
  color: #409eff;
  text-decoration: none;
  word-break: break-all;
}

.reels-link:hover {
  text-decoration: underline;
}

.task-progress {
  margin-bottom: 8px;
}

.progress-text {
  font-size: 0.9rem;
  color: #606266;
  margin-bottom: 4px;
}

.task-error {
  margin-top: 8px;
}

.task-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .page-header h2 {
    font-size: 1.5rem;
  }
  
  .task-item {
    flex-direction: column;
    gap: 16px;
  }
  
  .task-content {
    margin-right: 0;
  }
  
  .task-actions {
    flex-direction: row;
    align-self: stretch;
  }
}
</style>
