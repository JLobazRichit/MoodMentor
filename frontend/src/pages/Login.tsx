import axios from 'axios'
import { useState } from 'react'
import {
  ArrowRight,
  Brain,
  Eye,
  EyeOff,
  Lock,
  User,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { API_URL } from '../api'

export default function Login() {
  const navigate = useNavigate()

  const [showPassword, setShowPassword] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault()

    setError('')

    if (!username.trim() || !password.trim()) {
      setError('Please enter your username and password.')
      return
    }

    setLoading(true)

    try {
      const response = await axios.post(
        `${API_URL}/api/login`,
        {
          username: username.trim(),
          password: password,
        }
      )

      if (response.data.success) {
        localStorage.setItem(
          'moodmentor_user',
          JSON.stringify(response.data.user)
        );
        navigate('/dashboard')
      } else {
        setError(
          response.data.message || 'Invalid username or password.'
        )
      }
    } catch (error) {
      console.error('Login failed:', error)

      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.detail ||
          'Unable to connect to MoodMentor server.'
        )
      } else {
        setError('Something went wrong. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* Left visual */}
        <div className="relative hidden overflow-hidden bg-gradient-to-br from-violet-700 via-violet-600 to-indigo-700 lg:flex">
          <div className="absolute -right-32 -top-32 h-96 w-96 rounded-full bg-white/10 blur-3xl" />

          <div className="absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-indigo-300/20 blur-3xl" />

          <div className="relative z-10 flex w-full flex-col justify-between p-12 xl:p-16">

            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 backdrop-blur">
                <Brain className="h-6 w-6 text-white" />
              </div>

              <h1 className="text-xl font-bold text-white">
                MoodMentor
              </h1>
            </div>

            <div className="max-w-lg">
              <div className="text-6xl">🧠</div>

              <h2 className="mt-6 text-4xl font-bold leading-tight text-white xl:text-5xl">
                Your feelings
                <span className="block text-violet-200">
                  deserve to be understood.
                </span>
              </h2>

              <p className="mt-6 text-lg leading-8 text-violet-100">
                Reflect on your emotions, discover patterns,
                and build healthier habits with your personal
                AI wellness companion.
              </p>
            </div>

            <p className="text-sm text-violet-200">
              MoodMentor • Emotional wellness companion
            </p>
          </div>
        </div>

        {/* Login */}
        <div className="flex items-center justify-center px-6 py-10 sm:px-10">
          <div className="w-full max-w-md">

            {/* Logo mobile */}
            <div className="mb-10 flex items-center gap-3 lg:hidden">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-600">
                <Brain className="h-6 w-6 text-white" />
              </div>

              <h1 className="text-xl font-bold text-slate-900">
                Mood<span className="text-violet-600">Mentor</span>
              </h1>
            </div>

            <div className="mb-8">
              <h2 className="text-3xl font-bold text-slate-900">
                Welcome back 👋
              </h2>

              <p className="mt-2 text-slate-500">
                Sign in to continue your wellness journey.
              </p>
            </div>

            <form
              onSubmit={handleLogin}
              className="space-y-5"
            >

              {/* Username */}
              <div>
                <label
                  htmlFor="username"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Username
                </label>

                <div className="relative">
                  <User className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />

                  <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(event) =>
                      setUsername(event.target.value)
                    }
                    placeholder="Enter your username"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3.5 pl-12 pr-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-400 focus:ring-4 focus:ring-violet-100"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="text-sm font-medium text-slate-700"
                  >
                    Password
                  </label>

                  <button
                    type="button"
                    className="text-xs font-medium text-violet-600 hover:text-violet-700"
                  >
                    Forgot password?
                  </button>
                </div>

                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />

                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(event) =>
                      setPassword(event.target.value)
                    }
                    placeholder="Enter your password"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3.5 pl-12 pr-12 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-400 focus:ring-4 focus:ring-violet-100"
                  />

                  <button
                    type="button"
                    onClick={() =>
                      setShowPassword(!showPassword)
                    }
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
                  {error}
                </div>
              )}

              {/* Login */}
              <button
                type="submit"
                disabled={loading}
                className="group flex w-full items-center justify-center gap-2 rounded-xl bg-violet-600 py-3.5 font-semibold text-white shadow-lg shadow-violet-100 transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? 'Logging in...' : 'Login'}

                {!loading && (
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-slate-200" />

              <span className="text-xs text-slate-400">
                OR
              </span>

              <div className="h-px flex-1 bg-slate-200" />
            </div>

            {/* Google */}
            <button
              type="button"
              className="flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white py-3.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              <span className="flex h-5 w-5 items-center justify-center rounded-full text-sm font-bold">
                G
              </span>

              Sign in with Google
            </button>

            {/* Register */}
            <p className="mt-8 text-center text-sm text-slate-500">
              Don't have an account?{' '}

              <button
                type="button"
                onClick={() => navigate('/register')}
                className="font-semibold text-violet-600 hover:text-violet-700"
              >
                Create one
              </button>
            </p>

            {/* Back */}
            <button
              type="button"
              onClick={() => navigate('/')}
              className="mx-auto mt-6 block text-xs text-slate-400 hover:text-slate-600"
            >
              ← Back to welcome
            </button>

          </div>
        </div>
      </div>
    </div>
  )
}