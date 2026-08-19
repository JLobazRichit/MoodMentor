import { Bell, Search, User } from 'lucide-react'

interface TopbarProps {
  user: {
    id: number
    username: string
    email: string
  }
}

export default function Topbar({
  user,
}: TopbarProps) {

  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-5 sm:px-8">

      <div>

        <p className="text-sm text-slate-400">
          Welcome back
        </p>

        <h2 className="text-lg font-semibold text-slate-900">
          Your emotional wellness space
        </h2>

      </div>


      <div className="flex items-center gap-3">

        <button className="hidden rounded-xl p-2.5 text-slate-500 hover:bg-slate-100 sm:block">
          <Search className="h-5 w-5" />
        </button>


        <button className="relative rounded-xl p-2.5 text-slate-500 hover:bg-slate-100">

          <Bell className="h-5 w-5" />

          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-violet-500" />

        </button>


        <div className="flex items-center gap-3 border-l border-slate-200 pl-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet-100">
            <User className="h-5 w-5 text-violet-600" />
          </div>


          <div className="hidden sm:block">

            <p className="text-sm font-semibold text-slate-800">
              {user.username}
            </p>

            <p className="text-xs text-slate-400">
              Wellness journey
            </p>

          </div>

        </div>

      </div>

    </header>
  )
}