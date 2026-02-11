import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from '@/components/ui/dialog'
import { Plus, Pencil, Trash2, Star, History, Loader2, FileText } from 'lucide-react'
import { promptsApi, type Prompt, type PromptCreate, type PromptVersion } from '@/lib/api'

export function PromptsPage() {
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [versionsDialogOpen, setVersionsDialogOpen] = useState(false)
  const [editingPrompt, setEditingPrompt] = useState<Prompt | null>(null)
  const [selectedPromptVersions, setSelectedPromptVersions] = useState<PromptVersion[]>([])
  const [selectedPromptId, setSelectedPromptId] = useState<string | null>(null)

  const [formData, setFormData] = useState<PromptCreate>({
    name: '',
    description: '',
    content: '',
    tags: [],
  })
  const [tagsInput, setTagsInput] = useState('')

  useEffect(() => {
    loadPrompts()
  }, [])

  const loadPrompts = async () => {
    try {
      setLoading(true)
      const response = await promptsApi.list(0, 50)
      setPrompts(response.items)
    } catch (error) {
      console.error('Failed to load prompts:', error)
    } finally {
      setLoading(false)
    }
  }

  const openCreateDialog = () => {
    setEditingPrompt(null)
    setFormData({ name: '', description: '', content: '', tags: [] })
    setTagsInput('')
    setDialogOpen(true)
  }

  const openEditDialog = (prompt: Prompt) => {
    setEditingPrompt(prompt)
    setFormData({
      name: prompt.name,
      description: prompt.description || '',
      content: prompt.content,
      tags: prompt.tags,
    })
    setTagsInput(prompt.tags.join(', '))
    setDialogOpen(true)
  }

  const openVersionsDialog = async (promptId: string) => {
    setSelectedPromptId(promptId)
    try {
      const versions = await promptsApi.getVersions(promptId)
      setSelectedPromptVersions(versions)
      setVersionsDialogOpen(true)
    } catch (error) {
      console.error('Failed to load versions:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const tags = tagsInput
      .split(',')
      .map((t) => t.trim())
      .filter((t) => t.length > 0)

    try {
      if (editingPrompt) {
        await promptsApi.update(editingPrompt.id, {
          name: formData.name,
          description: formData.description || undefined,
          content: formData.content,
          tags,
        })
      } else {
        await promptsApi.create({
          ...formData,
          tags,
        })
      }
      setDialogOpen(false)
      loadPrompts()
    } catch (error) {
      console.error('Failed to save prompt:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this prompt?')) return
    try {
      await promptsApi.delete(id)
      loadPrompts()
    } catch (error) {
      console.error('Failed to delete prompt:', error)
    }
  }

  const handleToggleFavorite = async (id: string) => {
    try {
      await promptsApi.toggleFavorite(id)
      loadPrompts()
    } catch (error) {
      console.error('Failed to toggle favorite:', error)
    }
  }

  const handleRollback = async (versionNumber: number) => {
    if (!selectedPromptId) return
    if (!confirm(`Rollback to version ${versionNumber}?`)) return
    try {
      await promptsApi.rollback(selectedPromptId, versionNumber)
      setVersionsDialogOpen(false)
      loadPrompts()
    } catch (error) {
      console.error('Failed to rollback:', error)
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
          <h2 className="text-3xl font-bold tracking-tight">Prompts</h2>
          <p className="text-muted-foreground">
            Manage your system prompt templates
          </p>
        </div>
        <Button onClick={openCreateDialog}>
          <Plus className="h-4 w-4 mr-2" />
          Create Prompt
        </Button>
      </div>

      {prompts.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No prompts yet</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Create your first prompt template to get started.
            </p>
            <Button onClick={openCreateDialog}>
              <Plus className="h-4 w-4 mr-2" />
              Create Prompt
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {prompts.map((prompt) => (
            <Card key={prompt.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <FileText className="h-5 w-5 text-muted-foreground" />
                    <CardTitle className="text-lg">{prompt.name}</CardTitle>
                  </div>
                  <button
                    onClick={() => handleToggleFavorite(prompt.id)}
                    className="text-muted-foreground hover:text-yellow-500"
                  >
                    <Star
                      className={`h-5 w-5 ${prompt.is_favorite ? 'fill-yellow-500 text-yellow-500' : ''}`}
                    />
                  </button>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {prompt.description && (
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {prompt.description}
                  </p>
                )}
                <div className="text-sm font-mono bg-secondary/50 p-2 rounded text-xs line-clamp-3">
                  {prompt.content}
                </div>

                {prompt.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {prompt.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}

                <div className="flex items-center justify-between pt-2 text-xs text-muted-foreground">
                  <span>v{prompt.current_version}</span>
                  <span>{new Date(prompt.updated_at).toLocaleDateString()}</span>
                </div>

                <div className="flex gap-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => openVersionsDialog(prompt.id)}
                  >
                    <History className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => openEditDialog(prompt)}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDelete(prompt.id)}
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

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingPrompt ? 'Edit Prompt' : 'Create New Prompt'}
            </DialogTitle>
            <DialogDescription>
              {editingPrompt
                ? 'Update the prompt template. A new version will be created if content changes.'
                : 'Create a reusable system prompt template.'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g., Helpful Assistant"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description (Optional)</Label>
              <Input
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Brief description of this prompt"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="content">Content</Label>
              <Textarea
                id="content"
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                placeholder="You are a helpful assistant..."
                rows={6}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="tags">Tags (comma-separated)</Label>
              <Input
                id="tags"
                value={tagsInput}
                onChange={(e) => setTagsInput(e.target.value)}
                placeholder="e.g., assistant, coding, creative"
              />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">
                {editingPrompt ? 'Save Changes' : 'Create Prompt'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Versions Dialog */}
      <Dialog open={versionsDialogOpen} onOpenChange={setVersionsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Version History</DialogTitle>
            <DialogDescription>
              View and rollback to previous versions of this prompt.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            {selectedPromptVersions.map((version) => (
              <Card key={version.id}>
                <CardHeader className="py-3">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Version {version.version_number}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-muted-foreground">
                        {new Date(version.created_at).toLocaleString()}
                      </span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleRollback(version.version_number)}
                      >
                        Rollback
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="py-2">
                  <pre className="text-xs bg-secondary/50 p-2 rounded whitespace-pre-wrap">
                    {version.content}
                  </pre>
                </CardContent>
              </Card>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
