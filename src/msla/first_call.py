import json
import sys
import time
from pathlib import Path

import ollama

MODEL = "qwen3:4b"
PROMPT = (
    "You are helping a seller list a second-hand item. "
    "Describe only what is visible in the photo: item type, colour, material, "
    "visible text or logos, and visible damage. "
    "If something cannot be seen, write 'unknown'. Do not guess brands or sizes."
)


def main(image_path: str) -> None:
    image = Path(image_path)
    if not image.is_file():
        sys.exit(f"Image not found: {image}")

    started = time.perf_counter()
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT, "images": [str(image)]}],
        options={"temperature": 0},
    )
    wall_seconds = time.perf_counter() - started

    runs = Path("runs")
    runs.mkdir(exist_ok=True)
    out = runs / f"{image.stem}__{MODEL.replace(':', '_')}.json"
    record = {
        "model": MODEL,
        "prompt": PROMPT,
        "image": image.name,
        "wall_seconds": round(wall_seconds, 2),
        "response": response.model_dump(mode="json"),
    }
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    print(response.message.content)
    print(
        f"\nsaved: {out}  |  {wall_seconds:.1f}s  |  "
        f"in={response.prompt_eval_count} tokens  out={response.eval_count} tokens"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python -m msla.first_call PATH_TO_PHOTO")
    main(sys.argv[1])