"""Reproducible T01 audit for the UCI Bank Marketing data."""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path


EXPECTED_COLUMNS = (
    "age", "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "duration", "campaign", "pdays",
    "previous", "poutcome", "emp.var.rate", "cons.price.idx",
    "cons.conf.idx", "euribor3m", "nr.employed", "y",
)
NUMERIC_COLUMNS = (
    "age", "duration", "campaign", "pdays", "previous", "emp.var.rate",
    "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed",
)
TARGET_VALUES = {"yes", "no"}


@dataclass(frozen=True)
class FeatureRule:
    description: str
    availability: str
    strict: bool
    pre_call: bool
    risk: str
    rationale: str


FEATURE_RULES = {
    "age": FeatureRule("Customer age", "pre-campaign", True, True, "low", "Customer profile known before campaign."),
    "job": FeatureRule("Occupation category", "pre-campaign", True, True, "low", "Customer profile known before campaign."),
    "marital": FeatureRule("Marital status", "pre-campaign", True, True, "low", "Customer profile known before campaign."),
    "education": FeatureRule("Education category", "pre-campaign", True, True, "low", "Customer profile known before campaign; literal unknown remains a category."),
    "default": FeatureRule("Credit default indicator", "pre-campaign", True, True, "low", "Account attribute known before campaign; literal unknown remains a category."),
    "housing": FeatureRule("Housing loan indicator", "pre-campaign", True, True, "low", "Account attribute known before campaign; literal unknown remains a category."),
    "loan": FeatureRule("Personal loan indicator", "pre-campaign", True, True, "low", "Account attribute known before campaign; literal unknown remains a category."),
    "contact": FeatureRule("Contact communication type", "pre-call", False, True, "medium", "May be assigned during campaign planning, so unavailable at strict pre-campaign scoring."),
    "month": FeatureRule("Last contact month", "pre-call", False, True, "medium", "Current-campaign scheduling field, not available at strict initial selection."),
    "day_of_week": FeatureRule("Last contact weekday", "pre-call", False, True, "medium", "Current-campaign scheduling field, not available at strict initial selection."),
    "duration": FeatureRule("Last contact duration in seconds", "post-contact", False, False, "critical", "Known only after the call; prohibited leakage."),
    "campaign": FeatureRule("Contacts in current campaign including this contact", "during-contact/current-campaign", False, True, "high", "Generated as the current campaign unfolds; prohibited for initial selection."),
    "pdays": FeatureRule("Days since contact in a previous campaign; 999 means never", "pre-campaign", True, True, "medium", "Historical campaign recency is available before the current campaign; sentinel 999 is meaningful."),
    "previous": FeatureRule("Contacts before current campaign", "pre-campaign", True, True, "medium", "Explicitly refers to earlier campaigns, not current-campaign activity."),
    "poutcome": FeatureRule("Outcome of previous marketing campaign", "pre-campaign", True, True, "medium", "Explicitly historical; nonexistent is a meaningful category."),
    "emp.var.rate": FeatureRule("Quarterly employment variation rate", "pre-campaign", True, True, "low", "Published context available by scoring time."),
    "cons.price.idx": FeatureRule("Monthly consumer price index", "pre-campaign", True, True, "low", "Published context available by scoring time."),
    "cons.conf.idx": FeatureRule("Monthly consumer confidence index", "pre-campaign", True, True, "low", "Published context available by scoring time."),
    "euribor3m": FeatureRule("Daily three-month Euribor", "pre-campaign", True, True, "low", "Published context available by scoring time."),
    "nr.employed": FeatureRule("Quarterly number employed", "pre-campaign", True, True, "low", "Published context available by scoring time."),
}


def load_rows(path: Path) -> tuple[list[dict[str, str]], str]:
    """Load the expected semicolon CSV and fail loudly on schema/target errors."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Required raw dataset not found: {path}. Supply the canonical "
            "UCI bank-additional-full.csv; data are never fabricated or substituted."
        )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        actual = tuple(reader.fieldnames or ())
        missing = sorted(set(EXPECTED_COLUMNS) - set(actual))
        extra = sorted(set(actual) - set(EXPECTED_COLUMNS))
        if missing or extra:
            raise ValueError(f"Unexpected schema; missing={missing}, extra={extra}")
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset contains no records")
    target_values = {row["y"] for row in rows}
    if not target_values <= TARGET_VALUES or not target_values:
        raise ValueError(f"Target y must contain only yes/no; found {sorted(target_values)}")
    return rows, digest


def feature_matrix() -> list[dict[str, str]]:
    return [
        {
            "feature": feature,
            "description": rule.description,
            "availability_class": rule.availability,
            "allowed_strict_model": str(rule.strict).lower(),
            "allowed_pre_call_model": str(rule.pre_call).lower(),
            "leakage_risk": rule.risk,
            "rationale": rule.rationale,
        }
        for feature, rule in FEATURE_RULES.items()
    ]


def quality_checks(rows: list[dict[str, str]], digest: str) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    def add(check_id: str, category: str, field: str, metric: str, value: object,
            severity: str, implication: str, action: str) -> None:
        checks.append({"check_id": check_id, "category": category, "field": field,
                       "metric": metric, "value": str(value), "severity": severity,
                       "implication": implication, "action": action})

    add("source_sha256", "provenance", "dataset", "sha256", digest, "info",
        "Pins the exact audited bytes.", "Verify checksum when reproducing.")
    add("dimensions_rows", "dimensions", "dataset", "rows", len(rows), "info",
        "Defines the analyzed population.", "None.")
    add("dimensions_columns", "dimensions", "dataset", "columns", len(EXPECTED_COLUMNS), "info",
        "Expected schema was validated.", "None.")
    for column in EXPECTED_COLUMNS:
        declared_type = "numeric" if column in NUMERIC_COLUMNS else "categorical"
        add(f"type_{column}", "column_type", column, "declared_type", declared_type,
            "info", "Provides the reproducible preprocessing type inventory.",
            "Parse as numeric during validation." if declared_type == "numeric" else
            "Preserve observed strings as categories.")
    positives = sum(row["y"] == "yes" for row in rows)
    add("target_positive", "target", "y", "positive_count", positives, "info",
        "Positive-class volume drives ranking evaluation.", "Use stratification only where compatible with temporal order.")
    add("target_rate", "target", "y", "positive_rate", f"{positives / len(rows):.8f}", "info",
        "Historical conversion is the random-selection baseline.", "Carry prevalence into later comparisons.")
    duplicates = len(rows) - len({tuple(row[c] for c in EXPECTED_COLUMNS) for row in rows})
    add("exact_duplicates", "duplicates", "dataset", "exact_duplicate_rows", duplicates,
        "medium" if duplicates else "info", "Exact rows may represent repeated records or valid contacts.",
        "Retain for contact-opportunity analysis; report sensitivity if material.")
    for column in EXPECTED_COLUMNS:
        values = [row[column] for row in rows]
        missing = sum(value.strip() == "" for value in values)
        add(f"missing_{column}", "missing", column, "blank_count", missing,
            "high" if missing else "info", "Blank values can break or bias preprocessing.",
            "Investigate and declare handling before modeling." if missing else "No action.")
        unknown = sum(value.lower() == "unknown" for value in values)
        if unknown:
            add(f"unknown_{column}", "unknown_category", column, "literal_unknown_count", unknown,
                "info", "Unknown is an observed category, not automatically a missing value.",
                "Preserve as an explicit category.")
    for column in NUMERIC_COLUMNS:
        try:
            values = [float(row[column]) for row in rows]
        except ValueError as exc:
            raise ValueError(f"Column {column} contains a nonnumeric value") from exc
        add(f"range_{column}", "numeric_range", column, "min|max", f"{min(values):g}|{max(values):g}",
            "info", "Range supports plausibility review.", "Review sentinel values separately.")
    add("pdays_sentinel", "semantic", "pdays", "count_999", sum(row["pdays"] == "999" for row in rows),
        "info", "999 denotes no previous contact and is not ordinary elapsed time.", "Encode sentinel meaning explicitly.")
    add("customer_id", "independence", "dataset", "stable_customer_id_present", "false", "high",
        "Customer-level train/test independence cannot be guaranteed.", "Record limitation; do not claim customer-independent evaluation.")
    month_order = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    observed = [row["month"].lower() for row in rows]
    ranks = [month_order.index(value) if value in month_order else -1 for value in observed]
    backward = sum(b < a for a, b in zip(ranks, ranks[1:]))
    add("chronology_order", "temporal", "month", "adjacent_backward_transitions", backward,
        "medium", "Rows are only approximately chronological because year/date identifiers are absent.",
        "Preserve source row order and use an ordered holdout; document approximation.")
    add("chronology_coverage", "temporal", "month", "observed_months", "|".join(dict.fromkeys(observed)),
        "info", "Month and weekday provide incomplete dates.", "Do not reconstruct unsupported exact timestamps.")
    return checks


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/bank-additional-full.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/quality"))
    args = parser.parse_args()
    rows, digest = load_rows(args.input)
    write_csv(args.output_dir / "data_quality_table.csv", quality_checks(rows, digest))
    write_csv(args.output_dir / "feature_availability_matrix.csv", feature_matrix())


if __name__ == "__main__":
    main()
