import { defineStore } from 'pinia'
import axios from 'axios'

// 配置 axios 基礎設定
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  config => {
    // 可以在這裡添加認證 token
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 響應攔截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.message || error.message || '請求失敗'
    return Promise.reject(new Error(message))
  }
)

export const taskStore = defineStore('task', {
  state: () => ({
    tasks: [],
    currentTask: null,
    loading: false,
    error: null
  }),

  getters: {
    runningTasks: (state) => state.tasks.filter(task => task.status === 'running'),
    completedTasks: (state) => state.tasks.filter(task => task.status === 'completed'),
    failedTasks: (state) => state.tasks.filter(task => task.status === 'failed'),
    pendingTasks: (state) => state.tasks.filter(task => task.status === 'pending'),
    
    taskStats: (state) => ({
      total: state.tasks.length,
      running: state.tasks.filter(t => t.status === 'running').length,
      completed: state.tasks.filter(t => t.status === 'completed').length,
      failed: state.tasks.filter(t => t.status === 'failed').length,
      pending: state.tasks.filter(t => t.status === 'pending').length
    })
  },

  actions: {
    // 建立新任務
    async createTask(taskData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/tasks', {
          url: taskData.url,
          target_views: taskData.target_views,
          delay_type: taskData.delay_type,
          simulate_actions: taskData.simulate_actions
        })
        
        // 新增到本地狀態
        this.tasks.unshift(response.data)
        
        return {
          success: true,
          data: response.data,
          message: '任務建立成功'
        }
      } catch (error) {
        this.error = error.message
        return {
          success: false,
          message: error.message
        }
      } finally {
        this.loading = false
      }
    },

    // 獲取所有任務
    async getTasks() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/tasks')
        this.tasks = response.data || []
        
        return {
          success: true,
          data: this.tasks
        }
      } catch (error) {
        this.error = error.message
        return {
          success: false,
          message: error.message,
          data: []
        }
      } finally {
        this.loading = false
      }
    },

    // 獲取單個任務詳情
    async getTask(taskId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get(`/tasks/${taskId}`)
        this.currentTask = response.data
        
        // 更新本地任務列表中的對應項目
        const index = this.tasks.findIndex(task => task.id === taskId)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        
        return {
          success: true,
          data: response.data
        }
      } catch (error) {
        this.error = error.message
        return {
          success: false,
          message: error.message
        }
      } finally {
        this.loading = false
      }
    },

    // 停止任務
    async stopTask(taskId) {
      try {
        const response = await api.post(`/tasks/${taskId}/stop`)
        
        // 更新本地狀態
        const index = this.tasks.findIndex(task => task.id === taskId)
        if (index !== -1) {
          this.tasks[index].status = 'stopped'
        }
        
        return {
          success: true,
          data: response.data,
          message: '任務已停止'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    },

    // 重試任務
    async retryTask(taskId) {
      try {
        const response = await api.post(`/tasks/${taskId}/retry`)
        
        // 更新本地狀態
        const index = this.tasks.findIndex(task => task.id === taskId)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        
        return {
          success: true,
          data: response.data,
          message: '任務已重新開始'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    },

    // 刪除任務
    async deleteTask(taskId) {
      try {
        await api.delete(`/tasks/${taskId}`)
        
        // 從本地狀態中移除
        this.tasks = this.tasks.filter(task => task.id !== taskId)
        
        return {
          success: true,
          message: '任務已刪除'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    },

    // 獲取系統狀態
    async getSystemStatus() {
      try {
        const response = await api.get('/system/status')
        return {
          success: true,
          data: response.data
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    },

    // 清除錯誤狀態
    clearError() {
      this.error = null
    },

    // 重置狀態
    resetStore() {
      this.tasks = []
      this.currentTask = null
      this.loading = false
      this.error = null
    }
  }
})
