import { useState } from 'react'
import axios from 'axios'
import {
  Bot,
  Send,
  Sparkles,
  User,
} from 'lucide-react'
import { API_URL } from '../api'

import Sidebar from '../components/Sidebar'

interface Message {
  role: 'user' | 'assistant'
  text: string
}

export default function Companion() {

  const user = JSON.parse(
    localStorage.getItem('moodmentor_user') || '{}'
  )

  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      text: "Hi! I'm your MoodMentor companion. You can talk to me about how you're feeling, what's happening in your life, or anything that's on your mind."
    }
  ])

  const sendMessage = async () => {

    if (!message.trim() || loading) return

    const userMessage = message

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        text: userMessage
      }
    ])

    setMessage('')
    setLoading(true)

    try {

      const response = await axios.post(
        `${API_URL}/api/companion`,
        {
          user_id: user.id,
          message: userMessage
        }
      )

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: response.data.reply
        }
      ])

    } catch (error) {

      console.error(error)

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: "I'm having trouble connecting right now. Please try again."
        }
      ])

    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-50">

      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">

      

        <main className="flex flex-1 flex-col p-5 sm:p-8">

          <div className="mb-6">

            <div className="flex items-center gap-3">

              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-100">
                <Sparkles className="h-6 w-6 text-violet-600" />
              </div>

              <div>
                <h1 className="text-3xl font-bold text-slate-900">
                  AI Companion
                </h1>

                <p className="mt-1 text-slate-500">
                  A safe space to talk, reflect and understand yourself.
                </p>
              </div>

            </div>

          </div>

          <div className="flex min-h-[600px] flex-1 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

            <div className="flex-1 space-y-5 overflow-y-auto p-5">

              {messages.map((item, index) => (

                <div
                  key={index}
                  className={`flex gap-3 ${
                    item.role === 'user'
                      ? 'justify-end'
                      : 'justify-start'
                  }`}
                >

                  {item.role === 'assistant' && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-violet-100">
                      <Bot className="h-5 w-5 text-violet-600" />
                    </div>
                  )}

                  <div
                    className={`max-w-xl rounded-2xl px-4 py-3 text-sm leading-7 ${
                      item.role === 'user'
                        ? 'bg-violet-600 text-white'
                        : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {item.text}
                  </div>

                  {item.role === 'user' && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-100">
                      <User className="h-5 w-5 text-slate-500" />
                    </div>
                  )}

                </div>

              ))}

              {loading && (
                <div className="text-sm text-slate-400">
                  MoodMentor is thinking...
                </div>
              )}

            </div>

            <div className="border-t border-slate-200 p-4">

              <div className="flex gap-3">

                <input
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      sendMessage()
                    }
                  }}
                  placeholder="Tell MoodMentor what's on your mind..."
                  className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-400"
                />

                <button
                  onClick={sendMessage}
                  disabled={loading}
                  className="flex items-center justify-center rounded-xl bg-violet-600 px-5 text-white hover:bg-violet-700"
                >
                  <Send className="h-5 w-5" />
                </button>

              </div>

            </div>

          </div>

        </main>

      </div>

    </div>
  )
}