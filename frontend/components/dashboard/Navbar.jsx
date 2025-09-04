'use client'
import React from 'react'
import Link from 'next/link'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem ,DropdownMenuTrigger,DropdownMenuSeparator} from '../ui/dropdown-menu'
import { Button } from '../ui/button'
import { Moon, Sun, User ,Settings,LogOut} from 'lucide-react'
import { useTheme } from 'next-themes'

export default function Navbar() {
    const {setTheme}=useTheme()
  return (
    <div className='w-full px-4 py-2 border-b ml-0'>
        <div className='w-full mx-auto flex justify-between items-center ml-5 px-0 py-0'>
            <p>Content collapse</p>
            <div className='flex flex-row items-center justify-end gap-3 mr-5'>
                <Link href="/">Home</Link>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" size="icon">
                            <Sun className="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
                            <Moon className="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" />
                            <span className='sr-only'>Theme</span>
                        </Button>
                    </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <DropdownMenuItem onClick={()=>setTheme("light")}>
                                Light
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={()=>setTheme("dark")}>
                                Dark
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={()=>
                                setTheme("system")
                            }>
                                System
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                   
                </DropdownMenu>
                 <DropdownMenu>
                     <DropdownMenuTrigger asChild>
                        <Button>
                            <User />
                        </Button>
                        
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem>
                            <User className='mr-2'/> Profile
                        </DropdownMenuItem>
                      <DropdownMenuSeparator />
                        <DropdownMenuItem><Settings className="mr-2" /> Settings</DropdownMenuItem>
                        <DropdownMenuItem><LogOut className="mr-2" /> Logout</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
                
            </div>
        </div>
    </div>
  )
}
