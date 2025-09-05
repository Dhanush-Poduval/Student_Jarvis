'use client'
import React, { useEffect, useRef, useState } from 'react'
import { Sidebar,SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarSeparator } from '../ui/sidebar'
import Link from 'next/link'
import { Plus, Text } from 'lucide-react'
import { Input } from '../ui/input'
import { Button } from '../ui/button'

export default function AppSidebar() {
    const [chats,setChats]=useState([]);
    const [titleMenue,setttitleMenue]=useState()
    const [title,setTitle]=useState("");
    const ref=useRef();
    useEffect(()=>{
        async function fecthChats() {
            const  token=localStorage.getItem('token')
            try{
                const res=await fetch('http://127.0.0.1:8000/chat_session',{
                    headers:{
                        Authorization:`Bearer ${token}`
                    }
                })
                const data=await res.json()
                setChats(data)
            }catch(error){
                console.log("Error : ",error)
            }
        }
        fecthChats()
    },[])
    const createChats=async()=>{
       const token =localStorage.getItem("token")
       try{
        const res =await fetch("http://127.0.0.1:8000/chat_session",{
            method:'POST',
            headers:{
                'Content-Type':'application/x-www-form-urlencoded',
                Authorization:`Bearer ${token}`
            },
            body:new URLSearchParams({
                chat_title:title
            })
        })
        const data=await res.json()
        setChats(prev=>[data,...prev])
        setttitleMenue(false)

       }catch(error){
         console.log("Error",error)
       }
    }
  
   
  return (
    <div>
        <Sidebar>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        
                        <div className=''>
                            <div className='flex flex-row gap-3 items-center mt-3'>
                            <Plus/>
                          <span onClick={()=>setttitleMenue(true)}>New Chat</span>

                            </div>
                          
                          <div className='flex flex-col gap-5 items-center justify-start'>
                            {titleMenue?(<div className='flex flex-col gap-4 items-center justify-end'>
                            <Input
                            id="title"
                            placeholder="Enter Chat Title"
                            required
                            onChange={(e)=>{const text=e.target.value
                            setTitle(text)
                            console.log(text)
                            }}
                            /><Button onClick={createChats}>Create Chat</Button>
                            </div>):""}
                          </div>

                        </div>
                         
                       
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarSeparator />
            <SidebarContent className="mt-10">
                <SidebarGroup>
                    <SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu className="mt-10">
                                {chats.length>0?chats.map(chits=>(
                                <SidebarMenuItem  key={chits.number}>
                                    <SidebarMenuButton asChild>
                                    <Link href="/dashboard">
                                    <div className='flex flex-row gap-3 items-center justify-center'>
                                    <Text />
                                    <span>{chits.title}</span>

                                    </div>
                                   
                                    </Link>

                                    </SidebarMenuButton>
                                
                                </SidebarMenuItem>
                                


                            )):(<SidebarMenuItem className="mt-20">
                                <span className='font-bold text-center text-3xl'>No chats created yet!!</span>
                            </SidebarMenuItem>)}
                            </SidebarMenu>
                        </SidebarGroupContent>
                    </SidebarGroupLabel>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    </div>
  )
}
