"""A thin, testable wrapper around the Ollama client."""
from typing import Protocol

import ollama

from msla.llm.results import LLMResult, Usage

NANOSECONDS = 1_000_000_000


class LLMClient(Protocol):
    """Anything that can turn a prompt (and optional images) into an LLMResult."""

    def generate(
        self,
        prompt: str,
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResult: ...


class OllamaClient:
    def __init__(self, model: str, client: ollama.Client | None = None) -> None:
        self.model = model
        self._client = client or ollama.Client()

    def generate(
        self,
        prompt: str,
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResult:
        options: dict[str, float | int] = {"temperature": temperature}
        if max_tokens is not None:
            options["num_predict"] = max_tokens

        message: dict = {"role": "user", "content": prompt}
        if images:
            message["images"] = images

        response = self._client.chat(
            model=self.model, messages=[message], options=options
        )
        return LLMResult(
            text=response.message.content or "",
            model=self.model,
            finish_reason=response.done_reason or "",
            usage=_usage_from(response),
        )


def _usage_from(response) -> Usage:
    return Usage(
        prompt_tokens=response.prompt_eval_count or 0,
        completion_tokens=response.eval_count or 0,
        total_seconds=(response.total_duration or 0) / NANOSECONDS,
        load_seconds=(response.load_duration or 0) / NANOSECONDS,
        prompt_seconds=(response.prompt_eval_duration or 0) / NANOSECONDS,
        generation_seconds=(response.eval_duration or 0) / NANOSECONDS,
    )