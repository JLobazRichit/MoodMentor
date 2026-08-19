import {
  BarChart3,
  BookOpen,
  Brain,
  Home,
  LogOut,
  Settings,
  Sparkles,
  Wind,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

const menuItems = [
  {
    icon: Home,
    label: 'Dashboard',
    path: '/dashboard',
  },
  {
    icon: Brain,
    label: 'Mood Tracker',
    path: '/mood',
  },
  {
    icon: BookOpen,
    label: 'Journal',
    path: '/journal',
  },
  {
    icon: Sparkles,
    label: 'AI Companion',
    path: '/companion',
  },
  {
    icon: BarChart3,
    label: 'Analytics',
    path: '/analytics',
  },
  {
    icon: Wind,
    label: 'Wellness',
    path: '/wellness',
  },
]

export default function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      {/* Logo */}
      <div className="flex h-20 items-center gap-3 border-b border-slate-100 px-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-100">
          <Brain className="h-6 w-6 text-violet-600" />
        </div>

        <div>
          <h1 className="text-lg font-bold text-slate-900">
            Mood<span className="text-violet-600">Mentor</span>
          </h1>

          <p className="text-[11px] text-slate-400">
            Emotional wellness
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-6">
        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Main Menu
        </p>

        {menuItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? 'bg-violet-50 text-violet-700'
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              <Icon className="h-5 w-5" />

              {item.label}
            </NavLink>
          )
        })}
      </nav>

      {/* Bottom */}
      <div className="space-y-1 border-t border-slate-100 p-3">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
              isActive
                ? 'bg-violet-50 text-violet-700'
                : 'text-slate-500 hover:bg-slate-50'
            }`
          }
        >
          <Settings className="h-5 w-5" />
          Settings
        </NavLink>

        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-slate-500 transition hover:bg-red-50 hover:text-red-600">
          <LogOut className="h-5 w-5" />
          Logout
        </button>
      </div>
    </aside>
  )
}