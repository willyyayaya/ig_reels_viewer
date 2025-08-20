import axios from 'axios'

// 建立axios實例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    console.log('API請求:', config.method.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('請求錯誤:', error)
    return Promise.reject(error)
  }
)

// 回應攔截器
api.interceptors.response.use(
  (response) => {
    console.log('API回應:', response.status, response.config.url, response.data)
    return response
  },
  (error) => {
    console.error('回應錯誤:', error.response?.status, error.response?.data || error.message)
    
    // 統一錯誤處理
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.error || 
                        error.message || 
                        '未知錯誤'
    
    return Promise.reject(new Error(errorMessage))
  }
)

/**
 * 任務API服務
 */
const taskApi = {
  /**
   * 建立新任務
   * @param {Object} taskData - 任務資料 { reelsUrl, viewCount }
   */
  createTask(taskData) {
    return api.post('/tasks', taskData)
  },

  /**
   * 取得所有任務
   */
  getAllTasks() {
    return api.get('/tasks')
  },

  /**
   * 取得最近任務
   * @param {number} limit - 限制筆數
   */
  getRecentTasks(limit = 10) {
    return api.get('/tasks/recent', { params: { limit } })
  },

  /**
   * 取得特定任務
   * @param {number} taskId - 任務ID
   */
  getTask(taskId) {
    return api.get(`/tasks/${taskId}`)
  },

  /**
   * 根據狀態取得任務
   * @param {string} status - 任務狀態
   */
  getTasksByStatus(status) {
    return api.get(`/tasks/status/${status}`)
  },

  /**
   * 取消任務
   * @param {number} taskId - 任務ID
   */
  cancelTask(taskId) {
    return api.put(`/tasks/${taskId}/cancel`)
  },

  /**
   * 刪除任務
   * @param {number} taskId - 任務ID
   */
  deleteTask(taskId) {
    return api.delete(`/tasks/${taskId}`)
  },

  /**
   * 取得統計資訊
   */
  getStatistics() {
    return api.get('/tasks/statistics')
  },

  /**
   * 取得執行中任務數量
   */
  getRunningTaskCount() {
    return api.get('/tasks/running/count')
  }
}

export default taskApi
