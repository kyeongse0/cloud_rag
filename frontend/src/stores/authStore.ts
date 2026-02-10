import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authApi, type User } from '@/lib/api'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  setUser: (user: User | null) => void
  login: () => void
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,
      error: null,

      setUser: (user) => {
        set({ user, isAuthenticated: !!user, error: null })
      },

      login: () => {
        window.location.href = `${API_BASE_URL}/api/v1/auth/google/login`
      },

      logout: async () => {
        try {
          await authApi.logout()
        } catch {
          // Ignore errors, still clear local state
        } finally {
          set({ user: null, isAuthenticated: false, error: null })
        }
      },

      checkAuth: async () => {
        // If already checking, don't do it again
        if (get().isLoading === false && get().isAuthenticated) {
          return
        }

        set({ isLoading: true, error: null })
        try {
          const user = await authApi.me()
          set({ user, isAuthenticated: true, isLoading: false })
        } catch {
          set({ user: null, isAuthenticated: false, isLoading: false })
        }
      },

      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
