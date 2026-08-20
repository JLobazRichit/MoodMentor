import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  BarChart3,
  Brain,
  Heart,
  BookOpen,
} from 'lucide-react'
import { API_URL } from '../api'

import Sidebar from '../components/Sidebar'
import MoodChart from '../components/MoodChart'
import StatCard from '../components/StatCard'

interface AnalyticsData {
  total_entries: number
  average_mood: number
  current_mood: string
  weekly_mood: {
    date: string
    mood: number
    emotion: string
  }[]
  emotion_distribution: {
    emotion: string
    percentage: number
    count: number
  }[]
}

export default function Analytics() {

  const user = JSON.parse(
    localStorage.getItem('moodmentor_user') || '{}'
  )

  const [data, setData] = useState<AnalyticsData | null>(null)

  useEffect(() => {

    if (!user.id) return

    axios
      .get(
        `${API_URL}/api/analytics/${user.id}`
      )
      .then((response) => {
        setData(response.data)
      })
      .catch((error) => {
        console.error(error)
      })

  }, [])

  return (
    <div className="flex min-h-screen bg-slate-50">

      <Sidebar />

      <div className="min-w-0 flex-1">

        

        <main className="p-5 sm:p-8">

          <div className="mb-8">

            <h1 className="text-3xl font-bold text-slate-900">
              Analytics
            </h1>

            <p className="mt-2 text-slate-500">
              Understand your emotional patterns over time.
            </p>

          </div>

          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

            <StatCard
              title="Average Mood"
              value={`${data?.average_mood ?? 0}%`}
              description="Your overall mood score"
              icon={Heart}
              iconBg="bg-emerald-50"
              iconColor="text-emerald-600"
            />

            <StatCard
              title="Current Emotion"
              value={data?.current_mood ?? 'No data'}
              description="Latest detected emotion"
              icon={Brain}
              iconBg="bg-violet-50"
              iconColor="text-violet-600"
            />

            <StatCard
              title="Mood Check-ins"
              value={`${data?.total_entries ?? 0}`}
              description="Total mood analyses"
              icon={BookOpen}
              iconBg="bg-blue-50"
              iconColor="text-blue-600"
            />

            <StatCard
              title="Tracking"
              value={data?.total_entries ? 'Active' : 'Start'}
              description="Keep checking in regularly"
              icon={BarChart3}
              iconBg="bg-amber-50"
              iconColor="text-amber-600"
            />

          </section>

          <section className="mt-6 grid gap-6 lg:grid-cols-2">

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <h2 className="font-semibold text-slate-900">
                Mood Trend
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Your recent mood scores
              </p>

              <div className="mt-5">
                <MoodChart
                  data={data?.weekly_mood || []}
                />
              </div>

            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

              <h2 className="font-semibold text-slate-900">
                Emotion Distribution
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                How your emotions have been distributed
              </p>

              <div className="mt-6 space-y-5">

                {data?.emotion_distribution.map((item) => (

                  <div key={item.emotion}>

                    <div className="mb-2 flex justify-between text-sm">

                      <span className="font-medium capitalize text-slate-700">
                        {item.emotion}
                      </span>

                      <span className="text-slate-400">
                        {item.percentage}%
                      </span>

                    </div>

                    <div className="h-2 overflow-hidden rounded-full bg-slate-100">

                      <div
                        className="h-full rounded-full bg-violet-500"
                        style={{
                          width: `${item.percentage}%`
                        }}
                      />

                    </div>

                  </div>

                ))}

              </div>

            </div>

          </section>

        </main>

      </div>

    </div>
  )
}