import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Play } from 'lucide-react'

export function TestPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Run Test</h2>
        <p className="text-muted-foreground">
          Compare responses from multiple LLM models
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Test Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Test execution interface coming soon.
          </p>
          <Button disabled>
            <Play className="h-4 w-4 mr-2" />
            Run Test
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
