import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  BookOpen,
  Plus,
  Trash2,
  Heart,
} from 'lucide-react'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'

interface JournalEntry {
  id: number
  title: string
  content: string
  mood?: string
  created_at: string
}

export default function Journal() {

  const user = JSON.parse(
    localStorage.getItem('moodmentor_user') || '{}'
  )

  const userId = user.id

  const [journals, setJournals] = useState<JournalEntry[]>([])
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [mood, setMood] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(false)

  const loadJournals = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/journal/${userId}`
      )

      setJournals(response.data.journals)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    if (userId) {
      loadJournals()
    }
  }, [userId])

  const saveJournal = async () => {

    if (!title.trim() || !content.trim()) {
      return
    }

    setLoading(true)

    try {

      await axios.post(
        'http://127.0.0.1:8000/api/journal',
        {
          user_id: userId,
          title,
          content,
          mood
        }
      )

      setTitle('')
      setContent('')
      setMood('')
      setShowForm(false)

      await loadJournals()

    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteJournal = async (id: number) => {

    try {

      await axios.delete(
        `http://127.0.0.1:8000/api/journal/${id}`
      )

      setJournals(
        journals.filter((journal) => journal.id !== id)
      )

    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-50">

      <Sidebar />

      <div className="min-w-0 flex-1">



        <main className="p-5 sm:p-8">

          <div className="mb-8 flex items-center justify-between">

            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Journal
              </h1>

              <p className="mt-2 text-slate-500">
                Write freely. Reflect honestly. Understand yourself.
              </p>
            </div>

            <button
              onClick={() => setShowForm(!showForm)}
              className="flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-3 text-sm font-semibold text-white hover:bg-violet-700"
            >
              <Plus className="h-4 w-4" />
              New Entry
            </button>

          </div>

          {showForm && (
            <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <h2 className="text-lg font-semibold text-slate-900">
                New Journal Entry
              </h2>

              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Give your entry a title..."
                className="mt-5 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-violet-400"
              />

              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write about your thoughts and feelings..."
                rows={7}
                className="mt-4 w-full resize-none rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-violet-400"
              />

              <select
                value={mood}
                onChange={(e) => setMood(e.target.value)}
                className="mt-4 rounded-xl border border-slate-200 px-4 py-3"
              >
                <option value="">How are you feeling?</option>
                <option value="happy">😊 Happy</option>
                <option value="calm">😌 Calm</option>
                <option value="sad">😢 Sad</option>
                <option value="anxious">😟 Anxious</option>
                <option value="angry">😠 Angry</option>
              </select>

              <div className="mt-5 flex gap-3">

                <button
                  onClick={saveJournal}
                  disabled={loading}
                  className="rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white"
                >
                  {loading ? 'Saving...' : 'Save Entry'}
                </button>

                <button
                  onClick={() => setShowForm(false)}
                  className="rounded-xl bg-slate-100 px-5 py-3 text-sm font-semibold text-slate-600"
                >
                  Cancel
                </button>

              </div>

            </div>
          )}

          {journals.length === 0 ? (

            <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center">

              <BookOpen className="mx-auto h-12 w-12 text-violet-400" />

              <h2 className="mt-4 text-xl font-semibold">
                Your journal is empty
              </h2>

              <p className="mt-2 text-slate-500">
                Start writing your first reflection.
              </p>

            </div>

          ) : (

            <div className="grid gap-5 md:grid-cols-2">

              {journals.map((journal) => (

                <div
                  key={journal.id}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                >

                  <div className="flex justify-between">

                    <div>
                      <h2 className="font-semibold text-slate-900">
                        {journal.title}
                      </h2>

                      <p className="mt-1 text-xs text-slate-400">
                        {new Date(
                          journal.created_at
                        ).toLocaleString()}
                      </p>
                    </div>

                    <button
                      onClick={() =>
                        deleteJournal(journal.id)
                      }
                      className="text-slate-400 hover:text-red-500"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>

                  </div>

                  {journal.mood && (
                    <div className="mt-4 inline-flex items-center gap-2 rounded-full bg-violet-50 px-3 py-1 text-xs text-violet-700">
                      <Heart className="h-3 w-3" />
                      {journal.mood}
                    </div>
                  )}

                  <p className="mt-5 whitespace-pre-wrap text-sm leading-7 text-slate-600">
                    {journal.content}
                  </p>

                </div>

              ))}

            </div>

          )}

        </main>

      </div>

    </div>
  )
}