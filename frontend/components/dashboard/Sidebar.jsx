'use client'
import React, { useState } from 'react'
import { Sidebar,SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarSeparator } from '../ui/sidebar'
import Link from 'next/link'
import { Plus, Text } from 'lucide-react'
const chats=[
        {number:"1",title:"First Chat",icon:Text},
        {number:"1",title:"First Chat",icon:Text},
        {number:"1",title:"First Chat",icon:Text},
        {number:"1",title:"First Chat",icon:Text},
        {number:"1",title:"First Chat",icon:Text},
       {number:"1",title:"First Chat",icon:Text},
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
                          < Plus/>
                          <span>New Chat</span>
                        </Link>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarSeparator />
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu>
                                {chat?chats.map(chits=>(
                                <SidebarMenuItem key={chits.number}>
                                    <SidebarMenuButton>
                                    <Link href="/dashboard">
                                    <chits.icon />
                                    <span>{chits.title}</span>
                                    </Link>

                                    </SidebarMenuButton>
                                
                                </SidebarMenuItem>
                                


                            )):(<SidebarMenuItem>
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
