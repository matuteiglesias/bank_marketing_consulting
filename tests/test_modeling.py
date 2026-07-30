import math

import pytest

pytest.importorskip("numpy")
pytest.importorskip("pandas")
pytest.importorskip("sklearn")

from src.data_audit import FEATURE_RULES
from src.modeling import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    PRODUCTION_FEATURES,
    build_models,
    feature_manifest,
    load_frame,
    ordered_split,
    ranking_metrics,
    run,
)


DATA = "data/raw/bank-additional-full.csv"


def test_production_features_follow_strict_leakage_rules():
    assert PRODUCTION_FEATURES
    assert set(PRODUCTION_FEATURES) == {name for name, rule in FEATURE_RULES.items() if rule.strict}
    assert {"duration", "campaign", "contact", "month", "day_of_week"}.isdisjoint(PRODUCTION_FEATURES)


def test_ordered_holdout_is_latest_disjoint_rows():
    frame = load_frame(DATA)
    train, test = ordered_split(frame)
    assert len(train) + len(test) == len(frame)
    assert len(test) == len(frame) - math.floor(0.8 * len(frame))
    assert train.source_row_id.max() < test.source_row_id.min()
    assert list(test.source_row_id) == list(frame.iloc[len(train):].source_row_id)


def test_pipelines_own_all_preprocessing_and_are_unfitted():
    for pipeline in build_models().values():
        assert list(pipeline.named_steps) == ["preprocess", "model"]
        assert not hasattr(pipeline.named_steps["preprocess"], "transformers_")
    assert set(NUMERIC_FEATURES + CATEGORICAL_FEATURES) == set(PRODUCTION_FEATURES)


def test_ranking_metrics_exact_capacity_and_known_values():
    metrics = ranking_metrics([1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.2, 0.1], fractions=(0.2, 0.4))
    assert metrics["conversion_at_20pct"] == 1.0
    assert metrics["recall_at_20pct"] == 0.5
    assert metrics["lift_at_20pct"] == 2.5
    assert metrics["incremental_conversions_at_20pct"] == pytest.approx(0.6)
    assert metrics["conversion_at_40pct"] == 0.5


def test_manifest_accounts_for_every_feature_and_prohibited_reasons():
    manifest = feature_manifest()
    included = {item["feature"] for item in manifest["included_features"]}
    excluded = {item["feature"] for item in manifest["excluded_features"]}
    assert included | excluded == set(FEATURE_RULES)
    assert not included & excluded
    by_name = {item["feature"]: item for item in manifest["excluded_features"]}
    assert by_name["duration"]["availability_class"] == "post-contact"
    assert by_name["duration"]["exclusion_reason"]


def test_end_to_end_outputs_share_one_test_set(tmp_path):
    comparison, predictions = run(DATA, tmp_path)
    assert set(comparison.model_id) == {"logistic_regression", "hist_gradient_boosting"}
    assert comparison.selected_candidate.sum() == 1
    assert predictions.split.eq("test").all()
    assert predictions.source_row_id.is_unique
    assert set(predictions.observed_target) <= {0, 1}
    assert {
        "prediction_logistic_regression", "prediction_hist_gradient_boosting"
    } <= set(predictions)
    assert (tmp_path / "feature_manifest.json").is_file()
