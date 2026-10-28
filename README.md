# transcript-qa-toolkit

Small QA toolkit for audio transcription review and LLM response evaluation.
Built to demonstrate the exact work Mercor screens for: data accuracy checks,
error taxonomy, and structured annotation of model responses.

## what is inside

### 1. wer.py - word error rate checker
Compares a reference transcript against a hypothesis transcript and computes
WER (word error rate), with per-word diffs so a reviewer can see exactly what
was missed, misheard, or inserted.

    python3 wer.py sample/reference.txt sample/hypothesis.txt

### 2. llm_eval_rubric.py - LLM response annotation
Reads a JSONL file of model responses, scores each one against a rubric
(accuracy, completeness, instruction-following, harm) with a stated guideline,
and outputs an annotation-ready CSV. This mirrors the response-rating work
done in AI training / RLHF-style data projects.

    python3 llm_eval_rubric.py sample/responses.jsonl annotations.csv

### 3. annotation_guideline.md - a real annotation guideline
A short written guideline defining error types (omission, misheard word,
speaker attribution, formatting) and how to label them consistently. This is
the document a data annotation lead would ask for.

### 4. sample/ - example data
Reference and hypothesis transcript pair, plus a small JSONL of LLM responses
with example annotations, so everything runs out of the box.

## why
Background in transcription QA (verbatim review, speaker ID, error correction)
and clinical documentation. This repo shows the QA mindset applied to AI data
work: measurable error rates, consistent labels, written guidelines.
