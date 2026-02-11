import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from '@/components/ui/dialog'
import { Plus, Pencil, Trash2, Activity, Server, Loader2 } from 'lucide-react'
import { modelsApi, type Model, type ModelCreate } from '@/lib/api'

export function ModelsPage() {
  const [models, setModels] = useState<Model[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingModel, setEditingModel] = useState<Model | null>(null)
  const [healthChecking, setHealthChecking] = useState<string | null>(null)
  const [healthResults, setHealthResults] = useState<Record<string, { healthy: boolean; latency?: number; error?: string }>>({})

  const [formData, setFormData] = useState<ModelCreate>({
    name: '',
    model_name: '',
    endpoint_url: '',
    api_key: '',
  })

  useEffect(() => {
    loadModels()
  }, [])

  const loadModels = async () => {
    try {
      setLoading(true)
      const response = await modelsApi.list(1, 50, false)
      setModels(response.items)
    } catch (error) {
      console.error('Failed to load models:', error)
    } finally {
      setLoading(false)
    }
  }

  const openCreateDialog = () => {
    setEditingModel(null)
    setFormData({ name: '', model_name: '', endpoint_url: '', api_key: '' })
    setDialogOpen(true)
  }

  const openEditDialog = (model: Model) => {
    setEditingModel(model)
    setFormData({
      name: model.name,
      model_name: model.model_name || '',
      endpoint_url: model.endpoint_url,
      api_key: '',
    })
    setDialogOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingModel) {
        await modelsApi.update(editingModel.id, {
          name: formData.name,
          model_name: formData.model_name || undefined,
          endpoint_url: formData.endpoint_url,
          api_key: formData.api_key || undefined,
        })
      } else {
        await modelsApi.create(formData)
      }
      setDialogOpen(false)
      loadModels()
    } catch (error) {
      console.error('Failed to save model:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this model?')) return
    try {
      await modelsApi.delete(id)
      loadModels()
    } catch (error) {
      console.error('Failed to delete model:', error)
    }
  }

  const handleHealthCheck = async (id: string) => {
    setHealthChecking(id)
    try {
      const result = await modelsApi.healthCheck(id)
      setHealthResults((prev) => ({
        ...prev,
        [id]: {
          healthy: result.is_healthy,
          latency: result.latency_ms ?? undefined,
          error: result.error ?? undefined,
        },
      }))
    } catch (error) {
      setHealthResults((prev) => ({
        ...prev,
        [id]: { healthy: false, error: 'Health check failed' },
      }))
    } finally {
      setHealthChecking(null)
    }
  }

  const handleToggleActive = async (model: Model) => {
    try {
      await modelsApi.update(model.id, { is_active: !model.is_active })
      loadModels()
    } catch (error) {
      console.error('Failed to toggle model status:', error)
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
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Models</h2>
          <p className="text-muted-foreground">
            Manage your LLM model endpoints
          </p>
        </div>
        <Button onClick={openCreateDialog}>
          <Plus className="h-4 w-4 mr-2" />
          Add Model
        </Button>
      </div>

      {models.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No models yet</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Add your first LLM model endpoint to get started.
            </p>
            <Button onClick={openCreateDialog}>
              <Plus className="h-4 w-4 mr-2" />
              Add Model
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {models.map((model) => (
            <Card key={model.id} className={!model.is_active ? 'opacity-60' : ''}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <Server className="h-5 w-5 text-muted-foreground" />
                    <CardTitle className="text-lg">{model.name}</CardTitle>
                  </div>
                  <Badge variant={model.is_active ? 'success' : 'secondary'}>
                    {model.is_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm">
                  <span className="text-muted-foreground">Endpoint: </span>
                  <span className="font-mono text-xs break-all">{model.endpoint_url}</span>
                </div>
                {model.model_name && (
                  <div className="text-sm">
                    <span className="text-muted-foreground">Model: </span>
                    <span className="font-mono text-xs">{model.model_name}</span>
                  </div>
                )}

                {healthResults[model.id] && (
                  <div className="text-sm">
                    {healthResults[model.id].healthy ? (
                      <Badge variant="success">
                        Healthy {healthResults[model.id].latency && `(${healthResults[model.id].latency}ms)`}
                      </Badge>
                    ) : (
                      <Badge variant="destructive">
                        Unhealthy: {healthResults[model.id].error}
                      </Badge>
                    )}
                  </div>
                )}

                <div className="flex gap-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleHealthCheck(model.id)}
                    disabled={healthChecking === model.id}
                  >
                    {healthChecking === model.id ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Activity className="h-4 w-4" />
                    )}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => openEditDialog(model)}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleToggleActive(model)}
                  >
                    {model.is_active ? 'Disable' : 'Enable'}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDelete(model.id)}
                    className="text-destructive hover:text-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingModel ? 'Edit Model' : 'Add New Model'}
            </DialogTitle>
            <DialogDescription>
              {editingModel
                ? 'Update the model configuration.'
                : 'Register a new LLM model endpoint.'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Display Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g., Llama 3 8B"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="model_name">Model Name (API)</Label>
              <Input
                id="model_name"
                value={formData.model_name}
                onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                placeholder="e.g., meta-llama/Llama-3-8B-Instruct"
              />
              <p className="text-xs text-muted-foreground">
                The model identifier used in API calls
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="endpoint_url">Endpoint URL</Label>
              <Input
                id="endpoint_url"
                value={formData.endpoint_url}
                onChange={(e) => setFormData({ ...formData, endpoint_url: e.target.value })}
                placeholder="http://localhost:8000"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="api_key">API Key (Optional)</Label>
              <Input
                id="api_key"
                type="password"
                value={formData.api_key}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                placeholder={editingModel ? '(unchanged)' : 'Enter API key'}
              />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">
                {editingModel ? 'Save Changes' : 'Add Model'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
