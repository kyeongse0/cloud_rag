import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function HistoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Test History</h2>
        <p className="text-muted-foreground">
          View past test executions and results
        </p>
      </div>

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
    </div>
  )
}
