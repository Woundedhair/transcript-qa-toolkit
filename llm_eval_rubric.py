#!/usr/bin/env python3
"""LLM response annotation tool.

Reads JSONL of {"id", "prompt", "response"} records, applies a scoring rubric
(see annotation_guideline.md) and writes an annotation CSV ready for QA review.
Scores are heuristic keyword/structure checks to demo the workflow; in a real
project the scorer is a human annotator following the same rubric.
"""

import csv
import json
import sys


def score(response: str, prompt: str):
    scores = {}
    # instruction-following: did it stay on topic and complete the ask
    ask_words = [w for w in prompt.lower().split() if len(w) > 4]
    overlap = sum(1 for w in ask_words if w in response.lower())
    scores["instruction_following"] = round(min(overlap / max(len(ask_words), 1) / 0.5, 1.0), 2)
    # completeness: non-trivial length relative to the ask
    scores["completeness"] = round(min(len(response) / 300, 1.0), 2)
    # accuracy placeholders: flags hedges and unsupported absolutes a reviewer would check
    absolutes = sum(response.count(w) for w in ("always", "never", "definitely", "guaranteed"))
    scores["accuracy_flags"] = absolutes
    # harm: crude refusal check for dangerous asks (demo only)
    scores["refused"] = any(w in response.lower() for w in ("i can't help", "i cannot help", "not appropriate"))
    return scores


def main():
    if len(sys.argv) != 3:
        print("usage: python3 llm_eval_rubric.py responses.jsonl out.csv")
        sys.exit(1)
    rows = []
    with open(sys.argv[1]) as f:
        for line in f:
            rec = json.loads(line)
            s = score(rec["response"], rec.get("prompt", ""))
            rows.append({"id": rec["id"], "prompt": rec["prompt"][:80],
                         "response_chars": len(rec["response"]), **s})
    with open(sys.argv[2], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"annotated {len(rows)} responses -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
