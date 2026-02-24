"""LLM Judge script - evaluates answer quality from a CSV using Claude API."""

import csv
import json
import sys
import time
from pathlib import Path

import anthropic


def judge_row(client, question, answer, reference_answer):
    """Judge a single row by calling the Claude API."""
    prompt = f"""You are an answer quality judge. Compare the student answer against the reference answer.

Question: {question}
Student Answer: {answer}
Reference Answer: {reference_answer}

Score on 1-5 for each:
- accuracy: how factually correct is the answer
- completeness: how thorough compared to reference
- clarity: how clear and well-written

Respond with JSON only:
{{"accuracy": <int>, "completeness": <int>, "clarity": <int>, "reasoning": "<brief>"}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/llm_judge.py <input.csv> [output.csv]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_name("judged_" + input_path.name)

    client = anthropic.Anthropic()

    # Read all rows
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from {input_path}")

    results = []
    total_accuracy = 0
    total_completeness = 0
    total_clarity = 0
    failed = 0

    for i, row in enumerate(rows):
        print(f"Judging row {i + 1}/{len(rows)}...")
        start = time.time()
        try:
            scores = judge_row(
                client,
                row["question"],
                row["answer"],
                row["reference_answer"],
            )
            elapsed = time.time() - start
            results.append({
                "question": row["question"],
                "answer": row["answer"],
                "reference_answer": row["reference_answer"],
                "accuracy": scores["accuracy"],
                "completeness": scores["completeness"],
                "clarity": scores["clarity"],
                "reasoning": scores["reasoning"],
                "latency_s": round(elapsed, 2),
            })
            total_accuracy += scores["accuracy"]
            total_completeness += scores["completeness"]
            total_clarity += scores["clarity"]
            print(f"  accuracy={scores['accuracy']} completeness={scores['completeness']} "
                  f"clarity={scores['clarity']} ({elapsed:.1f}s)")
        except Exception as e:
            failed += 1
            elapsed = time.time() - start
            print(f"  FAILED ({elapsed:.1f}s): {e}")
            results.append({
                "question": row["question"],
                "answer": row["answer"],
                "reference_answer": row["reference_answer"],
                "accuracy": 0,
                "completeness": 0,
                "clarity": 0,
                "reasoning": f"ERROR: {e}",
                "latency_s": round(elapsed, 2),
            })

    # Write output CSV
    if results:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # Summary
    judged = len(rows) - failed
    print(f"\n{'='*50}")
    print(f"Total rows: {len(rows)}")
    print(f"Judged:     {judged}")
    print(f"Failed:     {failed}")
    if judged > 0:
        print(f"Avg accuracy:     {total_accuracy / judged:.2f}")
        print(f"Avg completeness: {total_completeness / judged:.2f}")
        print(f"Avg clarity:      {total_clarity / judged:.2f}")
    print(f"Results written to {output_path}")


if __name__ == "__main__":
    main()
