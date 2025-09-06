'use client'
import React, { useState, useRef, useEffect } from 'react'
import { Input } from '../ui/input'
import { Plus } from 'lucide-react'

export default function ChatSection() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hey! Ask me anything about your PDF.' }
  ])
  const[summarize,setSummarize]=useState("")
  const [summaryID,setsummaryID]=useState(null)
  const[plus,setPlus]=useState(false)
  const [fileID,setfileID]=useState()
  const [input, setInput] = useState('')
  const scrollRef = useRef(null)
  const pdfReciever=async(e)=>{
    const token =localStorage.getItem('token')
    const chat_id=localStorage.getItem('chat_session')
    const file=e.target.files[0];
    const formData=new FormData()
    formData.append("file",file)
    formData.append("chat_session",chat_id)
    console.log(chat_id)
    if (!chat_id){
        alert("Please select or create a chat")
    }
    try{
       const res=await fetch('http://127.0.0.1:8000/student_pdf',{
        method:'POST',
        headers:{
            Authorization:`Bearer ${token}`
        },
        body: formData 
       })
       const data=await res.json()
       setfileID(data.id)
       console.log(data.id)

    }catch(error){
        console.log("Error : ",error)
    }
  }
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  async function summary() {
    const token=localStorage.getItem('token')
    console.log(fileID)
    try{
      const res=await fetch('http://127.0.0.1:8000/summarize_pdf',{
        method:'POST',
        headers:{
          Authorization:`Bearer ${token}`,
          'Content-Type':'application/x-www-form-urlencoded'
        },
        body:new URLSearchParams({
         document_id:fileID
        
        })
      })
      
      const data=await res.json()
      console.log("Uploade the document :",data)
      console.log("flashcards:",data.flashcards)
      setSummarize(data.flashcards.map(f=>`${f.Point}:${f.Answer}`).join("\n"))
      setsummaryID(data.summary_id)
    }catch(error){
      console.log("Error : ",error)
    }
  }

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
    {summarize?( <div className="p-4  rounded-lg whitespace-pre-wrap">
            <strong>📌 Summary:</strong>
            <br />
            {summarize}
          </div>) :""}
    <div ref={scrollRef} />
  </div>

  <div className="flex p-4 border-t gap-2 absolute bottom-20 left-0 w-full items-center">
    <Plus onClick={()=>setPlus(!plus)}/>
    <div>
        {plus?(<Input type="file" accept=".pdf,.docx" onChange={pdfReciever}/>):''}
    </div>
    <Input
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
    <button  onClick={summary} className="px-4 py-2 rounded-lg border bg-green-200">
      Summarize
    </button>
  </div>
</div>

    </div>
  )
}
