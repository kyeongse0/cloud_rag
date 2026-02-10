import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

export function AuthCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { checkAuth } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const handleCallback = async () => {
      const errorParam = searchParams.get('error')

      if (errorParam) {
        setError(errorParam)
        setTimeout(() => navigate('/login'), 3000)
        return
      }

      // OAuth callback sets httpOnly cookies, so we just need to check auth
      await checkAuth()
      navigate('/', { replace: true })
    }

    handleCallback()
  }, [searchParams, checkAuth, navigate])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <p className="text-destructive mb-2">Authentication failed: {error}</p>
          <p className="text-sm text-muted-foreground">Redirecting to login...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
        <p className="text-muted-foreground">Completing sign in...</p>
      </div>
    </div>
  )
}
