import React, { useEffect, useRef, useState } from 'react'
import { Send, Mic, Loader } from 'lucide-react'
import { useStore } from '../store/appStore'
import { chatService, voiceService } from '../services/api'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'
import SystemStats from './SystemStats'

function ChatInterface() {
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const messagesEndRef = useRef(null)
  const { messages, addMessage, currentConversation, isLoading, setIsLoading } = useStore()

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input
    setInput('')
    addMessage('user', userMessage)
    setIsLoading(true)

    try {
      let response = ''
      const stream = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: currentConversation,
        }),
      })

      const reader = stream.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        response = buffer
      }

      addMessage('assistant', response)
    } catch (error) {
      console.error('Failed to send message:', error)
      addMessage('assistant', 'Sorry, I encountered an error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleVoiceInput = async () => {
    try {
      setIsRecording(true)
      const data = await voiceService.recognizeSpeech()
      if (data.text) {
        setInput(data.text)
      }
    } catch (error) {
      console.error('Voice recognition failed:', error)
    } finally {
      setIsRecording(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-aji-accent/20 to-cyan-600/20 flex items-center justify-center mb-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-aji-accent to-cyan-600"></div>
            </div>
            <h2 className="text-2xl font-bold mb-2">Welcome to Aji OS</h2>
            <p className="text-gray-400 max-w-md mb-8">
              Your intelligent desktop assistant. Start a conversation or use commands to control your computer.
            </p>
            <div className="grid grid-cols-2 gap-3 w-full max-w-md">
              <SystemStats />
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-white/10 backdrop-blur-xl glass p-4">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything... (Shift+Enter for new line)"
            className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 resize-none focus:outline-none focus:border-aji-accent transition"
            rows="1"
            style={{
              maxHeight: '120px',
              overflowY: input.split('\n').length > 3 ? 'auto' : 'hidden',
            }}
          />
          <button
            onClick={handleVoiceInput}
            disabled={isRecording}
            className={`p-3 rounded-lg transition ${
              isRecording
                ? 'bg-red-500/20 text-red-400'
                : 'bg-white/5 hover:bg-white/10 text-aji-accent'
            }`}
          >
            {isRecording ? (
              <Loader size={20} className="animate-spin" />
            ) : (
              <Mic size={20} />
            )}
          </button>
          <button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            className="px-4 py-3 rounded-lg bg-gradient-to-r from-aji-accent to-cyan-600 hover:from-aji-accent-dark hover:to-cyan-700 text-white font-medium transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? (
              <Loader size={20} className="animate-spin" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
