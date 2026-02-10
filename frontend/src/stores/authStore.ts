import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
  picture?: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  setUser: (user: User | null) => void
  login: () => void
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,

      setUser: (user) => {
        set({ user, isAuthenticated: !!user })
      },

      login: () => {
        window.location.href = `${API_BASE_URL}/api/v1/auth/google/login`
      },

      logout: async () => {
        try {
          await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
            method: 'POST',
            credentials: 'include',
          })
        } finally {
          set({ user: null, isAuthenticated: false })
        }
      },

      checkAuth: async () => {
        set({ isLoading: true })
        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
            credentials: 'include',
          })

          if (response.ok) {
            const user = await response.json()
            set({ user, isAuthenticated: true })
          } else {
            set({ user: null, isAuthenticated: false })
          }
        } catch {
          set({ user: null, isAuthenticated: false })
        } finally {
          set({ isLoading: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
)
