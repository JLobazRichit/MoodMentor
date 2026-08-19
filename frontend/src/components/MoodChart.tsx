import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

interface MoodChartProps {
  data?: {
    date: string
    mood: number
    emotion?: string
  }[]
}

export default function MoodChart({
  data = []
}: MoodChartProps) {

  return (
    <div className="h-72 w-full">

      <ResponsiveContainer width="100%" height="100%">

        <AreaChart data={data}>

          <defs>

            <linearGradient
              id="moodGradient"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >

              <stop
                offset="0%"
                stopColor="#8b5cf6"
                stopOpacity={0.25}
              />

              <stop
                offset="100%"
                stopColor="#8b5cf6"
                stopOpacity={0}
              />

            </linearGradient>

          </defs>

          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
            stroke="#e2e8f0"
          />

          <XAxis
            dataKey="date"
            axisLine={false}
            tickLine={false}
            tick={{
              fill: '#94a3b8',
              fontSize: 12
            }}
          />

          <YAxis
            domain={[0, 100]}
            axisLine={false}
            tickLine={false}
            tick={{
              fill: '#94a3b8',
              fontSize: 12
            }}
          />

          <Tooltip />

          <Area
            type="monotone"
            dataKey="mood"
            stroke="#8b5cf6"
            strokeWidth={3}
            fill="url(#moodGradient)"
          />

        </AreaChart>

      </ResponsiveContainer>

    </div>
  )
}