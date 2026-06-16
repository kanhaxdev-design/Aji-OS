import { create } from 'zustand'
import { v4 as uuidv4 } from 'uuid'

const useStore = create((set, get) => ({
  // Conversations
  conversations: [],
  currentConversation: null,
  messages: [],

  // Settings
  currentProvider: 'groq',
  providers: [],
  temperature: 0.7,
  maxTokens: 2048,
  voiceEnabled: true,
  pluginsEnabled: true,

  // System stats
  systemStats: {
    cpu: 0,
    memory: 0,
    battery: 0,
  },

  // UI state
  isLoading: false,
  error: null,

  // Actions
  createConversation: () => {
    const id = uuidv4()
    set((state) => ({
      currentConversation: id,
      messages: [],
    }))
  },

  setCurrentConversation: (conversationId) => {
    set({ currentConversation: conversationId })
  },

  addMessage: (role, content) => {
    set((state) => ({
      messages: [...state.messages, { role, content, id: uuidv4() }],
    }))
  },

  setMessages: (messages) => {
    set({ messages })
  },

  setCurrentProvider: (provider) => {
    set({ currentProvider: provider })
  },

  setProviders: (providers) => {
    set({ providers })
  },

  setSystemStats: (stats) => {
    set({ systemStats: stats })
  },

  setIsLoading: (loading) => {
    set({ isLoading: loading })
  },

  setError: (error) => {
    set({ error })
  },

  updateTemperature: (temp) => {
    set({ temperature: temp })
  },

  updateMaxTokens: (tokens) => {
    set({ maxTokens: tokens })
  },

  toggleVoice: () => {
    set((state) => ({ voiceEnabled: !state.voiceEnabled }))
  },

  togglePlugins: () => {
    set((state) => ({ pluginsEnabled: !state.pluginsEnabled }))
  },
}))

export { useStore }
