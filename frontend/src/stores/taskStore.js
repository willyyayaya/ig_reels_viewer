import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import taskApi from '@/services/taskApi'

export const useTaskStore = defineStore('task', () => {
  // 狀態
  const tasks = ref([])
  const currentTask = ref(null)
  const loading = ref(false)
  const statistics = ref({
    pendingCount: 0,
    runningCount: 0,
    completedCount: 0,
    failedCount: 0,
    cancelledCount: 0,
    totalCount: 0
  })

  // 計算屬性
  const runningTasks = computed(() => 
    tasks.value.filter(task => task.status === 'RUNNING')
  )

  const recentTasks = computed(() => 
    tasks.value
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      .slice(0, 10)
  )

  // 行為
  const createTask = async (reelsUrl, viewCount) => {
    loading.value = true
    try {
      const response = await taskApi.createTask({ reelsUrl, viewCount })
      tasks.value.unshift(response.data)
      await loadStatistics()
      return response.data
    } catch (error) {
      console.error('建立任務失敗:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const loadTasks = async () => {
    loading.value = true
    try {
      const response = await taskApi.getAllTasks()
      tasks.value = response.data
    } catch (error) {
      console.error('載入任務失敗:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const loadRecentTasks = async (limit = 20) => {
    loading.value = true
    try {
      const response = await taskApi.getRecentTasks(limit)
      tasks.value = response.data
    } catch (error) {
      console.error('載入最近任務失敗:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const loadTask = async (taskId) => {
    try {
      const response = await taskApi.getTask(taskId)
      currentTask.value = response.data
      
      // 更新tasks列表中的對應項目
      const index = tasks.value.findIndex(task => task.id === taskId)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      
      return response.data
    } catch (error) {
      console.error('載入任務詳情失敗:', error)
      throw error
    }
  }

  const cancelTask = async (taskId) => {
    try {
      await taskApi.cancelTask(taskId)
      await loadTask(taskId)
      await loadStatistics()
    } catch (error) {
      console.error('取消任務失敗:', error)
      throw error
    }
  }

  const deleteTask = async (taskId) => {
    try {
      await taskApi.deleteTask(taskId)
      tasks.value = tasks.value.filter(task => task.id !== taskId)
      await loadStatistics()
    } catch (error) {
      console.error('刪除任務失敗:', error)
      throw error
    }
  }

  const loadStatistics = async () => {
    try {
      const response = await taskApi.getStatistics()
      statistics.value = response.data
    } catch (error) {
      console.error('載入統計資料失敗:', error)
    }
  }

  const refreshTask = async (taskId) => {
    return await loadTask(taskId)
  }

  const refreshAllTasks = async () => {
    await loadRecentTasks()
    await loadStatistics()
  }

  // 工具函數
  const getTaskStatusText = (status) => {
    const statusMap = {
      PENDING: '等待中',
      RUNNING: '執行中',
      COMPLETED: '已完成',
      FAILED: '失敗',
      CANCELLED: '已取消'
    }
    return statusMap[status] || '未知'
  }

  const getTaskStatusColor = (status) => {
    const colorMap = {
      PENDING: 'warning',
      RUNNING: 'primary',
      COMPLETED: 'success',
      FAILED: 'danger',
      CANCELLED: 'info'
    }
    return colorMap[status] || 'info'
  }

  const formatDateTime = (dateTime) => {
    if (!dateTime) return '-'
    return new Date(dateTime).toLocaleString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  const formatProgress = (task) => {
    if (!task || task.viewCount === 0) return 0
    return Math.round((task.completedCount / task.viewCount) * 100)
  }

  return {
    // 狀態
    tasks,
    currentTask,
    loading,
    statistics,
    
    // 計算屬性
    runningTasks,
    recentTasks,
    
    // 行為
    createTask,
    loadTasks,
    loadRecentTasks,
    loadTask,
    cancelTask,
    deleteTask,
    loadStatistics,
    refreshTask,
    refreshAllTasks,
    
    // 工具函數
    getTaskStatusText,
    getTaskStatusColor,
    formatDateTime,
    formatProgress
  }
})
