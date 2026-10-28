#!/usr/bin/env python3
"""Word Error Rate (WER) checker for transcript QA.

Compares a reference transcript to a hypothesis transcript and reports
WER plus a per-word diff of the three error types reviewers care about:
omissions (deletions), misheard words (substitutions), and insertions.
"""

import sys
from difflib import SequenceMatcher


def normalize(text: str):
    return text.lower().replace(",", "").replace(".", "").split()


def wer_levenshtein(ref, hyp):
    r, h = len(ref), len(hyp)
    dp = [[0] * (h + 1) for _ in range(r + 1)]
    for i in range(r + 1):
        dp[i][0] = i
    for j in range(h + 1):
        dp[0][j] = j
    for i in range(1, r + 1):
        for j in range(1, h + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[r][h]


def diff_errors(ref, hyp):
    sm = SequenceMatcher(None, ref, hyp)
    subs, dels, ins = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace":
            subs.append((ref[i1:i2], hyp[j1:j2]))
        elif tag == "delete":
            dels.append(ref[i1:i2])
        elif tag == "insert":
            ins.append(hyp[j1:j2])
    return subs, dels, ins


def main():
    if len(sys.argv) != 3:
        print("usage: python3 wer.py reference.txt hypothesis.txt")
        sys.exit(1)
    ref = normalize(open(sys.argv[1]).read())
    hyp = normalize(open(sys.argv[2]).read())
    edits = wer_levenshtein(ref, hyp)
    subs, dels, ins = diff_errors(ref, hyp)
    n = max(len(ref), 1)
    print(f"reference words: {len(ref)}")
    print(f"hypothesis words: {len(hyp)}")
    print(f"edits: {edits}  (substitutions {sum(len(s[0]) for s in subs)}, "
          f"omissions {len(dels)}, insertions {len(ins)})")
    print(f"WER: {edits / n:.1%}")
    if subs:
        print("\nmisheard words (substitutions):")
        for r, h in subs:
            print(f"  '{' '.join(r)}' -> '{' '.join(h)}'")
    if dels:
        print("omissions (missing from transcript):")
        for d in dels:
            print(f"  '{' '.join(d)}'")
    if ins:
        print("insertions (added that was not said):")
        for i in ins:
            print(f"  '{' '.join(i)}'")


if __name__ == "__main__":
    main()
