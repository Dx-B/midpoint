import json
from pathlib import Path

from gemini_defense import build_message

# Reproduce the eight archived pilot messages from the defense-off prompts.
rows = json.loads(
    Path("evidence/pilot/prompts.json").read_text(encoding="utf-8")
)
base_prompts = {
    (row["case_id"], row["mode"]): row["prompt"]
    for row in rows
    if not row["defense"]
}

cells = {(row["case_id"], row["mode"], row["defense"]) for row in rows}
assert len(rows) == len(cells) == 8 and len(base_prompts) == 4

for row in rows:
    pair = (row["case_id"], row["mode"])
    actual = build_message(base_prompts[pair], row["defense"])
    assert actual == row["prompt"], f"Prompt mismatch: {pair}, defense={row['defense']}"

print("PASS: all 8 archived pilot prompts reproduced exactly")

# Compare the saved arithmetic examples byte for byte.
base = Path("evidence/gemini-01-prompt.txt").read_bytes().decode("utf-8")
for label, enabled in (("off", False), ("on", True)):
    saved = Path(f"evidence/defense_tests/arithmetic-{label}.txt").read_bytes()
    expected = build_message(base, enabled).encode("utf-8")
    assert saved == expected, f"Arithmetic defense-{label} prompt mismatch"

print("PASS: both saved arithmetic prompts match byte for byte")
print("Model calls: 0")