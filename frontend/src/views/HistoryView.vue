<template>
  <div class="history-view">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h2>
        <el-icon><Document /></el-icon>
        任務歷史記錄
      </h2>
      <p class="page-description">
        查看所有任務的執行歷史和詳細資訊
      </p>
    </div>

    <!-- 篩選和搜尋 -->
    <el-card class="filter-card">
      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :sm="12" :md="8">
          <el-select 
            v-model="statusFilter" 
            placeholder="選擇狀態篩選"
            style="width: 100%"
            clearable
            @change="loadFilteredTasks"
          >
            <el-option label="全部狀態" value="" />
            <el-option label="等待中" value="PENDING" />
            <el-option label="執行中" value="RUNNING" />
            <el-option label="已完成" value="COMPLETED" />
            <el-option label="失敗" value="FAILED" />
            <el-option label="已取消" value="CANCELLED" />
          </el-select>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="urlFilter"
            placeholder="搜尋URL關鍵字"
            clearable
            @input="handleUrlFilterChange"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        
        <el-col :xs="24" :sm="24" :md="8">
          <div class="filter-actions">
            <el-button 
              type="primary"
              @click="refreshAllTasks"
              :loading="loading"
            >
              <el-icon><Refresh /></el-icon>
              重新整理
            </el-button>
            
            <el-button 
              @click="clearFilters"
            >
              <el-icon><RefreshLeft /></el-icon>
              清除篩選
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 任務統計 -->
    <el-card class="statistics-card">
      <template #header>
        <span><el-icon><DataAnalysis /></el-icon> 統計資訊</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.totalCount }}</div>
            <div class="stat-label">總任務數</div>
          </div>
        </el-col>
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value success">{{ statistics.completedCount }}</div>
            <div class="stat-label">成功完成</div>
          </div>
        </el-col>
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value running">{{ statistics.runningCount }}</div>
            <div class="stat-label">執行中</div>
          </div>
        </el-col>
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value failed">{{ statistics.failedCount }}</div>
            <div class="stat-label">失敗</div>
          </div>
        </el-col>
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value warning">{{ statistics.pendingCount }}</div>
            <div class="stat-label">等待中</div>
          </div>
        </el-col>
        <el-col :xs="8" :sm="6" :md="4">
          <div class="stat-item">
            <div class="stat-value cancelled">{{ statistics.cancelledCount }}</div>
            <div class="stat-label">已取消</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 任務列表 -->
    <el-card class="tasks-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><List /></el-icon> 任務列表 ({{ filteredTasks.length }})</span>
          <div class="header-actions">
            <el-button 
              type="danger" 
              size="small"
              @click="deleteCompletedTasks"
              :disabled="completedTasks.length === 0"
            >
              <el-icon><Delete /></el-icon>
              清理已完成
            </el-button>
          </div>
        </div>
      </template>

      <!-- 載入狀態 -->
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="5" animated />
      </div>

      <!-- 空狀態 -->
      <div v-else-if="filteredTasks.length === 0" class="empty-state">
        <el-empty :description="getEmptyDescription()">
          <el-button type="primary" @click="$router.push('/')">
            建立新任務
          </el-button>
        </el-empty>
      </div>

      <!-- 任務表格 -->
      <el-table 
        v-else
        :data="paginatedTasks" 
        stripe
        class="tasks-table"
        @row-click="handleRowClick"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <div class="task-detail">
              <el-descriptions title="任務詳情" :column="2" border>
                <el-descriptions-item label="任務ID">
                  {{ row.id }}
                </el-descriptions-item>
                <el-descriptions-item label="建立時間">
                  {{ formatDateTime(row.createdAt) }}
                </el-descriptions-item>
                <el-descriptions-item label="開始時間">
                  {{ formatDateTime(row.startedAt) }}
                </el-descriptions-item>
                <el-descriptions-item label="完成時間">
                  {{ formatDateTime(row.completedAt) }}
                </el-descriptions-item>
                <el-descriptions-item label="目標觀看次數">
                  {{ row.viewCount }}
                </el-descriptions-item>
                <el-descriptions-item label="實際完成次數">
                  {{ row.completedCount }}
                </el-descriptions-item>
                <el-descriptions-item label="完成率">
                  {{ formatProgress(row) }}%
                </el-descriptions-item>
                <el-descriptions-item label="執行狀態">
                  <el-tag :type="getTaskStatusColor(row.status)">
                    {{ getTaskStatusText(row.status) }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="Instagram URL" :span="2">
                  <a :href="row.reelsUrl" target="_blank" class="reels-link">
                    {{ row.reelsUrl }}
                  </a>
                </el-descriptions-item>
                <el-descriptions-item 
                  v-if="row.errorMessage" 
                  label="錯誤訊息" 
                  :span="2"
                >
                  <el-alert
                    :title="row.errorMessage"
                    type="error"
                    show-icon
                    :closable="false"
                  />
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="狀態" width="100">
          <template #default="{ row }">
            <el-tag 
              :type="getTaskStatusColor(row.status)" 
              size="small"
            >
              {{ getTaskStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Instagram URL" min-width="200">
          <template #default="{ row }">
            <div class="url-cell">
              <a 
                :href="row.reelsUrl" 
                target="_blank" 
                class="reels-link"
              >
                {{ truncateUrl(row.reelsUrl) }}
              </a>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="進度" width="160">
          <template #default="{ row }">
            <div class="progress-cell">
              <div class="progress-text">
                {{ row.completedCount }}/{{ row.viewCount }}
              </div>
              <el-progress 
                :percentage="formatProgress(row)"
                :status="row.status === 'COMPLETED' ? 'success' : 
                         row.status === 'FAILED' ? 'exception' : 'primary'"
                :stroke-width="4"
                :show-text="false"
              />
            </div>
          </template>
        </el-table-column>

        <el-table-column label="建立時間" width="160">
          <template #default="{ row }">
            {{ formatDateTimeShort(row.createdAt) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button 
                v-if="row.status === 'PENDING'"
                type="warning" 
                size="small"
                @click.stop="cancelTask(row.id)"
              >
                取消
              </el-button>
              
              <el-button 
                v-if="row.status === 'RUNNING'"
                type="primary" 
                size="small"
                @click.stop="refreshTask(row.id)"
              >
                更新
              </el-button>
              
              <el-popconfirm
                title="確定要刪除這個任務嗎？"
                @confirm="deleteTask(row.id)"
                @cancel="$event.stopPropagation()"
              >
                <template #reference>
                  <el-button 
                    type="danger" 
                    size="small"
                    :disabled="row.status === 'RUNNING'"
                    @click.stop
                  >
                    刪除
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分頁 -->
      <div v-if="filteredTasks.length > pageSize" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredTasks.length"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTaskStore } from '@/stores/taskStore'
import {
  Document, Search, Refresh, RefreshLeft, DataAnalysis,
  List, Delete
} from '@element-plus/icons-vue'

// Store
const taskStore = useTaskStore()

// 響應式數據
const loading = ref(false)
const statusFilter = ref('')
const urlFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 計算屬性
const { tasks, statistics } = taskStore
const { 
  getTaskStatusText, 
  getTaskStatusColor, 
  formatDateTime, 
  formatProgress 
} = taskStore

const filteredTasks = computed(() => {
  let result = [...tasks.value]
  
  // 狀態篩選
  if (statusFilter.value) {
    result = result.filter(task => task.status === statusFilter.value)
  }
  
  // URL篩選
  if (urlFilter.value) {
    const keyword = urlFilter.value.toLowerCase()
    result = result.filter(task => 
      task.reelsUrl.toLowerCase().includes(keyword)
    )
  }
  
  // 按建立時間降序排序
  return result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredTasks.value.slice(start, end)
})

const completedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'COMPLETED')
)

// 方法
const loadFilteredTasks = async () => {
  if (statusFilter.value) {
    try {
      loading.value = true
      await taskStore.loadTasks() // 載入所有任務以支援本地篩選
    } catch (error) {
      ElMessage.error('載入任務失敗：' + error.message)
    } finally {
      loading.value = false
    }
  } else {
    await refreshAllTasks()
  }
}

const handleUrlFilterChange = () => {
  currentPage.value = 1 // 重設分頁
}

const refreshAllTasks = async () => {
  try {
    loading.value = true
    await taskStore.loadTasks()
    await taskStore.loadStatistics()
    ElMessage.success('資料已更新')
  } catch (error) {
    ElMessage.error('更新失敗：' + error.message)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  statusFilter.value = ''
  urlFilter.value = ''
  currentPage.value = 1
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
    
    // 檢查當前頁面是否還有數據
    const totalPages = Math.ceil(filteredTasks.value.length / pageSize.value)
    if (currentPage.value > totalPages && totalPages > 0) {
      currentPage.value = totalPages
    }
  } catch (error) {
    ElMessage.error('刪除失敗：' + error.message)
  }
}

const deleteCompletedTasks = async () => {
  try {
    await ElMessageBox.confirm(
      `確定要刪除所有 ${completedTasks.value.length} 個已完成的任務嗎？`,
      '批量刪除確認',
      {
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const deletePromises = completedTasks.value.map(task => 
      taskStore.deleteTask(task.id)
    )
    
    await Promise.all(deletePromises)
    ElMessage.success('已完成任務清理完成')
    currentPage.value = 1
    
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量刪除失敗：' + error.message)
    }
  }
}

const handleRowClick = (row) => {
  // 可以在這裡添加行點擊處理邏輯
  console.log('任務詳情:', row)
}

const handlePageChange = (page) => {
  currentPage.value = page
}

const getEmptyDescription = () => {
  if (statusFilter.value || urlFilter.value) {
    return '沒有符合篩選條件的任務'
  }
  return '尚無任務記錄'
}

const truncateUrl = (url, maxLength = 50) => {
  if (url.length <= maxLength) return url
  return url.substring(0, maxLength) + '...'
}

const formatDateTimeShort = (dateTime) => {
  if (!dateTime) return '-'
  return new Date(dateTime).toLocaleString('zh-TW', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 監聽篩選條件變化，重設分頁
watch([statusFilter, urlFilter], () => {
  currentPage.value = 1
})

// 生命週期
onMounted(async () => {
  await refreshAllTasks()
})
</script>

<style scoped>
.history-view {
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

.filter-card,
.statistics-card,
.tasks-card {
  margin-bottom: 24px;
}

.filter-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.statistics-card .stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-value.success { color: #67c23a; }
.stat-value.running { color: #409eff; }
.stat-value.failed { color: #f56c6c; }
.stat-value.warning { color: #e6a23c; }
.stat-value.cancelled { color: #909399; }

.stat-label {
  font-size: 0.9rem;
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.loading-state,
.empty-state {
  padding: 40px;
  text-align: center;
}

.tasks-table {
  margin-bottom: 20px;
}

.url-cell {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reels-link {
  color: #409eff;
  text-decoration: none;
}

.reels-link:hover {
  text-decoration: underline;
}

.progress-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.progress-text {
  font-size: 0.8rem;
  color: #606266;
  text-align: center;
}

.table-actions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.task-detail {
  padding: 20px;
  background: #fafafa;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .filter-actions {
    justify-content: stretch;
  }
  
  .filter-actions .el-button {
    flex: 1;
  }
  
  .page-header h2 {
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .table-actions {
    flex-direction: column;
  }
  
  .tasks-table {
    font-size: 0.9rem;
  }
}
</style>
