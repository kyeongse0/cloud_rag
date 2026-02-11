import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { Slider } from '@/components/ui/slider'
import { Select } from '@/components/ui/select'
import { Play, Loader2, Server, Clock, Hash, AlertCircle } from 'lucide-react'
import {
  modelsApi,
  promptsApi,
  testRunsApi,
  type Model,
  type Prompt,
  type TestRun,
  type ModelTestConfig,
} from '@/lib/api'

interface ModelConfig {
  model_id: string
  selected: boolean
  temperature: number
  max_tokens: number
  top_p: number
}

export function TestPage() {
  const [models, setModels] = useState<Model[]>([])
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [testResult, setTestResult] = useState<TestRun | null>(null)

  const [modelConfigs, setModelConfigs] = useState<Record<string, ModelConfig>>({})
  const [selectedPromptId, setSelectedPromptId] = useState<string>('')
  const [customSystemPrompt, setCustomSystemPrompt] = useState('')
  const [userMessage, setUserMessage] = useState('')
  const [useCustomPrompt, setUseCustomPrompt] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [modelsResponse, promptsResponse] = await Promise.all([
        modelsApi.list(1, 50, true),
        promptsApi.list(0, 50),
      ])
      setModels(modelsResponse.items)
      setPrompts(promptsResponse.items)

      // Initialize model configs
      const configs: Record<string, ModelConfig> = {}
      modelsResponse.items.forEach((model) => {
        configs[model.id] = {
          model_id: model.id,
          selected: false,
          temperature: 0.7,
          max_tokens: 1024,
          top_p: 1.0,
        }
      })
      setModelConfigs(configs)
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleModelSelection = (modelId: string) => {
    setModelConfigs((prev) => ({
      ...prev,
      [modelId]: {
        ...prev[modelId],
        selected: !prev[modelId].selected,
      },
    }))
  }

  const updateModelConfig = (
    modelId: string,
    key: 'temperature' | 'max_tokens' | 'top_p',
    value: number
  ) => {
    setModelConfigs((prev) => ({
      ...prev,
      [modelId]: {
        ...prev[modelId],
        [key]: value,
      },
    }))
  }

  const handlePromptSelect = (promptId: string) => {
    setSelectedPromptId(promptId)
    if (promptId) {
      const prompt = prompts.find((p) => p.id === promptId)
      if (prompt) {
        setCustomSystemPrompt(prompt.content)
      }
      setUseCustomPrompt(false)
    } else {
      setUseCustomPrompt(true)
    }
  }

  const selectedModels = Object.values(modelConfigs).filter((c) => c.selected)

  const handleRunTest = async () => {
    if (selectedModels.length === 0 || !userMessage.trim()) return

    setRunning(true)
    setTestResult(null)

    try {
      const modelTestConfigs: ModelTestConfig[] = selectedModels.map((config) => ({
        model_id: config.model_id,
        temperature: config.temperature,
        max_tokens: config.max_tokens,
        top_p: config.top_p,
      }))

      const result = await testRunsApi.create({
        user_message: userMessage,
        system_prompt: customSystemPrompt || undefined,
        prompt_template_id: selectedPromptId || undefined,
        models: modelTestConfigs,
      })

      setTestResult(result)
    } catch (error) {
      console.error('Failed to run test:', error)
    } finally {
      setRunning(false)
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
        <h2 className="text-3xl font-bold tracking-tight">Run Test</h2>
        <p className="text-muted-foreground">
          Compare responses from multiple LLM models
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Left Column: Configuration */}
        <div className="space-y-6">
          {/* Model Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="h-5 w-5" />
                Select Models
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {models.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No active models available. Add models first.
                </p>
              ) : (
                models.map((model) => (
                  <div key={model.id} className="space-y-3">
                    <div className="flex items-center gap-3">
                      <Checkbox
                        id={`model-${model.id}`}
                        checked={modelConfigs[model.id]?.selected || false}
                        onCheckedChange={() => toggleModelSelection(model.id)}
                      />
                      <Label
                        htmlFor={`model-${model.id}`}
                        className="flex-1 cursor-pointer"
                      >
                        <span className="font-medium">{model.name}</span>
                        {model.model_name && (
                          <span className="ml-2 text-xs text-muted-foreground font-mono">
                            ({model.model_name})
                          </span>
                        )}
                      </Label>
                    </div>

                    {modelConfigs[model.id]?.selected && (
                      <div className="ml-7 space-y-3 p-3 bg-secondary/30 rounded-md">
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <Label>Temperature</Label>
                            <span className="font-mono text-muted-foreground">
                              {modelConfigs[model.id].temperature.toFixed(2)}
                            </span>
                          </div>
                          <Slider
                            value={modelConfigs[model.id].temperature}
                            onChange={(v) => updateModelConfig(model.id, 'temperature', v)}
                            min={0}
                            max={2}
                            step={0.1}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <Label>Max Tokens</Label>
                            <span className="font-mono text-muted-foreground">
                              {modelConfigs[model.id].max_tokens}
                            </span>
                          </div>
                          <Slider
                            value={modelConfigs[model.id].max_tokens}
                            onChange={(v) => updateModelConfig(model.id, 'max_tokens', v)}
                            min={1}
                            max={4096}
                            step={1}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <Label>Top P</Label>
                            <span className="font-mono text-muted-foreground">
                              {modelConfigs[model.id].top_p.toFixed(2)}
                            </span>
                          </div>
                          <Slider
                            value={modelConfigs[model.id].top_p}
                            onChange={(v) => updateModelConfig(model.id, 'top_p', v)}
                            min={0}
                            max={1}
                            step={0.05}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          {/* Prompt Configuration */}
          <Card>
            <CardHeader>
              <CardTitle>System Prompt</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Use Saved Prompt</Label>
                <Select
                  value={selectedPromptId}
                  onChange={(e) => handlePromptSelect(e.target.value)}
                  placeholder="Select a prompt template..."
                >
                  <option value="">Custom prompt</option>
                  {prompts.map((prompt) => (
                    <option key={prompt.id} value={prompt.id}>
                      {prompt.name}
                    </option>
                  ))}
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="system-prompt">
                  {useCustomPrompt ? 'Custom System Prompt' : 'System Prompt (from template)'}
                </Label>
                <Textarea
                  id="system-prompt"
                  value={customSystemPrompt}
                  onChange={(e) => {
                    setCustomSystemPrompt(e.target.value)
                    if (!useCustomPrompt) {
                      setSelectedPromptId('')
                      setUseCustomPrompt(true)
                    }
                  }}
                  placeholder="You are a helpful assistant..."
                  rows={4}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Input and Results */}
        <div className="space-y-6">
          {/* User Message Input */}
          <Card>
            <CardHeader>
              <CardTitle>User Message</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Enter your message to test..."
                rows={6}
              />
              <Button
                onClick={handleRunTest}
                disabled={running || selectedModels.length === 0 || !userMessage.trim()}
                className="w-full"
              >
                {running ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Running Test...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Run Test ({selectedModels.length} model{selectedModels.length !== 1 ? 's' : ''})
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Test Results */}
          {testResult && (
            <Card>
              <CardHeader>
                <CardTitle>Results</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {testResult.results.map((result) => (
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
                      <div className="text-sm bg-secondary/50 p-3 rounded whitespace-pre-wrap">
                        {result.response}
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
