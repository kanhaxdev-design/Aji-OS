import React from 'react'
import { Copy, Check } from 'lucide-react'
import { useState } from 'react'

function MessageBubble({ role, content }) {
  const [copied, setCopied] = useState(false)

  const isUser = role === 'user'

  const handleCopy = () => {
    navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-in`}>
      <div
        className={`max-w-xs md:max-w-md lg:max-w-xl rounded-lg px-4 py-3 group ${
          isUser
            ? 'bg-gradient-to-r from-aji-accent/30 to-cyan-600/30 text-white'
            : 'glass text-gray-100'
        }`}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 text-sm leading-relaxed">
            {content.split('\n').map((line, idx) => (
              <div key={idx}>{line || <br />}</div>
            ))}
          </div>
          {!isUser && (
            <button
              onClick={handleCopy}
              className="opacity-0 group-hover:opacity-100 transition p-1 hover:bg-white/10 rounded"
            >
              {copied ? (
                <Check size={16} className="text-green-400" />
              ) : (
                <Copy size={16} className="text-gray-400" />
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
