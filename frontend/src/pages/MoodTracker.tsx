import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  ArrowLeft,
  Brain,
  Heart,
  Sparkles,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { API_URL } from '../api'

export default function MoodTracker() {
  const navigate = useNavigate()

  const [text, setText] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [user, setUser] = useState<{ id: number } | null>(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('moodmentor_user')
    if (!storedUser) {
      navigate('/login')
      return
    }
    setUser(JSON.parse(storedUser))
  }, [navigate])

  const [result, setResult] = useState<{
    emotion: string
    emotion_score: number
    sentiment: string
    sentiment_score: number
    recommendation: {
  empathetic_response: string
  recommendations: string[]
  wellness_activity: {
    title: string
    duration: string
    description: string
  }
  
}
    all_emotions: {
      label: string
      score: number
    }[]
  } | null>(null)
  const handleAnalyze = async () => {
    if (!text.trim()) {
      alert('Please tell me how you are feeling.')
      return
    }

    if (!user) {
      navigate('/login')
      return
    }

    setAnalyzing(true)
    setResult(null)

    try {
      const response = await axios.post(
        `${API_URL}/api/analyze`,
        {
          text: text,
          user_id: user.id,
        }
      )

      setResult({
        emotion: response.data.emotion,
        emotion_score: response.data.emotion_score,
        sentiment: response.data.sentiment,
        sentiment_score: response.data.sentiment_score,
        recommendation: response.data.recommendation,
        all_emotions: response.data.all_emotions,
      })
    } catch (error) {
      console.error('Mood analysis failed:', error)

      alert(
        'Unable to analyze your mood. Please make sure the MoodMentor backend is running.'
      )
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">

      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">

          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-violet-600"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </button>

          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-600">
              <Brain className="h-5 w-5 text-white" />
            </div>

            <span className="font-bold text-slate-900">
              Mood<span className="text-violet-600">Mentor</span>
            </span>
          </div>

        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-4xl px-6 py-10">

        {/* Title */}
        <div className="text-center">

          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-100">
            <Heart className="h-7 w-7 text-violet-600" />
          </div>

          <h1 className="mt-5 text-3xl font-bold text-slate-900">
            How are you feeling today?
          </h1>

          <p className="mx-auto mt-3 max-w-xl text-slate-500">
            Tell MoodMentor what's on your mind. Our AI will
            analyze your emotions and provide personalized
            recommendations.
          </p>

        </div>

        {/* Input Card */}
        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-100">
              <Sparkles className="h-5 w-5 text-violet-600" />
            </div>

            <div>
              <h2 className="font-semibold text-slate-900">
                Describe how you're feeling
              </h2>

              <p className="text-xs text-slate-400">
                There are no right or wrong answers.
              </p>
            </div>

          </div>

          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Example: I am feeling stressed because of my exams..."
            rows={7}
            className="mt-6 w-full resize-none rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm leading-7 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-400 focus:bg-white focus:ring-4 focus:ring-violet-100"
          />

          <div className="mt-5 flex items-center justify-between">

            <p className="text-xs text-slate-400">
              {text.length} characters
            </p>

            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="rounded-xl bg-violet-600 px-6 py-3 font-semibold text-white shadow-lg shadow-violet-100 transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {analyzing
                ? 'Analyzing...'
                : '✨ Analyze My Mood'}
            </button>

          </div>
        </div>

        {/* Result */}
        {result && (
          <div className="mt-6 rounded-3xl border border-violet-100 bg-white p-6 shadow-sm sm:p-8">

            {/* Result Header */}
            <div className="flex items-center gap-3">

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50">
                🧠
              </div>

              <div>
                <h2 className="font-semibold text-slate-900">
                  Your Mood Analysis
                </h2>

                <p className="text-xs text-slate-400">
                  Based on your latest check-in
                </p>
              </div>

            </div>


            {/* Analysis Cards */}
            <div className="mt-6 grid gap-4 sm:grid-cols-3">

              {/* Emotion */}
              <div className="rounded-2xl bg-violet-50 p-5">

                <p className="text-xs font-medium text-violet-500">
                  Emotion
                </p>

                <p className="mt-2 text-xl font-bold capitalize text-violet-900">
                  {result.emotion}
                </p>

                <p className="mt-2 text-xs text-violet-500">
                  AI detected emotion
                </p>

              </div>


              {/* Sentiment */}
              <div className="rounded-2xl bg-rose-50 p-5">

                <p className="text-xs font-medium text-rose-500">
                  Sentiment
                </p>

                <p className="mt-2 text-xl font-bold text-rose-900">
                  {result.sentiment}
                </p>

                <p className="mt-2 text-xs text-rose-500">
                  {result.sentiment_score.toFixed(1)}% confidence
                </p>

              </div>


              {/* Emotion Confidence */}
              <div className="rounded-2xl bg-emerald-50 p-5">

                <p className="text-xs font-medium text-emerald-500">
                  Emotion Confidence
                </p>

                <p className="mt-2 text-xl font-bold text-emerald-900">
                  {result.emotion_score.toFixed(1)}%
                </p>

                <p className="mt-2 text-xs text-emerald-600">
                  AI prediction confidence
                </p>

              </div>

            </div>


            {/* Recommendation */}
            <div className="mt-5 rounded-2xl bg-amber-50 p-5">

              <h3 className="font-semibold text-amber-900">
                Recommended for you
              </h3>

              <div className="mt-5 rounded-2xl border border-amber-100 bg-amber-50 p-6">

  <div className="flex items-center gap-3">
    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-100">
      💡
    </div>

    <div>
      <h3 className="font-semibold text-amber-900">
        Recommended for you
      </h3>

      <p className="text-xs text-amber-600">
        Personalized by MoodMentor AI
      </p>
    </div>
  </div>

  {/* Empathetic Response */}
  <div className="mt-5 rounded-xl bg-white p-4">
    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
      Understanding how you feel
    </p>

    <p className="mt-2 text-sm leading-6 text-slate-700">
      {result.recommendation.empathetic_response}
    </p>
  </div>

  {/* Recommendations */}
  <div className="mt-5">
    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
      Personalized recommendations
    </p>

    <div className="mt-3 space-y-3">
      {result.recommendation.recommendations.map(
        (item: string, index: number) => (
          <div
            key={index}
            className="flex gap-3 rounded-xl bg-white p-4"
          >
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-violet-100 text-xs font-bold text-violet-600">
              {index + 1}
            </div>

            <p className="text-sm leading-6 text-slate-700">
              {item}
            </p>
          </div>
        )
      )}
    </div>
  </div>

  {/* Wellness Activity */}
  <div className="mt-5 rounded-xl bg-emerald-50 p-5">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-emerald-600">
          Suggested wellness activity
        </p>

        <h4 className="mt-1 font-semibold text-emerald-900">
          {result.recommendation.wellness_activity.title}
        </h4>
      </div>

      <span className="rounded-full bg-white px-3 py-1 text-xs font-medium text-emerald-700">
        {result.recommendation.wellness_activity.duration}
      </span>
    </div>

    <p className="mt-3 text-sm leading-6 text-emerald-800">
      {result.recommendation.wellness_activity.description}
    </p>
  </div>

</div>

              

              

            </div>


            {/* Emotion Analysis */}
            <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5">

              <h3 className="font-semibold text-slate-900">
                Emotion Analysis
              </h3>

              <p className="mt-1 text-sm text-slate-400">
                AI confidence for each detected emotion
              </p>

              <div className="mt-5 space-y-4">

                {result.all_emotions.map((emotion) => (

                  <div key={emotion.label}>

                    <div className="mb-2 flex items-center justify-between">

                      <span className="text-sm font-medium capitalize text-slate-700">
                        {emotion.label}
                      </span>

                      <span className="text-sm font-semibold text-slate-500">
                        {emotion.score.toFixed(1)}%
                      </span>

                    </div>

                    <div className="h-2 overflow-hidden rounded-full bg-slate-100">

                      <div
                        className="h-full rounded-full bg-violet-500 transition-all duration-700"
                        style={{
                          width: `${emotion.score}%`,
                        }}
                      />

                    </div>

                  </div>

                ))}

              </div>

            </div>

          </div>
        )}

      </main>

    </div>
  )
}