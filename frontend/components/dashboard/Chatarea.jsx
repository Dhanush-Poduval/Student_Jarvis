'use client'
import React, { useState, useRef, useEffect } from 'react'
import { Input } from '../ui/input'
import { Plus } from 'lucide-react'

export default function ChatSection() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hey! Upload a PDF and then ask me anything about it.' }
  ])
  const [flashcards, setFlashcards] = useState([]) 
  const [summaryID, setsummaryID] = useState(null)
  const [plus, setPlus] = useState(false)
  const [fileID, setfileID] = useState()
  const [input, setInput] = useState('')
  const scrollRef = useRef(null)
  const [audio, setAudio] = useState(null)

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

  const tts = async () => {
    const token = localStorage.getItem('token')
    if (audio) {
      audio.pause()
      audio.currentTime = 0
    }
    try {
      const res = await fetch('http://127.0.0.1:8000/tts', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ summary_id: summaryID })
      })
      const data = await res.blob()
      const dataurl = URL.createObjectURL(data)
      const newaudio = new Audio(dataurl)
      setAudio(newaudio)
      newaudio.play()
    } catch (error) {
      console.log("Error : ", error)
    }
  }

  const stopAudio = () => {
    if (audio) {
      audio.pause()
      audio.currentTime = 0
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
      setFlashcards(data.flashcards)
      setsummaryID(data.summary_id)
    } catch (error) {
      console.log("Error : ", error)
    }
  }

  const sendMessage = async () => {
    const text = input.trim()
    if (!text) return
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          ask_question: text,
          document_id: fileID
        })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }])
    } catch (error) {
      console.log("Error : ", error)
      setMessages(prev => [...prev, { role: 'assistant', content: "Oops something went wrong." }])
    }
  }

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-4 py-2 rounded-2xl text-sm max-w-xl leading-relaxed border ${
                msg.role === 'user' ? 'border-gray-300' : 'border-gray-200'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {flashcards.length > 0 && (
          <div className="mt-6 space-y-4">
            {flashcards.map((f, idx) => (
              <div key={idx} className="p-4 rounded-xl border shadow-sm">
                <strong className="block text-base">{f.Point}</strong>
                <p className="mt-1 text-sm ">{f.Answer}</p>
              </div>
            ))}
          </div>
        )}
        <div ref={scrollRef} />
      </div>
      <div className="p-4 border-t flex items-center gap-2">
        <Plus onClick={() => setPlus(!plus)} className="cursor-pointer" />

        {plus && (
          <div className="flex items-center gap-2">
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={pdfReciever}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="px-3 py-2 border rounded-lg text-sm cursor-pointer"
            >
              Upload File
            </label>
            {fileID && (
              <span className="text-xs text-gray-500">PDF uploaded </span>
            )}
          </div>
        )}

        {fileID && (
          <>
            <Input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Type your question..."
              className="flex-1 px-4 py-2 border rounded-lg text-sm"
            />
            <button
              onClick={sendMessage}
              className="px-4 py-2 rounded-lg border text-sm"
            >
              Send
            </button>
          </>
        )}

        <button onClick={summary} className="px-3 py-2 rounded-lg border text-sm">
          Summarize
        </button>
        <button onClick={tts} className="px-3 py-2 rounded-lg border text-sm">
          Voice
        </button>
        <button onClick={stopAudio} className="px-3 py-2 rounded-lg border text-sm">
          Stop
        </button>
      </div>
    </div>
  )
}
