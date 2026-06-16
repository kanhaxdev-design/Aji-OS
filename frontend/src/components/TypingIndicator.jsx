import React from 'react'

function TypingIndicator() {
  return (
    <div className="flex justify-start animate-in">
      <div className="glass rounded-lg px-4 py-3">
        <div className="typing-indicator">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      </div>
    </div>
  )
}

export default TypingIndicator
