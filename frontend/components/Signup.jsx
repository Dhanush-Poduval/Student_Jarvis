'use client'
import Link from 'next/link'
import React from 'react'
import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useRouter } from "next/navigation"

import { useState } from "react"

export default function Signup() {
  return (
    <div className='flex items-center justify-center mt-32'>
        <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Sign Up</CardTitle>
        <CardDescription>
          Enter your name , email password to create an account
        </CardDescription>
        <CardAction>
            <Link href="/">
               <Button variant="/">Log in</Button>
            </Link>
          
        </CardAction>
      </CardHeader>
      <CardContent>
        <form>
          <div className="flex flex-col gap-6">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="name"
                placeholder="m@example.com"
                required
                
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
              </div>
              <Input id="password" type="password" required />
            </div>
          </div>
          <div className="flex-col gap-2">
            <Button type="submit" className="w-full">
                Create
            </Button>
            
          </div>
       
        </form>
      </CardContent>
    </Card>
    </div>
  )
}
