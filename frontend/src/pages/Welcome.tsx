
import {
  ArrowRight,
  Brain,
  Heart,
  Sparkles,
  ShieldCheck,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function Welcome() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen overflow-hidden bg-gradient-to-br from-violet-50 via-white to-indigo-50">
      {/* Decorative background */}
      <div className="pointer-events-none absolute -right-32 -top-32 h-80 w-80 rounded-full bg-violet-200/40 blur-3xl" />

      <div className="pointer-events-none absolute -bottom-32 -left-32 h-80 w-80 rounded-full bg-indigo-200/40 blur-3xl" />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-6 sm:px-10">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-600 shadow-lg shadow-violet-200">
            <Brain className="h-6 w-6 text-white" />
          </div>

          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Mood<span className="text-violet-600">Mentor</span>
            </h1>

            <p className="text-[11px] text-slate-400">
              Emotional wellness
            </p>
          </div>
        </div>

        <div className="hidden items-center gap-2 text-sm text-slate-500 sm:flex">
          <ShieldCheck className="h-4 w-4 text-emerald-500" />
          Your space. Your journey.
        </div>
      </header>

      {/* Main */}
      <main className="relative z-10 mx-auto flex min-h-[calc(100vh-100px)] max-w-7xl items-center px-6 py-10 sm:px-10 lg:py-16">
        <div className="grid w-full items-center gap-12 lg:grid-cols-2">
          {/* Left */}
          <div className="max-w-xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-violet-100 bg-white/80 px-4 py-2 text-sm font-medium text-violet-700 shadow-sm backdrop-blur">
              <Sparkles className="h-4 w-4" />
              Your AI-powered wellness companion
            </div>

            <h2 className="text-4xl font-bold leading-tight tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
              Understand your
              <span className="block text-violet-600">
                emotions.
              </span>

              <span className="block">
                Take care of yourself.
              </span>
            </h2>

            <p className="mt-6 max-w-lg text-base leading-7 text-slate-500 sm:text-lg">
              MoodMentor helps you understand how you're feeling,
              discover emotional patterns, and build healthier
              daily habits through AI-powered insights.
            </p>

            <button
              onClick={() => navigate('/login')}
              className="group mt-8 inline-flex items-center gap-3 rounded-2xl bg-violet-600 px-7 py-4 font-semibold text-white shadow-xl shadow-violet-200 transition hover:-translate-y-0.5 hover:bg-violet-700"
            >
              Get Started

              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </button>

            <div className="mt-6 flex items-center gap-2 text-sm text-slate-400">
              <Heart className="h-4 w-4 text-rose-400" />
              A safe space to reflect and understand yourself
            </div>
          </div>

          {/* Right visual */}
          <div className="relative mx-auto w-full max-w-lg">
            <div className="absolute inset-8 rounded-full bg-violet-200/40 blur-3xl" />

            <div className="relative rounded-[2rem] border border-white bg-white/80 p-5 shadow-2xl shadow-violet-100 backdrop-blur-xl sm:p-7">
              {/* Top card */}
              <div className="rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-violet-100">
                      Today's emotional check-in
                    </p>

                    <h3 className="mt-1 text-xl font-bold">
                      How are you feeling?
                    </h3>
                  </div>

                  <div className="text-4xl">
                    🌱
                  </div>
                </div>

                <div className="mt-6 rounded-xl bg-white/10 p-4 backdrop-blur">
                  <p className="text-sm leading-6 text-violet-50">
                    "I've been feeling stressed about my exams,
                    but I'm trying to stay positive."
                  </p>
                </div>
              </div>

              {/* Emotion cards */}
              <div className="mt-5 grid grid-cols-2 gap-3">
                <div className="rounded-2xl bg-emerald-50 p-4">
                  <div className="text-2xl">😌</div>

                  <p className="mt-2 text-xs text-emerald-600">
                    Detected emotion
                  </p>

                  <p className="mt-1 font-semibold text-emerald-900">
                    Calm
                  </p>
                </div>

                <div className="rounded-2xl bg-amber-50 p-4">
                  <div className="text-2xl">🧘</div>

                  <p className="mt-2 text-xs text-amber-600">
                    Recommendation
                  </p>

                  <p className="mt-1 font-semibold text-amber-900">
                    Take a break
                  </p>
                </div>
              </div>

              {/* AI insight */}
              <div className="mt-3 flex items-center gap-3 rounded-2xl border border-violet-100 bg-violet-50 p-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-violet-100">
                  <Sparkles className="h-5 w-5 text-violet-600" />
                </div>

                <div>
                  <p className="text-xs font-medium text-violet-500">
                    MoodMentor insight
                  </p>

                  <p className="mt-1 text-sm font-medium text-violet-900">
                    Small steps can make a big difference.
                  </p>
                </div>
              </div>
            </div>

            {/* Floating badge */}
            <div className="absolute -bottom-5 -left-4 hidden rounded-2xl border border-white bg-white p-4 shadow-xl sm:block">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100">
                  <Heart className="h-5 w-5 text-emerald-600" />
                </div>

                <div>
                  <p className="text-xs text-slate-400">
                    Wellness
                  </p>

                  <p className="font-semibold text-slate-800">
                    One day at a time
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
