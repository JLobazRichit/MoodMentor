
import React, { useEffect, useState } from "react";
import { api } from "../api";
import {
  User,
  Bell,
  Shield,
  Moon,
  Sun,
  Lock,
  Save,
  LogOut,
  Trash2,
  ChevronRight,
} from "lucide-react";

interface UserSettingsData {
  notifications: boolean;
  daily_reminder: boolean;
  dark_mode: boolean;
}

interface SettingToggleProps {
  title: string;
  description: string;
  enabled: boolean;
  setEnabled: (enabled: boolean) => void;
}

const Settings: React.FC = () => {
  const [userId, setUserId] = useState<number | null>(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const [notifications, setNotifications] = useState(true);
  const [dailyReminder, setDailyReminder] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [changingPassword, setChangingPassword] = useState(false);

  /*
   * Apply dark mode to the entire application.
   */
  const applyDarkMode = (enabled: boolean) => {
    document.documentElement.classList.toggle("dark", enabled);
  };

  /*
   * Load saved local dark mode immediately.
   */
  useEffect(() => {
    const savedDarkMode = localStorage.getItem("moodmentor_dark_mode");

    if (savedDarkMode !== null) {
      const enabled = savedDarkMode === "true";

      setDarkMode(enabled);
      applyDarkMode(enabled);
    }
  }, []);

  /*
   * Load logged-in user and backend settings.
   */
  useEffect(() => {
    const storedUser = localStorage.getItem("moodmentor_user");

    if (!storedUser) {
      setLoading(false);
      return;
    }

    try {
      const user = JSON.parse(storedUser);

      if (!user.id) {
        setLoading(false);
        return;
      }

      setUserId(user.id);
      loadSettings(user.id);
    } catch (error) {
      console.error("Invalid stored user:", error);
      setLoading(false);
    }
  }, []);

  /*
   * Load settings from backend.
   */
  const loadSettings = async (id: number) => {
    try {
      const response = await api.get(`/api/settings/${id}`);

      if (!response.data.success) {
        alert(
          response.data.message ||
            "Unable to load settings."
        );
        return;
      }

      const user = response.data.user;
      const settings: UserSettingsData =
        response.data.settings;

      setName(user.username || "");
      setEmail(user.email || "");

      setNotifications(
        Boolean(settings.notifications)
      );

      setDailyReminder(
        Boolean(settings.daily_reminder)
      );

      setDarkMode(Boolean(settings.dark_mode));

      applyDarkMode(Boolean(settings.dark_mode));

      localStorage.setItem(
        "moodmentor_dark_mode",
        String(Boolean(settings.dark_mode))
      );
    } catch (error) {
      console.error(
        "Failed to load settings:",
        error
      );

      alert("Unable to load your settings.");
    } finally {
      setLoading(false);
    }
  };

  /*
   * Dark mode toggle.
   */
  const handleDarkMode = (enabled: boolean) => {
    setDarkMode(enabled);
    applyDarkMode(enabled);

    localStorage.setItem(
      "moodmentor_dark_mode",
      String(enabled)
    );
  };

  /*
   * Save profile and preferences.
   */
  const handleSave = async () => {
    if (!userId) {
      alert("Please log in again.");
      return;
    }

    setSaving(true);

    try {
      const response = await api.put('/api/settings', {
          user_id: userId,
          username: name,
          email: email,
          notifications: notifications,
          daily_reminder: dailyReminder,
          dark_mode: darkMode,
        }
      );

      if (!response.data.success) {
        alert(
          response.data.message ||
            "Failed to save settings."
        );
        return;
      }

      /*
       * Keep local user information synchronized.
       */
      const storedUser =
        localStorage.getItem("moodmentor_user");

      if (storedUser) {
        const user = JSON.parse(storedUser);

        const updatedUser = {
          ...user,
          id: response.data.user.id,
          username: response.data.user.username,
          email: response.data.user.email,
        };

        localStorage.setItem(
          "moodmentor_user",
          JSON.stringify(updatedUser)
        );

        localStorage.setItem(
          "user",
          JSON.stringify(updatedUser)
        );
      }

      localStorage.setItem(
        "moodmentor_dark_mode",
        String(darkMode)
      );

      applyDarkMode(darkMode);

      setSaved(true);

      setTimeout(() => {
        setSaved(false);
      }, 2000);
    } catch (error) {
      console.error(
        "Failed to save settings:",
        error
      );

      alert("Failed to save settings.");
    } finally {
      setSaving(false);
    }
  };

  /*
   * Change password.
   */
  const handleChangePassword = async () => {
    if (!userId) {
      alert("Please log in again.");
      return;
    }

    if (!currentPassword || !newPassword) {
      alert("Please enter both passwords.");
      return;
    }

    if (newPassword.length < 6) {
      alert(
        "New password must be at least 6 characters."
      );
      return;
    }

    setChangingPassword(true);

    try {
      const response = await api.put('/api/settings/password', {
          user_id: userId,
          current_password: currentPassword,
          new_password: newPassword,
        }
      );

      if (!response.data.success) {
        alert(
          response.data.message ||
            "Unable to change password."
        );
        return;
      }

      alert("Password changed successfully.");

      setCurrentPassword("");
      setNewPassword("");
      setShowPasswordForm(false);
    } catch (error) {
      console.error(
        "Password change error:",
        error
      );

      alert("Unable to change password.");
    } finally {
      setChangingPassword(false);
    }
  };

  /*
   * Logout.
   */
  const handleLogout = () => {
    localStorage.removeItem("moodmentor_user");
    localStorage.removeItem("user");
    localStorage.removeItem("token");

    document.documentElement.classList.remove("dark");

    window.location.href = "/login";
  };

  /*
   * Delete account.
   */
  const handleDeleteAccount = async () => {
    if (!userId) {
      alert("Please log in again.");
      return;
    }

    const confirmed = window.confirm(
      "Are you sure you want to delete your account? This will permanently delete your MoodMentor data."
    );

    if (!confirmed) {
      return;
    }

    try {
      const response = await api.delete(`/api/settings/account/${userId}`);

      if (!response.data.success) {
        alert(
          response.data.message ||
            "Unable to delete account."
        );
        return;
      }

      localStorage.removeItem("moodmentor_user");
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      localStorage.removeItem("moodmentor_dark_mode");

      document.documentElement.classList.remove("dark");

      alert("Your account has been deleted.");

      window.location.href = "/";
    } catch (error) {
      console.error(
        "Delete account error:",
        error
      );

      alert("Unable to delete your account.");
    }
  };

  /*
   * Loading screen.
   */
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-600 dark:text-gray-300">
          Loading settings...
        </div>
      </div>
    );
  }

  /*
   * User not logged in.
   */
  if (!userId) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
        <div className="max-w-xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8 text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Please log in
          </h1>

          <p className="mt-2 text-gray-500 dark:text-gray-400">
            Your account information could not be found.
          </p>

          <button
            onClick={() => {
              window.location.href = "/login";
            }}
            className="mt-6 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-medium"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6 transition-colors duration-300">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Settings
          </h1>

          <p className="mt-2 text-gray-500 dark:text-gray-400">
            Manage your MoodMentor account and preferences.
          </p>
        </div>

        {/* Profile */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 mb-6 transition-colors">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-xl">
              <User className="w-5 h-5 text-purple-600" />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Profile
              </h2>

              <p className="text-sm text-gray-500 dark:text-gray-400">
                Manage your personal information
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Username
              </label>

              <input
                type="text"
                value={name}
                onChange={(e) =>
                  setName(e.target.value)
                }
                className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>

              <input
                type="email"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>
        </section>

        {/* Notifications */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 mb-6 transition-colors">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-xl">
              <Bell className="w-5 h-5 text-blue-600" />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Notifications
              </h2>

              <p className="text-sm text-gray-500 dark:text-gray-400">
                Control your notification preferences
              </p>
            </div>
          </div>

          <div className="space-y-5">
            <SettingToggle
              title="Notifications"
              description="Receive MoodMentor notifications"
              enabled={notifications}
              setEnabled={setNotifications}
            />

            <SettingToggle
              title="Daily Mood Reminder"
              description="Get a reminder to record your mood"
              enabled={dailyReminder}
              setEnabled={setDailyReminder}
            />
          </div>
        </section>

        {/* Appearance */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 mb-6 transition-colors">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-yellow-100 dark:bg-yellow-900/30 rounded-xl">
              {darkMode ? (
                <Moon className="w-5 h-5 text-yellow-600" />
              ) : (
                <Sun className="w-5 h-5 text-yellow-600" />
              )}
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Appearance
              </h2>

              <p className="text-sm text-gray-500 dark:text-gray-400">
                Customize how MoodMentor looks
              </p>
            </div>
          </div>

          <SettingToggle
            title="Dark Mode"
            description="Use a darker appearance throughout the application"
            enabled={darkMode}
            setEnabled={handleDarkMode}
          />
        </section>

        {/* Privacy & Security */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 mb-6 transition-colors">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-xl">
              <Shield className="w-5 h-5 text-green-600" />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Privacy & Security
              </h2>

              <p className="text-sm text-gray-500 dark:text-gray-400">
                Keep your account and personal information secure
              </p>
            </div>
          </div>

          <div className="space-y-3">
            <button
              onClick={() =>
                setShowPasswordForm(
                  !showPasswordForm
                )
              }
              className="w-full flex items-center justify-between p-4 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition"
            >
              <div className="flex items-center gap-3">
                <Lock className="w-5 h-5 text-gray-500" />

                <div className="text-left">
                  <p className="font-medium text-gray-900 dark:text-white">
                    Change Password
                  </p>

                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Update your account password
                  </p>
                </div>
              </div>

              <ChevronRight className="w-5 h-5 text-gray-400" />
            </button>

            {showPasswordForm && (
              <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-900 space-y-4">
                <input
                  type="password"
                  placeholder="Current password"
                  value={currentPassword}
                  onChange={(e) =>
                    setCurrentPassword(
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-purple-500"
                />

                <input
                  type="password"
                  placeholder="New password"
                  value={newPassword}
                  onChange={(e) =>
                    setNewPassword(
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-purple-500"
                />

                <button
                  onClick={handleChangePassword}
                  disabled={changingPassword}
                  className="px-5 py-3 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-medium"
                >
                  {changingPassword
                    ? "Changing..."
                    : "Change Password"}
                </button>
              </div>
            )}

            <div className="w-full flex items-center justify-between p-4 rounded-xl">
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-gray-500" />

                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    Privacy Settings
                  </p>

                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Your MoodMentor data is stored under your account.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Account */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 mb-6 transition-colors">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-5">
            Account
          </h2>

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleLogout}
              className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            >
              <LogOut className="w-5 h-5" />
              Log Out
            </button>

            <button
              onClick={handleDeleteAccount}
              className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 transition"
            >
              <Trash2 className="w-5 h-5" />
              Delete Account
            </button>
          </div>
        </section>

        {/* Save */}
        <div className="flex justify-end">
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-medium transition shadow-sm"
          >
            <Save className="w-5 h-5" />

            {saving
              ? "Saving..."
              : saved
              ? "Saved!"
              : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
};

/*
 * Reusable toggle component.
 */
const SettingToggle: React.FC<SettingToggleProps> = ({
  title,
  description,
  enabled,
  setEnabled,
}) => {
  return (
    <div className="flex items-center justify-between gap-4">
      <div>
        <p className="font-medium text-gray-900 dark:text-white">
          {title}
        </p>

        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {description}
        </p>
      </div>

      <button
        type="button"
        onClick={() => setEnabled(!enabled)}
        className={`relative w-12 h-6 rounded-full transition ${
          enabled
            ? "bg-purple-600"
            : "bg-gray-300 dark:bg-gray-600"
        }`}
        aria-label={`Toggle ${title}`}
        aria-pressed={enabled}
      >
        <span
          className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
            enabled ? "translate-x-6" : ""
          }`}
        />
      </button>
    </div>
  );
};

export default Settings;

