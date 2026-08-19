import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import Welcome from './pages/Welcome'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import MoodTracker from './pages/MoodTracker'
import Journal from './pages/Journal'
import Analytics from './pages/Analytics'
import Wellness from './pages/Wellness'
import Companion from './pages/Companion'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Welcome Page */}
        <Route path="/" element={<Welcome />} />

        {/* Login Page */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Main Application */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/mood"
          element={<MoodTracker />}
        />

        <Route
          path="/journal"
          element={<Journal />}
        />

        <Route
          path="/analytics"
          element={<Analytics />}
        />

        <Route
          path="/wellness"
          element={<Wellness />}
        />

        <Route
          path="/companion"
          element={<Companion />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />

        {/* Unknown URL → Dashboard */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App

