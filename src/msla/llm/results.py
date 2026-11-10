"""Plain data containers returned by every model call."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Usage:
    """Token counts and timings for one model call (seconds, not nanoseconds)."""

    prompt_tokens: int
    completion_tokens: int
    total_seconds: float
    load_seconds: float
    prompt_seconds: float
    generation_seconds: float

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def tokens_per_second(self) -> float:
        """Generation speed: output tokens divided by generation time."""
        if self.generation_seconds <= 0:
            return 0.0
        return self.completion_tokens / self.generation_seconds


@dataclass(frozen=True, slots=True)
class LLMResult:
    """What a caller gets back: the text, which model made it, and the usage."""

    text: str
    model: str
    finish_reason: str  # "stop" = finished by itself; "length" = cut off
    usage: Usage

    @property
    def truncated(self) -> bool:
        return self.finish_reason == "length"