import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  Wind,
  Heart,
  Moon,
  Smile,
  CheckCircle,
} from 'lucide-react'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'

const activities = [
  {
    title: 'Deep Breathing',
    description:
      'Slow your breathing and bring your attention back to the present.',
    duration: '5 minutes',
    icon: Wind,
  },
  {
    title: 'Gratitude Practice',
    description:
      'Write down three things you are grateful for today.',
    duration: '10 minutes',
    icon: Heart,
  },
  {
    title: 'Mindful Pause',
    description:
      'Take a quiet moment to notice your thoughts without judging them.',
    duration: '5 minutes',
    icon: Smile,
  },
  {
    title: 'Sleep Wind-down',
    description:
      'Put away distractions and prepare your mind for restful sleep.',
    duration: '15 minutes',
    icon: Moon,
  },
]

export default function Wellness() {

  const user = JSON.parse(
    localStorage.getItem('moodmentor_user') || '{}'
  )

  const [completed, setCompleted] = useState<string[]>([])

  const loadWellness = async () => {

    try {

      const response = await axios.get(
        `http://127.0.0.1:8000/api/wellness/${user.id}`
      )

      setCompleted(
        response.data.activities.map(
          (item: { activity: string }) =>
            item.activity
        )
      )

    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {

    if (user.id) {
      loadWellness()
    }

  }, [])

  const completeActivity = async (
    activity: string
  ) => {

    try {

      await axios.post(
        'http://127.0.0.1:8000/api/wellness',
        {
          user_id: user.id,
          activity
        }
      )

      setCompleted((prev) => [
        ...prev,
        activity
      ])

    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-50">

      <Sidebar />

      <div className="min-w-0 flex-1">

       

        <main className="p-5 sm:p-8">

          <div className="mb-8">

            <h1 className="text-3xl font-bold text-slate-900">
              Wellness
            </h1>

            <p className="mt-2 text-slate-500">
              Small habits can make a meaningful difference.
            </p>

          </div>

          <div className="mb-8 rounded-3xl bg-gradient-to-r from-emerald-500 to-teal-500 p-7 text-white">

            <h2 className="text-2xl font-bold">
              Take care of yourself 🌿
            </h2>

            <p className="mt-2 max-w-xl text-emerald-50">
              Choose an activity that fits how you're feeling
              right now.
            </p>

          </div>

          <div className="grid gap-5 md:grid-cols-2">

            {activities.map((activity) => {

              const Icon = activity.icon

              const isCompleted =
                completed.includes(activity.title)

              return (

                <div
                  key={activity.title}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                >

                  <div className="flex items-start justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50">
                      <Icon className="h-6 w-6 text-emerald-600" />
                    </div>

                    {isCompleted && (
                      <CheckCircle className="h-6 w-6 text-emerald-500" />
                    )}

                  </div>

                  <h2 className="mt-5 text-lg font-semibold text-slate-900">
                    {activity.title}
                  </h2>

                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {activity.description}
                  </p>

                  <div className="mt-4 text-xs font-medium text-slate-400">
                    ⏱ {activity.duration}
                  </div>

                  <button
                    disabled={isCompleted}
                    onClick={() =>
                      completeActivity(
                        activity.title
                      )
                    }
                    className={`mt-5 w-full rounded-xl py-3 text-sm font-semibold ${
                      isCompleted
                        ? 'bg-emerald-50 text-emerald-600'
                        : 'bg-emerald-600 text-white hover:bg-emerald-700'
                    }`}
                  >
                    {isCompleted
                      ? 'Completed ✓'
                      : 'Complete Activity'}
                  </button>

                </div>

              )
            })}

          </div>

        </main>

      </div>

    </div>
  )
}