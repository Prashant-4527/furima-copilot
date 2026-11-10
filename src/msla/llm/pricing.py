"""Reference prices: turn token counts into 'what would this cost on a paid API'."""
from dataclasses import dataclass

TOKENS_PER_PRICE_UNIT = 1_000_000


@dataclass(frozen=True, slots=True)
class Price:
    """US dollars per one million tokens, plus where and when the numbers came from."""

    name: str
    input_per_million: float
    output_per_million: float
    as_of: str
    source: str


# Read from the vendor's pricing page. Prices change: re-read the page and update as_of.
REFERENCE_PRICES: dict[str, Price] = {
    "gemini-3.1-flash-lite": Price(
        name="Gemini 3.1 Flash-Lite",
        input_per_million=0.25,
        output_per_million=1.50,
        as_of="2026-10-26",
        source="https://ai.google.dev/gemini-api/docs/pricing",
    ),
    "gemini-3.5-flash-lite": Price(
        name="Gemini 3.5 Flash-Lite",
        input_per_million=0.30,
        output_per_million=2.50,
        as_of="2026-10-26",
        source="https://ai.google.dev/gemini-api/docs/pricing",
    ),
}


def estimate_cost(prompt_tokens: int, completion_tokens: int, price: Price) -> float:
    """Dollars for one call at the given price."""
    return (
        prompt_tokens * price.input_per_million
        + completion_tokens * price.output_per_million
    ) / TOKENS_PER_PRICE_UNIT