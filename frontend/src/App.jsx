import React, { useState, useCallback } from 'react'
import { Menu, Settings, Plus, MessageCircle } from 'lucide-react'
import Sidebar from './components/Sidebar'
import ChatInterface from './components/ChatInterface'
import SettingsPanel from './components/SettingsPanel'
import { useStore } from './store/appStore'

function App() {
  const [showSidebar, setShowSidebar] = useState(true)
  const [showSettings, setShowSettings] = useState(false)
  const { currentConversation, createConversation } = useStore()

  const handleNewChat = useCallback(() => {
    createConversation()
    setShowSettings(false)
  }, [createConversation])

  return (
    <div className="flex h-screen bg-gradient-to-br from-aji-dark to-aji-darker">
      {/* Sidebar */}
      {showSidebar && (
        <div className="hidden md:flex md:flex-col md:w-64 md:border-r md:border-white/10 md:backdrop-blur-xl">
          <Sidebar onNewChat={handleNewChat} />
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-white/10 backdrop-blur-xl glass">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="md:hidden p-2 hover:bg-white/10 rounded-lg transition"
            >
              <Menu size={20} className="text-aji-accent" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-aji-accent to-cyan-600 flex items-center justify-center">
                <span className="text-white font-bold text-sm">A</span>
              </div>
              <span className="font-semibold text-lg hidden sm:inline">Aji OS</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleNewChat}
              className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg bg-aji-accent/10 hover:bg-aji-accent/20 text-aji-accent transition"
            >
              <Plus size={18} />
              <span className="text-sm font-medium">New Chat</span>
            </button>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 hover:bg-white/10 rounded-lg transition"
            >
              <Settings size={20} className="text-aji-accent" />
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-hidden">
          {showSettings ? (
            <SettingsPanel />
          ) : (
            <ChatInterface />
          )}
        </div>
      </div>
    </div>
  )
}

export default App
