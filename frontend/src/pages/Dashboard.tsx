import { useEffect, useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

import {
  BookOpen,
  Brain,
  Heart,
  Sparkles,
} from 'lucide-react'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import StatCard from '../components/StatCard'
import MoodChart from '../components/MoodChart'


interface DashboardData {
  success: boolean

  user: {
    id: number
    username: string
    email: string
  }

  stats: {
    current_mood: string
    mood_score: number
    journal_entries: number
    wellness_streak: number
  }

  weekly_mood: {
    day: string
    date: string
    mood: number
  }[]

  today_suggestion: {
    title: string
    description: string
  }

  emotion_distribution: {
    emotion: string
    percentage: number
  }[]

  recent_journal: {
    id: number
    emoji: string
    title: string
    emotion: string
    time: string | null
  }[]
}


export default function Dashboard() {

  const navigate = useNavigate()

  const [data, setData] = useState<DashboardData | null>(null)

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState('')


  useEffect(() => {

    const loadDashboard = async () => {

      try {

        const storedUser = localStorage.getItem(
          'moodmentor_user'
        )

        if (!storedUser) {
          navigate('/login')
          return
        }

        const user = JSON.parse(storedUser)

        const response = await axios.get(
          `http://127.0.0.1:8000/api/dashboard/${user.id}`
        )

        if (response.data.success) {
          setData(response.data)
        } else {
          setError(
            response.data.message ||
            'Unable to load dashboard.'
          )
        }

      } catch (error) {

        console.error(
          'Dashboard loading failed:',
          error
        )

        setError(
          'Unable to connect to MoodMentor server.'
        )

      } finally {

        setLoading(false)

      }
    }

    loadDashboard()

  }, [navigate])


  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="text-4xl">🧠</div>

          <p className="mt-3 text-sm text-slate-500">
            Loading your wellness dashboard...
          </p>
        </div>
      </div>
    )
  }


  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
        <div className="rounded-2xl border border-red-100 bg-white p-8 text-center shadow-sm">

          <div className="text-4xl">⚠️</div>

          <h2 className="mt-4 text-xl font-bold text-slate-900">
            Something went wrong
          </h2>

          <p className="mt-2 text-sm text-red-500">
            {error}
          </p>

          <button
            onClick={() => window.location.reload()}
            className="mt-5 rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-violet-700"
          >
            Try Again
          </button>

        </div>
      </div>
    )
  }


  if (!data) {
    return null
  }


  return (
    <div className="flex min-h-screen bg-slate-50">

      <Sidebar />

      <div className="min-w-0 flex-1">

        <Topbar user={data.user} />

        <main className="p-5 sm:p-8">

          {/* ================================================= */}
          {/* Welcome */}
          {/* ================================================= */}

          <section className="mb-8">

            <div className="rounded-3xl bg-gradient-to-r from-violet-600 to-indigo-600 p-6 text-white shadow-lg sm:p-8">

              <div className="max-w-2xl">

                <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-xs font-medium backdrop-blur">

                  <Sparkles className="h-3.5 w-3.5" />

                  Your personal wellness companion

                </div>


                <h1 className="text-2xl font-bold sm:text-3xl">

                  How are you feeling today, {data.user.username}? 👋

                </h1>


                <p className="mt-2 max-w-xl text-sm leading-6 text-violet-100 sm:text-base">

                  Take a moment to check in with yourself.
                  Understanding your emotions is the first step
                  toward taking care of them.

                </p>


                <button
                  onClick={() => navigate('/mood')}
                  className="mt-6 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-violet-700 shadow-sm transition hover:bg-violet-50"
                >
                  ✨ Analyze My Mood
                </button>

              </div>

            </div>

          </section>


          {/* ================================================= */}
          {/* Stats */}
          {/* ================================================= */}

          <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

            <StatCard
              title="Current Mood"
              value={data.stats.current_mood}
              description="Based on your latest check-in"
              icon={Heart}
              iconBg="bg-emerald-50"
              iconColor="text-emerald-600"
            />


            <StatCard
              title="Mood Score"
              value={`${data.stats.mood_score}%`}
              description="Latest sentiment score"
              icon={Brain}
              iconBg="bg-violet-50"
              iconColor="text-violet-600"
            />


            <StatCard
              title="Journal Entries"
              value={String(
                data.stats.journal_entries
              )}
              description="Keep expressing your thoughts"
              icon={BookOpen}
              iconBg="bg-blue-50"
              iconColor="text-blue-600"
            />


            <StatCard
              title="Wellness Streak"
              value={`${data.stats.wellness_streak} days`}
              description="Your current daily check-in streak"
              icon={Sparkles}
              iconBg="bg-amber-50"
              iconColor="text-amber-600"
            />

          </section>


          {/* ================================================= */}
          {/* Chart + Suggestion */}
          {/* ================================================= */}

          <section className="grid gap-6 xl:grid-cols-3">

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm xl:col-span-2">

              <div className="mb-5">

                <h2 className="font-semibold text-slate-900">
                  Your Mood This Week
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  Your emotional wellness trend
                </p>

              </div>


              <MoodChart
                data={data.weekly_mood}
              />

            </div>


            {/* Today's Suggestion */}

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <div className="flex items-center gap-3">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50">
                  🌿
                </div>

                <div>

                  <h2 className="font-semibold text-slate-900">
                    Today's Suggestion
                  </h2>

                  <p className="text-xs text-slate-400">
                    Personalized for you
                  </p>

                </div>

              </div>


              <div className="mt-6 rounded-2xl bg-emerald-50 p-5">

                <h3 className="font-semibold text-emerald-900">
                  {data.today_suggestion.title}
                </h3>


                <p className="mt-2 text-sm leading-6 text-emerald-700">
                  {data.today_suggestion.description}
                </p>


                <button
                  onClick={() => navigate('/wellness')}
                  className="mt-5 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700"
                >
                  Start Activity
                </button>

              </div>

            </div>

          </section>


          {/* ================================================= */}
          {/* Bottom */}
          {/* ================================================= */}

          <section className="mt-6 grid gap-6 lg:grid-cols-2">


            {/* Emotion Distribution */}

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <h2 className="font-semibold text-slate-900">
                Emotion Distribution
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Your recent emotional patterns
              </p>


              {data.emotion_distribution.length === 0 ? (

                <p className="mt-6 text-sm text-slate-400">
                  No emotional data available yet.
                </p>

              ) : (

                <div className="mt-6 space-y-5">

                  {data.emotion_distribution.map(
                    (item) => (

                      <EmotionBar
                        key={item.emotion}
                        label={item.emotion}
                        percentage={item.percentage}
                      />

                    )
                  )}

                </div>

              )}

            </div>


            {/* Recent Journal */}

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <div className="flex items-center justify-between">

                <div>

                  <h2 className="font-semibold text-slate-900">
                    Recent Journal
                  </h2>

                  <p className="mt-1 text-sm text-slate-400">
                    Your latest reflections
                  </p>

                </div>


                <button
                  onClick={() => navigate('/journal')}
                  className="text-sm font-medium text-violet-600 hover:text-violet-700"
                >
                  View all
                </button>

              </div>


              {data.recent_journal.length === 0 ? (

                <div className="mt-6 rounded-xl bg-slate-50 p-5 text-center">

                  <p className="text-sm text-slate-400">
                    Your journal is empty.
                  </p>

                  <button
                    onClick={() => navigate('/mood')}
                    className="mt-3 text-sm font-semibold text-violet-600"
                  >
                    Create your first entry
                  </button>

                </div>

              ) : (

                <div className="mt-5 space-y-4">

                  {data.recent_journal.map(
                    (entry) => (

                      <JournalItem
                        key={entry.id}
                        emoji={entry.emoji}
                        title={entry.title}
                        time={formatTime(entry.time)}
                      />

                    )
                  )}

                </div>

              )}

            </div>

          </section>

        </main>

      </div>

    </div>
  )
}


/* ============================================================
   Emotion Bar
============================================================ */

function EmotionBar({
  label,
  percentage,
}: {
  label: string
  percentage: number
}) {

  return (
    <div>

      <div className="mb-2 flex justify-between text-sm">

        <span className="font-medium text-slate-700">
          {label}
        </span>

        <span className="text-slate-400">
          {percentage}%
        </span>

      </div>


      <div className="h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-violet-500"
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  )
}


/* ============================================================
   Journal Item
============================================================ */

function JournalItem({
  emoji,
  title,
  time,
}: {
  emoji: string
  title: string
  time: string
}) {

  return (
    <div className="flex items-center gap-4 rounded-xl border border-slate-100 p-3 transition hover:bg-slate-50">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-50 text-xl">
        {emoji}
      </div>


      <div className="min-w-0">

        <p className="truncate text-sm font-medium text-slate-800">
          {title}
        </p>

        <p className="mt-1 text-xs text-slate-400">
          {time}
        </p>

      </div>

    </div>
  )
}


/* ============================================================
   Time Formatting
============================================================ */

function formatTime(
  time: string | null
) {

  if (!time) {
    return 'Recently'
  }

  const date = new Date(time)

  return date.toLocaleString([], {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}