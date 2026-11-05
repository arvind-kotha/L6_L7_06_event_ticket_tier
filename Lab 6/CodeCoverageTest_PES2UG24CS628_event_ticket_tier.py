"""Lab 6 line coverage tests. Student: Arvind, SRN: PES2UG24CS628."""

import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def test_tiers_promotions_bulk_discount_and_lounge():
    manifests = [
        {"is_confirmed": True, "tier": "vip", "orders": [{"qty": 2}]},
        {"is_confirmed": True, "tier": "premium", "orders": [{"qty": 1, "promo": "EARLYBIRD"}]},
        {"is_confirmed": True, "tier": "general", "exclusive_lounge": True, "orders": [{"qty": 5}]},
    ]
    assert process_ticket_manifest(manifests, .1) == {"total_revenue": 717.2, "status": "COMPLETED"}


def test_unconfirmed_unknown_invalid_and_fraud_paths():
    manifests = [
        {"is_confirmed": False, "tier": "general", "orders": [{"qty": 10}]},
        {"is_confirmed": True, "tier": "unknown"},
        {"is_confirmed": True, "tier": "general", "orders": [{"qty": 0}]},
        {"is_confirmed": True, "tier": "premium", "orders": [{"qty": 2, "promo": "FRAUD_RISK"}, {"qty": 1}]},
        {"is_confirmed": True, "tier": "vip", "orders": [{"qty": 1, "promo": "FRAUD_RISK"}, {"qty": 3}]},
    ]
    assert process_ticket_manifest(manifests, 0) == {"total_revenue": 270.0, "status": "COMPLETED"}


@pytest.mark.parametrize("manifests,rate", [(({},), 0), ([], -1)])
def test_invalid_inputs(manifests, rate):
    with pytest.raises(ValueError):
        process_ticket_manifest(manifests, rate)


def test_audit_zero_sales_and_gate_flow():
    assert process_ticket_manifest([{"is_confirmed": True, "tier": "bad"} for _ in range(5)], 0)["status"] == "AUDIT_REJECTED"
    assert process_ticket_manifest([], 0)["status"] == "ZERO_SALES"
    assert monitor_gate_flow([]) == "NO_DATA"
    assert monitor_gate_flow([[51], [70, 50, 51]]) == "FLOW_NORMAL"
    assert monitor_gate_flow([[51, 52]]) == "OVERFLOW"
