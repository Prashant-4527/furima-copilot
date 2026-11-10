import pytest

from msla.llm.pricing import Price, estimate_cost

PRICE = Price("test", input_per_million=1.0, output_per_million=4.0, as_of="2026-01-01", source="n/a")


def test_estimate_cost_adds_input_and_output():
    # 1,000 input tokens at $1 per million = $0.001; 500 output at $4 per million = $0.002
    assert estimate_cost(1_000, 500, PRICE) == pytest.approx(0.003)


def test_zero_tokens_cost_nothing():
    assert estimate_cost(0, 0, PRICE) == 0.0