"""LLM Client for vLLM and OpenAI-compatible endpoints."""

import time
from dataclasses import dataclass

import httpx


@dataclass
class LLMResponse:
    """Response from LLM API call."""

    content: str | None
    latency_ms: int
    token_count: int | None
    error: str | None


class LLMClient:
    """Client for calling vLLM/OpenAI-compatible APIs."""

    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout

    async def chat_completion(
        self,
        endpoint_url: str,
        api_key: str | None,
        model_name: str,
        user_message: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        top_p: float = 1.0,
    ) -> LLMResponse:
        """
        Call the chat completion API.

        Args:
            endpoint_url: Base URL of the vLLM/OpenAI-compatible server
            api_key: Optional API key for authentication
            model_name: Model name to use
            user_message: User's input message
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter

        Returns:
            LLMResponse with content, latency, token count, or error
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
        }

        # Ensure endpoint URL ends with /v1/chat/completions
        url = endpoint_url.rstrip("/")
        if not url.endswith("/v1/chat/completions"):
            if not url.endswith("/v1"):
                url = f"{url}/v1"
            url = f"{url}/chat/completions"

        start_time = time.perf_counter()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=headers)

            latency_ms = int((time.perf_counter() - start_time) * 1000)

            if response.status_code != 200:
                return LLMResponse(
                    content=None,
                    latency_ms=latency_ms,
                    token_count=None,
                    error=f"HTTP {response.status_code}: {response.text}",
                )

            data = response.json()

            # Extract content from OpenAI-compatible response
            content = None
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]

            # Extract token count from usage
            token_count = None
            if "usage" in data:
                token_count = data["usage"].get("total_tokens")

            return LLMResponse(
                content=content,
                latency_ms=latency_ms,
                token_count=token_count,
                error=None,
            )

        except httpx.TimeoutException:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            return LLMResponse(
                content=None,
                latency_ms=latency_ms,
                token_count=None,
                error="Request timeout",
            )
        except httpx.RequestError as e:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            return LLMResponse(
                content=None,
                latency_ms=latency_ms,
                token_count=None,
                error=f"Request error: {str(e)}",
            )
        except Exception as e:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            return LLMResponse(
                content=None,
                latency_ms=latency_ms,
                token_count=None,
                error=f"Unexpected error: {str(e)}",
            )


# Singleton instance
llm_client = LLMClient()
