import React from 'react'
import Link from 'next/link'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem ,DropdownMenuTrigger} from '../ui/dropdown-menu'
import { Button } from '../ui/button'
import { Moon, Sun } from 'lucide-react'

export default function Navbar() {
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
                        <DropdownMenuContent>
                            <DropdownMenuItem>
                                Light
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                Dark
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                System
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenuTrigger>
                </DropdownMenu>
            </div>
        </div>
    </div>
  )
}
