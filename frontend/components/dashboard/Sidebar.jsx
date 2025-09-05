'use client'
import React, { useState } from 'react'
import { Sidebar,SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarSeparator } from '../ui/sidebar'
import Link from 'next/link'
import { Plus, Text } from 'lucide-react'
const chats=[
        {number:"1",title:"First Chat",icon:Text},
        {number:"2",title:"First Chat",icon:Text},
        {number:"3",title:"First Chat",icon:Text},
        {number:"4",title:"First Chat",icon:Text},
        {number:"5",title:"First Chat",icon:Text},
       {number:"6",title:"First Chat",icon:Text},
    ]
export default function AppSidebar() {
    const [chat]=useState(true);
   
  return (
    <div>
        <Sidebar>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <Link href={"/dashaboard"}>
                        <div className='flex flex-row gap-3 items-center mt-3'>
                          <Plus/>
                          <span>New Chat</span>

                        </div>
                         
                        </Link>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarSeparator />
            <SidebarContent className="mt-10">
                <SidebarGroup>
                    <SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu className="mt-10">
                                {chat?chats.map(chits=>(
                                <SidebarMenuItem  key={chits.number}>
                                    <SidebarMenuButton asChild>
                                    <Link href="/dashboard">
                                    <div className='flex flex-row gap-3 items-center justify-center'>
                                    <chits.icon />
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
