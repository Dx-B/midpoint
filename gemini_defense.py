import argparse
from pathlib import Path

from harness import DEFENSE


def build_message(base_prompt: str, defense: bool) -> str:
    if defense:
        return DEFENSE + "\n\n" + base_prompt
    return base_prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare one user message for the Gemini website."
    )
    parser.add_argument("base_prompt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--defense", action="store_true")
    args = parser.parse_args()

    base_prompt = args.base_prompt.read_bytes().decode("utf-8")
    message = build_message(base_prompt, args.defense)
    with args.output.open("xb") as output:
        output.write(message.encode("utf-8"))