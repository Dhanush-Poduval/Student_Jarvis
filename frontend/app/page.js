"use client"
import Link from "next/link"
import { BookOpen, Brain, FileAudio, Sparkles } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-gray-900 via-gray-950 to-black text-gray-100">
      <nav className="w-full flex justify-between items-center px-8 py-4">
        <h1 className="text-2xl font-bold text-purple-400">Student Jarvis</h1>
        <Link
          href="/login"
          className="px-5 py-2 rounded-xl bg-purple-600 text-white font-medium shadow hover:bg-purple-700 transition"
        >
          Login
        </Link>
      </nav>
      <section className="flex flex-col items-center justify-center flex-1 px-6 text-center space-y-6">
        <h2 className="text-5xl font-extrabold tracking-tight">
          Learn <span className="text-purple-400">Smarter</span>, Not Harder
        </h2>
        <p className="text-lg text-gray-400 max-w-2xl">
          Upload your notes, textbooks, or slides and let AI generate
          summaries, flashcards, and even voice explanations — so you can
          study faster and retain more.
        </p>
        <Link
          href="/signup"
          className="px-6 py-3 rounded-xl bg-purple-600 text-white font-semibold shadow-md hover:bg-purple-700 transition"
        >
          Start Learning
        </Link>
      </section>
      <section className="py-16 px-8 grid gap-8 md:grid-cols-3 max-w-6xl mx-auto">
        <div className="bg-gray-800 rounded-2xl shadow p-6 flex flex-col items-center text-center hover:bg-gray-700 transition">
          <BookOpen className="w-10 h-10 text-purple-400 mb-4" />
          <h3 className="font-semibold text-lg">Smart Summaries</h3>
          <p className="text-gray-400 text-sm mt-2">
            Get concise summaries from your documents to save hours of reading.
          </p>
        </div>
        <div className="bg-gray-800 rounded-2xl shadow p-6 flex flex-col items-center text-center hover:bg-gray-700 transition">
          <Brain className="w-10 h-10 text-purple-400 mb-4" />
          <h3 className="font-semibold text-lg">Flashcards</h3>
          <p className="text-gray-400 text-sm mt-2">
            Turn any text into interactive flashcards for effective revision.
          </p>
        </div>
        <div className="bg-gray-800 rounded-2xl shadow p-6 flex flex-col items-center text-center hover:bg-gray-700 transition">
          <FileAudio className="w-10 h-10 text-purple-400 mb-4" />
          <h3 className="font-semibold text-lg">Voice Learning</h3>
          <p className="text-gray-400 text-sm mt-2">
            Listen to AI-generated audio summaries on the go.
          </p>
        </div>
      </section>
      <footer className="py-6 text-center text-sm text-gray-500">
        Made with <Sparkles className="inline w-4 h-4 text-purple-400" /> at Hackathon 2025
      </footer>
    </div>
  )
}
