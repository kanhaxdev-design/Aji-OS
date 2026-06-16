import React, { useEffect, useState } from 'react'
import { Trash2, Plus } from 'lucide-react'
import { useStore } from '../store/appStore'
import { chatService } from '../services/api'

function Sidebar({ onNewChat }) {
  const [conversations, setConversations] = useState([])
  const [loading, setLoading] = useState(true)
  const { currentConversation, setCurrentConversation } = useStore()

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const data = await chatService.getConversations()
      setConversations(data.conversations || [])
    } catch (error) {
      console.error('Failed to load conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteConversation = async (id, e) => {
    e.stopPropagation()
    try {
      await chatService.deleteConversation(id)
      setConversations(conversations.filter(c => c.id !== id))
      if (currentConversation === id) {
        onNewChat()
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error)
    }
  }

  const handleSelectConversation = (id) => {
    setCurrentConversation(id)
  }

  return (
    <div className="h-full flex flex-col bg-gradient-to-b from-aji-dark/80 to-aji-darker/80 backdrop-blur-xl">
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg bg-gradient-to-r from-aji-accent/20 to-cyan-600/20 hover:from-aji-accent/30 hover:to-cyan-600/30 text-aji-accent transition"
        >
          <Plus size={18} />
          <span className="font-medium">New Chat</span>
        </button>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {loading ? (
          <div className="text-center text-gray-400 text-sm py-8">Loading...</div>
        ) : conversations.length === 0 ? (
          <div className="text-center text-gray-500 text-sm py-8">
            No conversations yet
          </div>
        ) : (
          conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => handleSelectConversation(conv.id)}
              className={`w-full text-left p-3 rounded-lg transition group ${
                currentConversation === conv.id
                  ? 'bg-aji-accent/20 border border-aji-accent/50'
                  : 'hover:bg-white/10 border border-transparent'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="truncate font-medium text-sm flex-1">
                  {conv.title || 'Untitled'}
                </span>
                <button
                  onClick={(e) => handleDeleteConversation(conv.id, e)}
                  className="p-1 hover:bg-red-500/20 rounded opacity-0 group-hover:opacity-100 transition"
                >
                  <Trash2 size={14} className="text-red-400" />
                </button>
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {new Date(conv.updated_at).toLocaleDateString()}
              </div>
            </button>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-white/10 text-xs text-gray-400">
        <p>Aji OS v1.0</p>
      </div>
    </div>
  )
}

export default Sidebar
