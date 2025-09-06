'use client'
import React, { useEffect, useState } from 'react'
import { Sidebar, SidebarContent, SidebarHeader, SidebarMenu, SidebarMenuItem, SidebarSeparator } from '../ui/sidebar'
import Link from 'next/link'
import { Plus, Text } from 'lucide-react'
import { Input } from '../ui/input'
import { Button } from '../ui/button'
import { ScrollArea } from '../ui/scroll-area'

export default function AppSidebar() {
  const [chats, setChats] = useState([]);
  const [titleMenu, setTitleMenu] = useState(false);
  const [title, setTitle] = useState("");

  useEffect(() => {
    async function fetchChats() {
      const token = localStorage.getItem('token');
      try {
        const res = await fetch('http://127.0.0.1:8000/chat_session', {
          headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        setChats(data);
      } catch (error) {
        console.log("Error:", error);
      }
    }
    fetchChats();
  }, []);

  const createChats = async () => {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch("http://127.0.0.1:8000/chat_session", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Authorization: `Bearer ${token}`
        },
        body: new URLSearchParams({ chat_title: title })
      });
      const data = await res.json();
      setChats(prev => [data, ...(Array.isArray(prev) ? prev : [])]);
      setTitleMenu(false);
      localStorage.setItem('chat_session', data.id)
      
    } catch (error) {
      console.log("Error", error);
    }
  }

  return (
    <div className="">
      <Sidebar className="flex flex-col h-full mt-0">
        
        {/* Header + New Chat */}
        <SidebarHeader className="p-4 border-b ">
          <SidebarMenu>
            <SidebarMenuItem>
              <div className="flex flex-col gap-2">
                <button
                  className="flex items-center gap-2 px-2 py-1 rounded w-full"
                  onClick={() => setTitleMenu(!titleMenu)}
                >
                  <Plus size={16} />
                  New Chat
                </button>

                {titleMenu && (
                  <div className="flex flex-col gap-2 mt-2">
                    <Input
                      placeholder="Enter chat title"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                    />
                    <Button onClick={createChats}>Create</Button>
                  </div>
                )}
              </div>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarHeader>

        <SidebarSeparator />

        {/* Scrollable Chat List */}
        <ScrollArea className="flex-1">
          <SidebarContent className="flex flex-col gap-1 p-2">
            <SidebarMenu>
              {chats.length > 0 ? (
                chats.map(chat => (
                  <SidebarMenuItem key={chat.id || chat.number}>
                    <Link href={`/dashboard/${chat.id}`} onClick={()=>localStorage.setItem("chat_session",chat.id)}>
                      <div className="flex items-center gap-2 p-2 rounded cursor-pointer">
                        <Text size={16} />
                        <span className="truncate">{chat.title}</span>
                      </div>
                    </Link>
                  </SidebarMenuItem>
                ))
              ) : (
                <div className="text-center mt-4">No chats created yet!</div>
              )}
            </SidebarMenu>
          </SidebarContent>
        </ScrollArea>

      </Sidebar>
    </div>
  )
}
