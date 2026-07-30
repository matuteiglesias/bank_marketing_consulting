"""Small, reproducible, hypothesis-driven EDA for T02.

This module deliberately computes descriptive aggregates only.  It does not fit a
model, and it keeps post-contact/current-campaign fields visibly separated from
the candidate production features.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Callable

from src.data_audit import load_rows


OUTPUT_FIELDS = (
    "hypothesis", "analysis", "segment", "n", "positives",
    "conversion_rate", "baseline_rate", "lift",
)


def recency_segment(row: dict[str, str]) -> str:
    """Treat pdays=999 as 'never', not as an extreme elapsed duration."""
    value = int(row["pdays"])
    if value == 999:
        return "never previously contacted (pdays=999)"
    if value <= 7:
        return "previously contacted: 0-7 days"
    if value <= 30:
        return "previously contacted: 8-30 days"
    return "previously contacted: 31+ days"


def campaign_segment(row: dict[str, str]) -> str:
    value = int(row["campaign"])
    if value <= 3:
        return str(value)
    if value <= 5:
        return "4-5"
    return "6+"


def duration_segment(row: dict[str, str]) -> str:
    value = int(row["duration"])
    if value <= 60:
        return "0-60 seconds"
    if value <= 180:
        return "61-180 seconds"
    if value <= 300:
        return "181-300 seconds"
    if value <= 600:
        return "301-600 seconds"
    return "601+ seconds"


def aggregate(rows: list[dict[str, str]], hypothesis: str, analysis: str,
              segmenter: Callable[[dict[str, str]], str]) -> list[dict[str, object]]:
    baseline = sum(row["y"] == "yes" for row in rows) / len(rows)
    groups: dict[str, list[int]] = {}
    for row in rows:
        group = segmenter(row)
        counts = groups.setdefault(group, [0, 0])
        counts[0] += 1
        counts[1] += row["y"] == "yes"
    output = []
    for segment, (n, positives) in groups.items():
        rate = positives / n
        output.append({
            "hypothesis": hypothesis, "analysis": analysis, "segment": segment,
            "n": n, "positives": positives, "conversion_rate": f"{rate:.8f}",
            "baseline_rate": f"{baseline:.8f}",
            "lift": f"{rate / baseline:.6f}" if baseline else "not_defined",
        })
    return output


def summary_metrics(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return the complete, compact evidence table for hypotheses H1-H6."""
    n = len(rows)
    order = {id(row): index for index, row in enumerate(rows)}
    euribor = sorted(float(row["euribor3m"]) for row in rows)
    cuts = [euribor[int((n - 1) * fraction)] for fraction in (.25, .5, .75)]

    def euribor_segment(row: dict[str, str]) -> str:
        value = float(row["euribor3m"])
        if value <= cuts[0]:
            return f"Q1 <= {cuts[0]:g}"
        if value <= cuts[1]:
            return f"Q2 <= {cuts[1]:g}"
        if value <= cuts[2]:
            return f"Q3 <= {cuts[2]:g}"
        return f"Q4 > {cuts[2]:g}"

    def source_period(row: dict[str, str]) -> str:
        quintile = min(4, order[id(row)] * 5 // n) + 1
        return f"source-order quintile {quintile}"

    analyses = [
        ("H1", "global conversion", lambda row: "all records"),
        ("H1/H2", "conversion by prior campaign outcome", lambda row: row["poutcome"]),
        ("H2", "conversion by prior-contact recency", recency_segment),
        ("H3", "conversion by Euribor quartile", euribor_segment),
        ("H4", "conversion by approximate source-order period", source_period),
        ("H5", "conversion by current-campaign contact count (descriptive only)", campaign_segment),
        ("H6", "conversion by post-contact call duration (leakage demonstration only)", duration_segment),
    ]
    result: list[dict[str, object]] = []
    for hypothesis, analysis, segmenter in analyses:
        result.extend(aggregate(rows, hypothesis, analysis, segmenter))
    return result


def write_csv(path: Path, metrics: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(metrics)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/bank-additional-full.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/eda/eda_summary_metrics.csv"))
    args = parser.parse_args()
    rows, _ = load_rows(args.input)
    write_csv(args.output, summary_metrics(rows))


if __name__ == "__main__":
    main()
