# tests/test_client.py
from types import SimpleNamespace

import pytest

from msla.llm.client import OllamaClient


class FakeOllama:
    """Stands in for ollama.Client: records calls and returns a canned response."""

    def __init__(self):
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            message=SimpleNamespace(content="hello"),
            done_reason="stop",
            prompt_eval_count=12,
            eval_count=30,
            total_duration=3_000_000_000,
            load_duration=1_000_000_000,
            prompt_eval_duration=500_000_000,
            eval_duration=1_500_000_000,
        )


def test_generate_maps_usage_and_text():
    result = OllamaClient("m", client=FakeOllama()).generate("hi")
    assert result.text == "hello"
    assert result.usage.prompt_tokens == 12
    assert result.usage.completion_tokens == 30
    assert result.usage.tokens_per_second == pytest.approx(20.0)  # 30 tokens / 1.5 s
    assert not result.truncated


def test_max_tokens_is_sent_only_when_given():
    fake = FakeOllama()
    client = OllamaClient("m", client=fake)
    client.generate("hi")
    client.generate("hi", temperature=0.7, max_tokens=5)
    assert fake.calls[0]["options"] == {"temperature": 0.0}
    assert fake.calls[1]["options"] == {"temperature": 0.7, "num_predict": 5}