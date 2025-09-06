'use client'
import React, { useState, useRef, useEffect } from 'react'
import { Input } from '../ui/input'
import { Plus } from 'lucide-react'

export default function ChatSection() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hey! Ask me anything about your PDF.' }
  ])
  const [flashcards, setFlashcards] = useState([]) 
  const [summaryID, setsummaryID] = useState(null)
  const [plus, setPlus] = useState(false)
  const [fileID, setfileID] = useState()
  const [input, setInput] = useState('')
  const scrollRef = useRef(null)

  const pdfReciever = async (e) => {
    const token = localStorage.getItem('token')
    const chat_id = localStorage.getItem('chat_session')
    const file = e.target.files[0]
    const formData = new FormData()
    formData.append("file", file)
    formData.append("chat_session", chat_id)
    if (!chat_id) {
      alert("Please select or create a chat")
      return
    }
    try {
      const res = await fetch('http://127.0.0.1:8000/student_pdf', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData
      })
      const data = await res.json()
      setfileID(data.id)
      console.log(data.id)
    } catch (error) {
      console.log("Error : ", error)
    }
  }

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, flashcards])

  async function summary() {
    const token = localStorage.getItem('token')
    if (!fileID) {
      alert("Upload a PDF first")
      return
    }
    try {
      const res = await fetch('http://127.0.0.1:8000/summarize_pdf', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ document_id: fileID })
      })
      const data = await res.json()
      console.log("flashcards:", data.flashcards)
      setFlashcards(data.flashcards) // <-- store flashcards array directly
      setsummaryID(data.summary_id)
    } catch (error) {
      console.log("Error : ", error)
    }
  }

  const sendMessage = () => {
    const text = input.trim()
    if (!text) return
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')
    setTimeout(() => {
      setMessages(prev => [...prev, { role: 'assistant', content: 'This is a placeholder reply.' }])
    }, 500)
  }

  return (
    <div className="flex flex-col">
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

          
          {flashcards.length > 0 && (
            <div className="flex flex-col gap-4 mt-4">
              {flashcards.map((f, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl bg-gradient-to-r from-purple-500 via-pink-500 to-indigo-500 text-white shadow-md"
                >
                  <strong className="text-lg">{f.Point}</strong>
                  <p className="mt-2">{f.Answer}</p>
                </div>
              ))}
            </div>
          )}

          <div ref={scrollRef} />
        </div>

        <div className="flex p-4 border-t gap-2 bottom-20 left-0 w-full items-center">
          <Plus onClick={() => setPlus(!plus)} />
          <div>
            {plus && <Input type="file" accept=".pdf,.docx" onChange={pdfReciever} />}
          </div>
          <Input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg"
          />
          <button onClick={sendMessage} className="px-4 py-2 rounded-lg border">
            Send
          </button>
          <button onClick={summary} className="px-4 py-2 rounded-lg border ">
            Summarize
          </button>
        </div>
      </div>
    </div>
  )
}
