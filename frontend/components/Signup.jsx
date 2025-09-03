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
    const [name,setName]=useState("")
    const [email,setEmail]=useState("")
    const [password,setPassword]=useState("")
    const router=useRouter()
    const handleName=(e)=>{
      const text=e.target.value
      setName(text)
      console.log(text)
    }
    const handleEmail=(e)=>{
        const text=e.target.value
        setEmail(text)
        console.log(text)
    }
    const handlePassword=(e)=>{
        const text=e.target.value
        setPassword(text)
        console.log(text)
    }
    const handleSubmit=async(e)=>{
      e.preventDefault()
      try{
        const res=await fetch('http://127.0.0.1:8000/user',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
                "name":name,
                "email":email,
                "password":password
            })})
        const data=await res.json()
        console.log(data)
        router.push('/')
      }catch(error){
        console.log("error",error)
      }
    }
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
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-6">
            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                placeholder="Enter your name"
                required
                onChange={handleName}
                
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                onChange={handleEmail}
                
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
              </div>
              <Input id="password" type="password" required onChange={handlePassword}/>
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
