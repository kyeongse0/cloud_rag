import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'

export function ModelsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Models</h2>
          <p className="text-muted-foreground">
            Manage your LLM model endpoints
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Model
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>No models yet</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Add your first LLM model endpoint to get started.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
