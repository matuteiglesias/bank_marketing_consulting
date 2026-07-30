"""Leakage-safe, reproducible T03 model comparison.

The source file has no complete date or customer identifier.  Consequently the
last rows are used as an *ordered-row temporal approximation*, not claimed as a
customer-independent or exact calendar holdout.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from src.data_audit import EXPECTED_COLUMNS, FEATURE_RULES


RANDOM_STATE = 1729
TEST_FRACTION = 0.20
NUMERIC_FEATURES = [
    "age", "pdays", "previous", "emp.var.rate", "cons.price.idx",
    "cons.conf.idx", "euribor3m", "nr.employed",
]
CATEGORICAL_FEATURES = [
    "job", "marital", "education", "default", "housing", "loan", "poutcome",
]
PRODUCTION_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_frame(path: Path | str) -> pd.DataFrame:
    """Load and strictly validate the canonical semicolon-delimited input."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Required raw dataset not found: {path}")
    frame = pd.read_csv(path, sep=";", keep_default_na=False)
    missing = sorted(set(EXPECTED_COLUMNS) - set(frame.columns))
    extra = sorted(set(frame.columns) - set(EXPECTED_COLUMNS))
    if missing or extra:
        raise ValueError(f"Unexpected schema; missing={missing}, extra={extra}")
    if frame.empty:
        raise ValueError("Dataset contains no records")
    if not set(frame["y"].unique()) <= {"yes", "no"}:
        raise ValueError("Target y must contain only yes/no")
    frame = frame.copy()
    frame.insert(0, "source_row_id", np.arange(1, len(frame) + 1))
    return frame


def ordered_split(frame: pd.DataFrame, test_fraction: float = TEST_FRACTION):
    """Return earlier training rows and the untouched latest ordered rows."""
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between zero and one")
    cut = math.floor(len(frame) * (1 - test_fraction))
    if cut <= 0 or cut >= len(frame):
        raise ValueError("Both ordered split partitions must be non-empty")
    train, test = frame.iloc[:cut].copy(), frame.iloc[cut:].copy()
    if train["source_row_id"].max() >= test["source_row_id"].min():
        raise AssertionError("Ordered holdout integrity failure")
    return train, test


def _numeric_steps(scale: bool) -> Pipeline:
    steps = [("impute", SimpleImputer(strategy="median"))]
    if scale:
        steps.append(("scale", StandardScaler()))
    return Pipeline(steps)


def build_models() -> dict[str, Pipeline]:
    """Construct unfitted pipelines so all preprocessing learns on train only."""
    logistic_preprocessor = ColumnTransformer(
        [
            ("numeric", _numeric_steps(scale=True), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    ordinal_preprocessor = ColumnTransformer(
        [
            ("numeric", _numeric_steps(scale=False), NUMERIC_FEATURES),
            (
                "categorical",
                Pipeline([
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("encode", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
                ]),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    categorical_mask = [False] * len(NUMERIC_FEATURES) + [True] * len(CATEGORICAL_FEATURES)
    return {
        "logistic_regression": Pipeline([
            ("preprocess", logistic_preprocessor),
            ("model", LogisticRegression(max_iter=2_000, random_state=RANDOM_STATE)),
        ]),
        "hist_gradient_boosting": Pipeline([
            ("preprocess", ordinal_preprocessor),
            ("model", HistGradientBoostingClassifier(
                categorical_features=categorical_mask, random_state=RANDOM_STATE
            )),
        ]),
    }


def ranking_metrics(y_true, scores, fractions=(0.10, 0.20, 0.30)) -> dict[str, float]:
    """Calculate deterministic capacity-cut metrics using exactly ceil(n*f) rows."""
    y = np.asarray(y_true, dtype=int)
    probability = np.asarray(scores, dtype=float)
    if y.ndim != 1 or probability.ndim != 1 or len(y) != len(probability) or not len(y):
        raise ValueError("y_true and scores must be equally sized, non-empty vectors")
    prevalence = y.mean()
    positives = y.sum()
    order = np.argsort(-probability, kind="stable")
    result: dict[str, float] = {}
    for fraction in fractions:
        n_selected = math.ceil(len(y) * fraction)
        selected_positives = int(y[order[:n_selected]].sum())
        label = int(round(fraction * 100))
        conversion = selected_positives / n_selected
        result[f"conversion_at_{label}pct"] = conversion
        result[f"recall_at_{label}pct"] = selected_positives / positives if positives else 0.0
        result[f"lift_at_{label}pct"] = conversion / prevalence if prevalence else 0.0
        result[f"incremental_conversions_at_{label}pct"] = selected_positives - n_selected * prevalence
    return result


def feature_manifest() -> dict:
    included = [
        {"feature": feature, "availability_class": FEATURE_RULES[feature].availability}
        for feature in PRODUCTION_FEATURES
    ]
    excluded = [
        {
            "feature": feature,
            "availability_class": rule.availability,
            "exclusion_reason": rule.rationale,
        }
        for feature, rule in FEATURE_RULES.items()
        if feature not in PRODUCTION_FEATURES
    ]
    return {
        "feature_set": "strict_pre_campaign",
        "included_features": included,
        "excluded_features": excluded,
        "target": "y",
        "row_identifier": "source_row_id",
        "split": {
            "method": "ordered source-row holdout",
            "test_fraction": TEST_FRACTION,
            "limitation": "Approximate chronology only; exact dates, years, and customer IDs are unavailable.",
        },
    }


def run(input_path: Path | str, output_dir: Path | str) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir)
    frame = load_frame(input_path)
    train, test = ordered_split(frame)
    x_train, x_test = train[PRODUCTION_FEATURES], test[PRODUCTION_FEATURES]
    y_train = (train["y"] == "yes").astype(int)
    y_test = (test["y"] == "yes").astype(int)

    predictions = pd.DataFrame({
        "source_row_id": test["source_row_id"].to_numpy(),
        "observed_target": y_test.to_numpy(),
        "split": "test",
    })
    comparisons = []
    for model_id, pipeline in build_models().items():
        pipeline.fit(x_train, y_train)
        scores = pipeline.predict_proba(x_test)[:, 1]
        predictions[f"prediction_{model_id}"] = scores
        comparisons.append({
            "model_id": model_id,
            "valid_for_deployment": True,
            "feature_set": "strict_pre_campaign",
            "roc_auc": roc_auc_score(y_test, scores),
            "pr_auc": average_precision_score(y_test, scores),
            "brier_score": brier_score_loss(y_test, scores),
            **ranking_metrics(y_test, scores),
            "notes": "Metrics use the same untouched ordered-row test holdout.",
        })

    comparison = pd.DataFrame(comparisons)
    # Predeclared, conservative complexity rule: the flexible candidate must
    # improve lift by at least 5% at every operational cut and not reduce PR-AUC.
    logistic = comparison.set_index("model_id").loc["logistic_regression"]
    flexible = comparison.set_index("model_id").loc["hist_gradient_boosting"]
    stable_lift_gain = all(
        flexible[f"lift_at_{cut}pct"] >= 1.05 * logistic[f"lift_at_{cut}pct"]
        for cut in (10, 20, 30)
    )
    select_flexible = stable_lift_gain and flexible["pr_auc"] >= logistic["pr_auc"]
    selected = "hist_gradient_boosting" if select_flexible else "logistic_regression"
    comparison["selected_candidate"] = comparison["model_id"].eq(selected)
    comparison["selection_rule"] = (
        "Flexible selected only with >=5% relative lift improvement at each of "
        "10%, 20%, and 30% capacity and no lower PR-AUC; otherwise logistic."
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(output_dir / "test_predictions.csv", index=False)
    comparison.to_csv(output_dir / "model_comparison.csv", index=False)
    (output_dir / "feature_manifest.json").write_text(
        json.dumps(feature_manifest(), indent=2) + "\n", encoding="utf-8"
    )
    return comparison, predictions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/bank-additional-full.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/modeling"))
    args = parser.parse_args()
    run(args.input, args.output_dir)


if __name__ == "__main__":
    main()
