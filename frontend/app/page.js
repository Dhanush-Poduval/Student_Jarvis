'use client'
import Benefits from '@/LandingPage/Benefits'
import Features from '@/LandingPage/Features'
import Hero from '@/LandingPage/Hero'
import Navbar from '@/LandingPage/Navbar'
import React from 'react'

export default function page() {
  return (
    <div>
      <Navbar/>
      <Hero />
      <Features />
      <Benefits />
    </div>
    
  )
}
