const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'

interface RequestOptions {
  method?: RequestMethod
  body?: unknown
  headers?: Record<string, string>
}

class ApiError extends Error {
  status: number
  data?: unknown

  constructor(message: string, status: number, data?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {} } = options

  const config: RequestInit = {
    method,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  }

  if (body) {
    config.body = JSON.stringify(body)
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config)

  if (response.status === 401) {
    // Try to refresh token
    const refreshResponse = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    })

    if (refreshResponse.ok) {
      // Retry original request
      const retryResponse = await fetch(`${API_BASE_URL}${endpoint}`, config)
      if (!retryResponse.ok) {
        throw new ApiError(
          'Request failed after token refresh',
          retryResponse.status,
          await retryResponse.json().catch(() => null)
        )
      }
      return retryResponse.json()
    }

    // Refresh failed, redirect to login
    window.location.href = '/login'
    throw new ApiError('Session expired', 401)
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new ApiError(
      errorData?.detail || 'Request failed',
      response.status,
      errorData
    )
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

// Auth API
export const authApi = {
  me: () => request<User>('/api/v1/auth/me'),
  logout: () => request<void>('/api/v1/auth/logout', { method: 'POST' }),
}

// Models API
export interface Model {
  id: string
  name: string
  model_name: string | null
  endpoint_url: string
  is_active: boolean
  metadata_: Record<string, unknown> | null
  created_at: string
  updated_at: string
}

export interface ModelCreate {
  name: string
  model_name?: string
  endpoint_url: string
  api_key?: string
  metadata_?: Record<string, unknown>
}

export interface ModelUpdate {
  name?: string
  model_name?: string
  endpoint_url?: string
  api_key?: string
  is_active?: boolean
  metadata_?: Record<string, unknown>
}

export interface ModelListResponse {
  items: Model[]
  total: number
  page: number
  size: number
}

export interface ModelHealthCheck {
  model_id: string
  model_name: string
  endpoint_url: string
  is_healthy: boolean
  latency_ms: number | null
  error: string | null
}

export const modelsApi = {
  list: (page = 1, size = 20, activeOnly = true) =>
    request<ModelListResponse>(
      `/api/v1/models?page=${page}&size=${size}&active_only=${activeOnly}`
    ),
  get: (id: string) => request<Model>(`/api/v1/models/${id}`),
  create: (data: ModelCreate) =>
    request<Model>('/api/v1/models', { method: 'POST', body: data }),
  update: (id: string, data: ModelUpdate) =>
    request<Model>(`/api/v1/models/${id}`, { method: 'PUT', body: data }),
  delete: (id: string) =>
    request<void>(`/api/v1/models/${id}`, { method: 'DELETE' }),
  healthCheck: (id: string) =>
    request<ModelHealthCheck>(`/api/v1/models/${id}/health`, { method: 'POST' }),
}

// Prompts API
export interface Prompt {
  id: string
  name: string
  description: string | null
  content: string
  tags: string[]
  is_favorite: boolean
  current_version: number
  created_at: string
  updated_at: string
}

export interface PromptCreate {
  name: string
  description?: string
  content: string
  tags?: string[]
}

export interface PromptUpdate {
  name?: string
  description?: string
  content?: string
  tags?: string[]
}

export interface PromptListResponse {
  items: Prompt[]
  total: number
  skip: number
  limit: number
}

export interface PromptVersion {
  id: string
  version_number: number
  content: string
  created_at: string
}

export const promptsApi = {
  list: (skip = 0, limit = 20, favoritesOnly = false, tag?: string) => {
    let url = `/api/v1/prompts?skip=${skip}&limit=${limit}&favorites_only=${favoritesOnly}`
    if (tag) url += `&tag=${encodeURIComponent(tag)}`
    return request<PromptListResponse>(url)
  },
  get: (id: string) => request<Prompt>(`/api/v1/prompts/${id}`),
  create: (data: PromptCreate) =>
    request<Prompt>('/api/v1/prompts', { method: 'POST', body: data }),
  update: (id: string, data: PromptUpdate) =>
    request<Prompt>(`/api/v1/prompts/${id}`, { method: 'PUT', body: data }),
  delete: (id: string) =>
    request<void>(`/api/v1/prompts/${id}`, { method: 'DELETE' }),
  toggleFavorite: (id: string) =>
    request<Prompt>(`/api/v1/prompts/${id}/favorite`, { method: 'POST' }),
  getVersions: (id: string) =>
    request<PromptVersion[]>(`/api/v1/prompts/${id}/versions`),
  rollback: (id: string, versionNumber: number) =>
    request<Prompt>(`/api/v1/prompts/${id}/rollback`, {
      method: 'POST',
      body: { version_number: versionNumber },
    }),
}

// Test Runs API
export interface TestResult {
  id: string
  model_id: string
  model_name: string
  parameters: Record<string, unknown>
  response: string | null
  latency_ms: number | null
  token_count: number | null
  error: string | null
  created_at: string
}

export interface TestRun {
  id: string
  user_id: string
  prompt_template_id: string | null
  user_message: string
  system_prompt: string | null
  results: TestResult[]
  created_at: string
  updated_at: string
}

export interface TestRunSummary {
  id: string
  user_message: string
  system_prompt: string | null
  prompt_template_id: string | null
  result_count: number
  created_at: string
}

export interface TestRunListResponse {
  items: TestRunSummary[]
  total: number
  skip: number
  limit: number
}

export interface ModelTestConfig {
  model_id: string
  temperature?: number
  max_tokens?: number
  top_p?: number
}

export interface TestRunCreate {
  user_message: string
  system_prompt?: string
  prompt_template_id?: string
  models: ModelTestConfig[]
}

export const testRunsApi = {
  list: (skip = 0, limit = 20) =>
    request<TestRunListResponse>(`/api/v1/test-runs?skip=${skip}&limit=${limit}`),
  get: (id: string) => request<TestRun>(`/api/v1/test-runs/${id}`),
  create: (data: TestRunCreate) =>
    request<TestRun>('/api/v1/test-runs', { method: 'POST', body: data }),
  delete: (id: string) =>
    request<void>(`/api/v1/test-runs/${id}`, { method: 'DELETE' }),
}

// User type
export interface User {
  id: string
  email: string
  name: string
  picture: string | null
  is_active: boolean
  is_admin: boolean
}

export { ApiError }
