'use client'
import React, { useState, useRef, useEffect } from 'react'

export default function ChatSection() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hey! Ask me anything about your PDF.' }
  ])
  const [input, setInput] = useState('')
  const scrollRef = useRef(null)

  
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = () => {
    const text = input.trim()
    if (!text) return

    
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')

    
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'This is a placeholder reply.' }
      ])
    }, 500)
  }

  return (
    <div className="flex flex-col h-screen">
     
      <div className="flex flex-col h-screen relative">
  <div className="flex-1 p-4 pb-24 overflow-y-auto flex flex-col gap-2">
    {messages.map((msg, idx) => (
      <div
        key={idx}
        className={`max-w-[70%] px-4 py-2 rounded-lg ${
          msg.role === 'user' ? 'self-end' : 'self-start'
        }`}
      >
        {msg.content}
      </div>
    ))}
    <div ref={scrollRef} />
  </div>

  <div className="flex p-4 border-t gap-2 absolute bottom-30 left-0 w-full">
    <input
      type="text"
      value={input}
      onChange={e => setInput(e.target.value)}
      onKeyDown={e => e.key === 'Enter' && sendMessage()}
      placeholder="Type your message..."
      className="flex-1 px-4 py-2 border rounded-lg"
    />
    <button
      onClick={sendMessage}
      className="px-4 py-2 rounded-lg border"
    >
      Send
    </button>
  </div>
</div>

    </div>
  )
}
