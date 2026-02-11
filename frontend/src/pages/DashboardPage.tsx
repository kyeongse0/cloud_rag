import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Server, FileText, Play, History, Loader2, ArrowRight, Clock, MessageSquare } from 'lucide-react'
import { modelsApi, promptsApi, testRunsApi, type TestRunSummary } from '@/lib/api'

interface Stats {
  activeModels: number
  totalPrompts: number
  totalTests: number
}

export function DashboardPage() {
  const [stats, setStats] = useState<Stats>({ activeModels: 0, totalPrompts: 0, totalTests: 0 })
  const [recentTests, setRecentTests] = useState<TestRunSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [modelsRes, promptsRes, testsRes] = await Promise.all([
        modelsApi.list(1, 1, true),
        promptsApi.list(0, 1),
        testRunsApi.list(0, 5),
      ])

      setStats({
        activeModels: modelsRes.total,
        totalPrompts: promptsRes.total,
        totalTests: testsRes.total,
      })
      setRecentTests(testsRes.items)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Active Models',
      value: stats.activeModels,
      description: 'Registered LLM endpoints',
      icon: Server,
      href: '/models',
    },
    {
      title: 'Prompt Templates',
      value: stats.totalPrompts,
      description: 'Saved prompts',
      icon: FileText,
      href: '/prompts',
    },
    {
      title: 'Total Tests',
      value: stats.totalTests,
      description: 'All time executions',
      icon: History,
      href: '/history',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Welcome to LLM Test Platform
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        {statCards.map((stat) => (
          <Link key={stat.title} to={stat.href}>
            <Card className="hover:bg-secondary/50 transition-colors cursor-pointer">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {loading ? (
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                ) : (
                  <>
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <p className="text-xs text-muted-foreground">{stat.description}</p>
                  </>
                )}
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Tests */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recent Tests
            </CardTitle>
            <Link to="/history">
              <Button variant="ghost" size="sm">
                View all
                <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center h-32">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : recentTests.length === 0 ? (
              <div className="text-center py-8">
                <Play className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
                <p className="text-sm text-muted-foreground mb-4">No tests yet</p>
                <Link to="/test">
                  <Button size="sm">
                    <Play className="h-4 w-4 mr-2" />
                    Run First Test
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {recentTests.map((test) => (
                  <div
                    key={test.id}
                    className="flex items-start justify-between p-3 rounded-lg bg-secondary/30"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <MessageSquare className="h-4 w-4 text-muted-foreground shrink-0" />
                        <span className="text-sm font-medium truncate">
                          {test.user_message}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="secondary" className="text-xs">
                          {test.result_count} model{test.result_count !== 1 ? 's' : ''}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {new Date(test.created_at).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Start */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Start</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <ol className="space-y-3">
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                  1
                </span>
                <div>
                  <p className="text-sm font-medium">Add LLM Models</p>
                  <p className="text-xs text-muted-foreground">
                    Register your vLLM or OpenAI-compatible endpoints
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                  2
                </span>
                <div>
                  <p className="text-sm font-medium">Create Prompts</p>
                  <p className="text-xs text-muted-foreground">
                    Save reusable system prompt templates
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                  3
                </span>
                <div>
                  <p className="text-sm font-medium">Run Tests</p>
                  <p className="text-xs text-muted-foreground">
                    Compare responses from multiple models
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                  4
                </span>
                <div>
                  <p className="text-sm font-medium">Analyze Results</p>
                  <p className="text-xs text-muted-foreground">
                    Review latency, tokens, and response quality
                  </p>
                </div>
              </li>
            </ol>

            <div className="pt-2">
              <Link to="/test">
                <Button className="w-full">
                  <Play className="h-4 w-4 mr-2" />
                  Start Testing
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
