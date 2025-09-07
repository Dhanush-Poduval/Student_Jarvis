'use client'
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
import Link from "next/link"
import { useRouter } from "next/navigation"

import { useState } from "react"

export function Login() {
    const [email,setEmail]=useState("")
    const [password,setPassword]=useState("")
    const router=useRouter()
    const handlemail=(e)=>{
        const text=e.target.value;
        setEmail(text)
        console.log(text)

    }
    const handlepassword=(e)=>{
        const text=e.target.value
        setPassword(text)
        console.log(text)

    }
    const handlesubmit=async(e)=>{
        e.preventDefault()
      try{
        const res=await fetch("http://127.0.0.1:8000/login",{
            method:"POST",
            headers:{
                'Content-Type':'application/x-www-form-urlencoded'
            },
            body:new URLSearchParams({
                username:email,
                password:password
            })
            
        })
        const data=await res.json()
        console.log("JWT Token",data.access_token)
        localStorage.setItem("token",data.access_token)
        
        router.push("/dashboard")
        
        
        
      }catch(error){
        console.log("error",error)
        alert("INvalid Credentials")

      }
    }
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
        <CardAction>
            <Link href="/signup">
               <Button variant="/signup">Sign Up</Button>
            </Link>
          
        </CardAction>
      </CardHeader>
      <CardContent>
        <form onSubmit={handlesubmit}>
          <div className="flex flex-col gap-6">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                onChange={handlemail}
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
              </div>
              <Input id="password" type="password" required onChange={handlepassword}/>
            </div>
          </div>
          <div className="flex-col gap-2">
            <Button type="submit" className="w-full">
                Login
            </Button>
            
          </div>
       
        </form>
      </CardContent>
    </Card>
  )
}
