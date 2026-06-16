import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat endpoints
export const chatService = {
  async sendMessage(message, conversationId = null) {
    try {
      const response = await api.post('/api/chat', {
        message,
        conversation_id: conversationId,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async sendMessageSync(message, conversationId = null) {
    try {
      const response = await api.post('/api/chat-sync', {
        message,
        conversation_id: conversationId,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getConversations(limit = 50) {
    try {
      const response = await api.get('/api/conversations', {
        params: { limit },
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getConversation(conversationId) {
    try {
      const response = await api.get(`/api/conversation/${conversationId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteConversation(conversationId) {
    try {
      const response = await api.delete(`/api/conversation/${conversationId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async clearHistory() {
    try {
      const response = await api.post('/api/clear-history')
      return response.data
    } catch (error) {
      throw error
    }
  },
}

// Command endpoints
export const commandService = {
  async executeCommand(command, args = {}) {
    try {
      const response = await api.post('/api/command', {
        command,
        args,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getCommands() {
    try {
      const response = await api.get('/api/commands')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getPluginInfo(pluginName) {
    try {
      const response = await api.get(`/api/plugin/${pluginName}`)
      return response.data
    } catch (error) {
      throw error
    }
  },
}

// Voice endpoints
export const voiceService = {
  async recognizeSpeech() {
    try {
      const response = await api.post('/api/voice/recognize')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async synthesizeSpeech(text) {
    try {
      const response = await api.post('/api/voice/synthesize', {
        text,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },
}

// System endpoints
export const systemService = {
  async getStats() {
    try {
      const response = await api.get('/stats')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getSettings() {
    try {
      const response = await api.get('/api/settings')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateSetting(key, value) {
    try {
      const response = await api.post('/api/settings', {
        key,
        value,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getProviders() {
    try {
      const response = await api.get('/api/providers')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async switchProvider(provider) {
    try {
      const response = await api.post('/api/provider', {
        provider,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },
}

export default api
