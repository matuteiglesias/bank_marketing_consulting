import csv
from pathlib import Path

import pytest

from src.data_audit import EXPECTED_COLUMNS, FEATURE_RULES, load_rows, quality_checks


def write_fixture(path: Path, **overrides: str) -> None:
    row = {column: "x" for column in EXPECTED_COLUMNS}
    row.update({"age": "40", "duration": "10", "campaign": "1", "pdays": "999",
                "previous": "0", "emp.var.rate": "1.1", "cons.price.idx": "93.2",
                "cons.conf.idx": "-40", "euribor3m": "4.2", "nr.employed": "5000",
                "month": "may", "y": "no"})
    row.update(overrides)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS, delimiter=";")
        writer.writeheader()
        writer.writerow(row)


def test_missing_input_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError, match="never fabricated"):
        load_rows(tmp_path / "missing.csv")


def test_schema_and_target_are_validated(tmp_path):
    path = tmp_path / "bank.csv"
    path.write_text("age;y\n40;maybe\n")
    with pytest.raises(ValueError, match="Unexpected schema"):
        load_rows(path)
    write_fixture(path, y="maybe")
    with pytest.raises(ValueError, match="only yes/no"):
        load_rows(path)


def test_leakage_rules_and_historical_fields_are_explicit():
    assert FEATURE_RULES["duration"].availability == "post-contact"
    assert not FEATURE_RULES["duration"].strict
    assert FEATURE_RULES["campaign"].availability == "during-contact/current-campaign"
    assert not FEATURE_RULES["campaign"].strict
    for name in ("pdays", "previous", "poutcome"):
        assert FEATURE_RULES[name].availability == "pre-campaign"
        assert FEATURE_RULES[name].rationale


def test_quality_metrics_are_deterministic(tmp_path):
    path = tmp_path / "bank.csv"
    write_fixture(path)
    rows, digest = load_rows(path)
    checks = quality_checks(rows, digest)
    values = {row["check_id"]: row["value"] for row in checks}
    assert values["dimensions_rows"] == "1"
    assert values["target_rate"] == "0.00000000"
    assert values["customer_id"] == "false"
    assert values["pdays_sentinel"] == "1"
