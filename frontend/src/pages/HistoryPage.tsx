import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'
import { Loader2, Trash2, Eye, Clock, Hash, AlertCircle, MessageSquare } from 'lucide-react'
import { testRunsApi, type TestRunSummary, type TestRun } from '@/lib/api'

export function HistoryPage() {
  const [testRuns, setTestRuns] = useState<TestRunSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTestRun, setSelectedTestRun] = useState<TestRun | null>(null)
  const [detailDialogOpen, setDetailDialogOpen] = useState(false)
  const [loadingDetail, setLoadingDetail] = useState(false)

  useEffect(() => {
    loadTestRuns()
  }, [])

  const loadTestRuns = async () => {
    try {
      setLoading(true)
      const response = await testRunsApi.list(0, 50)
      setTestRuns(response.items)
    } catch (error) {
      console.error('Failed to load test runs:', error)
    } finally {
      setLoading(false)
    }
  }

  const openDetailDialog = async (id: string) => {
    setLoadingDetail(true)
    setDetailDialogOpen(true)
    try {
      const testRun = await testRunsApi.get(id)
      setSelectedTestRun(testRun)
    } catch (error) {
      console.error('Failed to load test run details:', error)
    } finally {
      setLoadingDetail(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this test run?')) return
    try {
      await testRunsApi.delete(id)
      loadTestRuns()
    } catch (error) {
      console.error('Failed to delete test run:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Test History</h2>
        <p className="text-muted-foreground">
          View past test executions and results
        </p>
      </div>

      {testRuns.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No test history</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Run your first test to see results here.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {testRuns.map((testRun) => (
            <Card key={testRun.id}>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-2">
                      <MessageSquare className="h-4 w-4 text-muted-foreground" />
                      <span className="font-medium line-clamp-1">
                        {testRun.user_message}
                      </span>
                    </div>
                    {testRun.system_prompt && (
                      <p className="text-sm text-muted-foreground line-clamp-1">
                        System: {testRun.system_prompt}
                      </p>
                    )}
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">
                        {testRun.result_count} model{testRun.result_count !== 1 ? 's' : ''}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        {new Date(testRun.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => openDetailDialog(testRun.id)}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(testRun.id)}
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Detail Dialog */}
      <Dialog open={detailDialogOpen} onOpenChange={setDetailDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Test Run Details</DialogTitle>
            <DialogDescription>
              View the full results of this test execution.
            </DialogDescription>
          </DialogHeader>

          {loadingDetail ? (
            <div className="flex items-center justify-center h-32">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : selectedTestRun ? (
            <div className="space-y-6">
              {/* Test Configuration */}
              <div className="space-y-3">
                <h4 className="font-medium">User Message</h4>
                <div className="text-sm bg-secondary/50 p-3 rounded whitespace-pre-wrap">
                  {selectedTestRun.user_message}
                </div>

                {selectedTestRun.system_prompt && (
                  <>
                    <h4 className="font-medium">System Prompt</h4>
                    <div className="text-sm bg-secondary/50 p-3 rounded whitespace-pre-wrap">
                      {selectedTestRun.system_prompt}
                    </div>
                  </>
                )}
              </div>

              {/* Results */}
              <div className="space-y-3">
                <h4 className="font-medium">Results</h4>
                {selectedTestRun.results.map((result) => (
                  <div key={result.id} className="border rounded-lg p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{result.model_name}</span>
                      <div className="flex items-center gap-2">
                        {result.error ? (
                          <Badge variant="destructive">
                            <AlertCircle className="h-3 w-3 mr-1" />
                            Error
                          </Badge>
                        ) : (
                          <>
                            {result.latency_ms && (
                              <Badge variant="secondary">
                                <Clock className="h-3 w-3 mr-1" />
                                {result.latency_ms}ms
                              </Badge>
                            )}
                            {result.token_count && (
                              <Badge variant="secondary">
                                <Hash className="h-3 w-3 mr-1" />
                                {result.token_count} tokens
                              </Badge>
                            )}
                          </>
                        )}
                      </div>
                    </div>

                    {result.error ? (
                      <div className="text-sm text-destructive bg-destructive/10 p-3 rounded">
                        {result.error}
                      </div>
                    ) : (
                      <div className="text-sm bg-secondary/50 p-3 rounded whitespace-pre-wrap max-h-64 overflow-y-auto">
                        {result.response}
                      </div>
                    )}

                    {result.parameters && Object.keys(result.parameters).length > 0 && (
                      <div className="text-xs text-muted-foreground">
                        Parameters: temp={String(result.parameters.temperature ?? 'N/A')},
                        max_tokens={String(result.parameters.max_tokens ?? 'N/A')},
                        top_p={String(result.parameters.top_p ?? 'N/A')}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="text-xs text-muted-foreground">
                Created: {new Date(selectedTestRun.created_at).toLocaleString()}
              </div>
            </div>
          ) : null}
        </DialogContent>
      </Dialog>
    </div>
  )
}
