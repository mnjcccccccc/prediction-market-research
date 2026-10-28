from dataclasses import replace
from datetime import timedelta
from io import StringIO
import json

import pytest

from market_research.adapters import polymarket
from market_research.agents import InvalidDecision, judge, validate_decision
from market_research.analysis import Config, analyze
from market_research.audit import verify_manifest
from market_research.cli import main
from market_research.demo import DEMO_AS_OF, demo_snapshots
from market_research.evaluation import classification_metrics, generate_cases
from market_research.models import parse_time
from market_research.native_history import NativeHistory, PricePoint, features, fetch_history
from market_research.store import Store


@pytest.fixture
def market():
    return [m for m in demo_snapshots() if m.market_id == "DEMO-POLY-RATES"][-1]


@pytest.fixture
def native(market):
    end = parse_time(market.observed_at)
    points = [
        PricePoint((end - timedelta(hours=24 - h)).isoformat(), 0.30 if h < 24 else 0.43)
        for h in range(25)
    ]
    return NativeHistory(
        market.source,
        market.market_id,
        "clob_reported_yes_price",
        DEMO_AS_OF,
        "https://clob.polymarket.com/prices-history",
        {},
        points,
    )


def test_native_prices_never_mixed_with_gamma_current(market, native):
    a = analyze(replace(market, probability=0.9), [], Config(), DEMO_AS_OF, native)
    change = a.evidence["e_change_1h"]
    assert change["value"] == pytest.approx(0.13)
    assert change["current_probability"] == 0.43
    assert change["basis"] == "clob_reported_yes_price"
    assert change["origin"] == "exchange_native_history"
    assert "unusual_hourly_move" in {s.kind for s in a.signals}
    assert a.evidence["e_robust_z"]["baseline_moves"] == 23


def test_native_history_received_later_is_not_available(market, native):
    native.received_at = (parse_time(DEMO_AS_OF) + timedelta(minutes=1)).isoformat()
    result = features(native, market, DEMO_AS_OF)
    assert not result["e_native_history"]["available"]
    assert "e_change_1h" not in result


def test_native_future_event_is_filtered_not_used(market, native):
    native.points.append(
        PricePoint((parse_time(DEMO_AS_OF) + timedelta(hours=1)).isoformat(), 0.99)
    )
    a = analyze(market, [], Config(), DEMO_AS_OF, native)
    assert a.evidence["e_change_1h"]["value"] == pytest.approx(0.13)


def test_stale_native_series_does_not_fill_missing_history(market, native):
    native.points = native.points[:-3]
    a = analyze(market, [], Config(), DEMO_AS_OF, native)
    assert not a.evidence["e_native_history"]["available"]
    assert a.evidence["e_change_1h"]["value"] is None


def test_native_series_identity_and_order_validation(market, native):
    with pytest.raises(ValueError):
        features(replace(native, market_id="another-market"), market, DEMO_AS_OF)
    data = native.to_dict()
    data["points"].reverse()
    with pytest.raises(ValueError):
        NativeHistory.from_dict(data)


def test_local_history_preferred_when_basis_matches(market, native):
    previous = replace(
        market,
        probability=0.53,
        observed_at=(parse_time(DEMO_AS_OF) - timedelta(hours=1)).isoformat(),
    )
    a = analyze(market, [previous], Config(), DEMO_AS_OF, native)
    assert a.evidence["e_change_1h"]["value"] == pytest.approx(0.01)
    assert a.evidence["e_change_1h"]["origin"] == "local_snapshots"


def test_polymarket_history_uses_yes_token_and_bounds_samples(market):
    current_ts = int(parse_time(DEMO_AS_OF).timestamp())

    class HTTP:
        def get(self, url, params):
            assert params["market"] == "YES-TOKEN"
            assert params["endTs"] == current_ts
            return {
                "history": [
                    {"t": current_ts, "p": 0.6},
                    {"t": current_ts - 3600, "p": 0.5},
                    {"t": current_ts + 1, "p": 0.99},
                    {"t": current_ts - 7200, "p": "NaN"},
                ]
            }

    series, raw = fetch_history(replace(market, yes_token_id="YES-TOKEN"), HTTP())
    assert [p.probability for p in series.points] == [0.5, 0.6]
    assert series.issues == ["ignored_invalid_or_out_of_window_points:2"]
    assert len(raw["payload"]["history"]) == 4


def test_kalshi_history_preserves_candle_volume(market):
    current_ts = int(parse_time(DEMO_AS_OF).timestamp())

    class HTTP:
        def get(self, url, params):
            assert "/series/KXCPI/markets/T/candlesticks" in url
            return {
                "candlesticks": [
                    {
                        "end_period_ts": current_ts,
                        "yes_bid": {"close_dollars": "0.40"},
                        "yes_ask": {"close_dollars": "0.42"},
                        "volume_fp": "123.45",
                    }
                ]
            }

    m = replace(market, source="kalshi", market_id="T", series_ticker="KXCPI")
    series, _ = fetch_history(m, HTTP())
    assert series.points[0].probability == pytest.approx(0.41)
    assert series.points[0].interval_volume == 123.45
    assert series.points[0].volume_unit == "contracts"


def test_yes_token_follows_reordered_outcome_labels():
    m = polymarket(
        {
            "id": 1,
            "question": "Event?",
            "outcomes": ["No", "Yes"],
            "outcomePrices": [0.7, 0.3],
            "clobTokenIds": '["NO", "YES"]',
        },
        DEMO_AS_OF,
    )
    assert m.yes_token_id == "YES"


def test_native_sqlite_preserves_received_time_constraint(tmp_path, market, native):
    with Store(tmp_path / "data.sqlite3") as store:
        store.save_native([native])
        before = (parse_time(DEMO_AS_OF) - timedelta(seconds=1)).isoformat()
        assert store.native_for(market, before) is None
        assert store.native_for(market, DEMO_AS_OF).to_dict() == native.to_dict()


@pytest.mark.parametrize(
    "field,value", [("value", 13), ("value", -0.13), ("unit", "percent"), ("value", True)]
)
def test_quantitative_claims_must_preserve_values_signs_and_units(market, native, field, value):
    a = analyze(market, [], Config(), DEMO_AS_OF, native)
    decision = judge(a).decision
    claim = next(c for c in decision["claims"] if c["evidence_id"] == "e_change_1h")
    claim[field] = value
    with pytest.raises(InvalidDecision, match="value/sign/unit"):
        validate_decision(decision, a)


def test_schema_request_and_usage_retained_when_model_refuses(monkeypatch, market):
    a = analyze(market, [], Config(), DEMO_AS_OF)
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_MODEL", "mock-model")
    monkeypatch.delenv("LLM_RESPONSE_FORMAT", raising=False)

    def response(req, timeout):
        request = json.loads(req.data)
        assert request["response_format"]["type"] == "json_schema"
        assert request["response_format"]["json_schema"]["strict"]
        return StringIO(
            json.dumps(
                {
                    "usage": {"total_tokens": 200},
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"refusal": "refused", "content": None},
                        }
                    ],
                }
            )
        )

    monkeypatch.setattr("market_research.agents.urlopen", response)
    result = judge(a, True)
    assert result.mode == "llm_failed_abstain"
    assert result.usage["total_tokens"] == 200


def test_schema_valid_model_success_and_prompt_hash(monkeypatch, market, native):
    a = analyze(market, [], Config(), DEMO_AS_OF, native)
    expected = judge(a).decision
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_MODEL", "mock-model")
    monkeypatch.setattr(
        "market_research.agents.urlopen",
        lambda *args, **kwargs: StringIO(
            json.dumps(
                {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": json.dumps(expected)}}
                    ],
                    "usage": {"total_tokens": 123},
                }
            )
        ),
    )
    result = judge(a, True)
    assert result.mode == "llm"
    assert result.decision == expected
    assert len(result.validation["prompt_sha256"]) == 64
    assert result.validation["quantitative_claims_checked"] > 0


@pytest.mark.parametrize("payload", [[], {"choices": [None]}, {"choices": [{"message": []}]}])
def test_malformed_provider_envelope_abstains(monkeypatch, market, payload):
    a = analyze(market, [], Config(), DEMO_AS_OF)
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_MODEL", "mock-model")
    monkeypatch.setattr(
        "market_research.agents.urlopen", lambda *args, **kwargs: StringIO(json.dumps(payload))
    )
    result = judge(a, True)
    assert result.mode == "llm_failed_abstain"
    assert result.decision["action"] == "abstain"


def test_model_cannot_invent_action_without_anomaly(market):
    a = analyze(market, [], Config(), DEMO_AS_OF)
    decision = {**judge(a).decision, "action": "investigate"}
    with pytest.raises(InvalidDecision, match="detected signal"):
        validate_decision(decision, a)


def test_expiry_checked_against_analysis_time_not_capture(market):
    m = replace(market, close_time=(parse_time(DEMO_AS_OF) + timedelta(minutes=5)).isoformat())
    as_of = (parse_time(DEMO_AS_OF) + timedelta(minutes=10)).isoformat()
    assert "past_scheduled_close" in analyze(m, [], Config(), as_of).exclusion_reasons


def test_submillisecond_future_timestamp_not_hidden_by_display_rounding(market):
    m = replace(
        market, observed_at=(parse_time(DEMO_AS_OF) + timedelta(microseconds=1)).isoformat()
    )
    assert "stale_or_future_snapshot" in analyze(m, [], Config(), DEMO_AS_OF).exclusion_reasons


def test_manifest_detects_mutation_and_trace_contains_roles(tmp_path):
    assert main(["demo", "--out", str(tmp_path)]) == 0
    assert verify_manifest(tmp_path)["valid"]
    events = [json.loads(line) for line in (tmp_path / "trace.jsonl").read_text().splitlines()]
    assert {e["step"] for e in events} == {
        "market_analyst",
        "risk_reviewer",
        "research_manager",
        "validation",
    }
    with (tmp_path / "report.md").open("a", encoding="utf-8") as f:
        f.write("tampered")
    assert verify_manifest(tmp_path)["mismatches"] == ["report.md"]
    assert main(["verify", "--dir", str(tmp_path)]) == 2


def test_metrics_match_hand_calculated_confusion():
    rows = [
        {"expected": "investigate", "predicted": "investigate"},
        {"expected": "monitor", "predicted": "investigate"},
        {"expected": "abstain", "predicted": "monitor"},
    ]
    metrics = classification_metrics(rows)
    assert metrics["per_class"]["investigate"]["precision"] == 0.5
    assert metrics["unsafe_non_abstentions"] == 1
    assert metrics["false_research_alerts"] == 1


def test_synthetic_dataset_reproducible_with_disjoint_split_ids():
    first, second = generate_cases(41, 1), generate_cases(41, 1)
    assert [c.to_dict() for c in first] == [c.to_dict() for c in second]
    calibration = {c.case_id for c in first if c.split == "calibration"}
    holdout = {c.case_id for c in first if c.split == "holdout"}
    assert not calibration & holdout
    assert len(first) == 24


def test_toml_configuration_applies_and_rejects_unknowns(tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text("[analysis]\nmax_spread = 0.01\n", encoding="utf-8")
    out = tmp_path / "out"
    assert main(["demo", "--out", str(out), "--config", str(cfg)]) == 0
    report = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert report["meta"]["counts"]["eligible"] == 0
    cfg.write_text("[analysis]\nunknown_field = 3\n", encoding="utf-8")
    assert main(["demo", "--out", str(out), "--config", str(cfg)]) == 2


def test_live_bundle_includes_local_history_needed_for_exact_replay(tmp_path, market, monkeypatch):
    from market_research.adapters import Collection

    previous = replace(
        market,
        probability=0.40,
        observed_at=(parse_time(DEMO_AS_OF) - timedelta(hours=1)).isoformat(),
    )
    db = tmp_path / "history.sqlite3"
    with Store(db) as store:
        store.save([previous])
    monkeypatch.setattr("market_research.cli.utc_now", lambda: DEMO_AS_OF)
    another = replace(market, market_id="aaa")
    monkeypatch.setattr(
        "market_research.cli.collect",
        lambda *a, **k: Collection("polymarket", markets=[market, another]),
    )
    live, replay = tmp_path / "live", tmp_path / "replay"
    assert main(["collect", "--source", "polymarket", "--db", str(db), "--out", str(live)]) == 0
    assert (
        main(["replay", "--bundle", str(live / "snapshot_bundle.json"), "--out", str(replay)]) == 0
    )
    a = json.loads((live / "report.json").read_text(encoding="utf-8"))["markets"][0]
    b = json.loads((replay / "report.json").read_text(encoding="utf-8"))["markets"][0]
    assert a["analysis"] == b["analysis"]
    assert a["agent"]["decision"] == b["agent"]["decision"]
    assert a["history"] == b["history"]
    live_meta = json.loads((live / "report.json").read_text(encoding="utf-8"))["meta"]
    replay_meta = json.loads((replay / "report.json").read_text(encoding="utf-8"))["meta"]
    assert live_meta["input_sha256"] == replay_meta["input_sha256"]
