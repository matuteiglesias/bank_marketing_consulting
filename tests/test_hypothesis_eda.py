from src.hypothesis_eda import recency_segment, summary_metrics


def row(**values):
    base = {"y": "no", "pdays": "999", "poutcome": "nonexistent",
            "euribor3m": "1", "campaign": "1", "duration": "0"}
    base.update(values)
    return base


def test_recency_sentinel_is_a_distinct_meaningful_segment():
    assert recency_segment(row(pdays="999")).startswith("never previously")
    assert recency_segment(row(pdays="7")).endswith("0-7 days")
    assert recency_segment(row(pdays="8")).endswith("8-30 days")
    assert recency_segment(row(pdays="31")).endswith("31+ days")


def test_summary_covers_named_hypotheses_and_reconciles_counts():
    rows = [row(), row(y="yes", pdays="3", poutcome="success", euribor3m="5",
                      campaign="6", duration="700")]
    metrics = summary_metrics(rows)
    assert {item["hypothesis"] for item in metrics} == {"H1", "H1/H2", "H2", "H3", "H4", "H5", "H6"}
    global_row = next(item for item in metrics if item["analysis"] == "global conversion")
    assert (global_row["n"], global_row["positives"], global_row["conversion_rate"]) == (2, 1, "0.50000000")
    for analysis in {item["analysis"] for item in metrics}:
        subset = [item for item in metrics if item["analysis"] == analysis]
        assert sum(item["n"] for item in subset) == len(rows)
        assert sum(item["positives"] for item in subset) == 1


def test_campaign_and_duration_are_explicitly_nonproduction_analyses():
    analyses = {item["analysis"] for item in summary_metrics([row()])}
    assert any("descriptive only" in name for name in analyses if "campaign" in name)
    assert any("leakage demonstration only" in name for name in analyses if "duration" in name)
