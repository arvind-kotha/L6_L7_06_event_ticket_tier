"""Lab 6 branch coverage tests. Student: Arvind, SRN: PES2UG24CS628."""

import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


@pytest.mark.parametrize("manifests,rate", [(({},), 0), ([], -1)])
def test_input_validation_branches(manifests, rate):
    with pytest.raises(ValueError):
        process_ticket_manifest(manifests, rate)


def test_confirmation_tier_and_order_pricing_branches():
    manifests = [
        {"is_confirmed": False, "tier": "general", "orders": [{"qty": 1}]},
        {"is_confirmed": True, "tier": "vip", "orders": [{"qty": 1}]},
        {"is_confirmed": True, "tier": "premium", "orders": [{"qty": 1}]},
        {"is_confirmed": True, "tier": "general", "exclusive_lounge": True, "orders": [
            {"qty": 0}, {"qty": 1, "promo": "FRAUD_RISK"},
            {"qty": 2, "promo": "EARLYBIRD"}, {"qty": 4}, {"qty": 5}],
        },
        {"is_confirmed": True, "tier": "invalid", "orders": []},
    ]
    assert process_ticket_manifest(manifests, 0) == {"total_revenue": 817.0, "status": "COMPLETED"}


def test_non_vip_fraud_and_vip_manifest_cancellation():
    manifests = [
        {"is_confirmed": True, "tier": "premium", "orders": [{"qty": 2, "promo": "FRAUD_RISK"}, {"qty": 1}]},
        {"is_confirmed": True, "tier": "vip", "exclusive_lounge": True, "orders": [{"qty": 1, "promo": "FRAUD_RISK"}]},
    ]
    assert process_ticket_manifest(manifests, 0) == {"total_revenue": 345.0, "status": "COMPLETED"}


def test_audit_rejected_zero_sales_completed_and_gate_outcomes():
    assert process_ticket_manifest([{"is_confirmed": True, "tier": "bad"} for _ in range(5)], 0)["status"] == "AUDIT_REJECTED"
    assert process_ticket_manifest([], 0)["status"] == "ZERO_SALES"
    assert process_ticket_manifest([{"is_confirmed": True, "tier": "general", "orders": [{"qty": 1}]}], .1)["status"] == "COMPLETED"
    assert monitor_gate_flow([]) == "NO_DATA"
    assert monitor_gate_flow([[51], [60, 50, 51]]) == "FLOW_NORMAL"
    assert monitor_gate_flow([[51, 51]]) == "OVERFLOW"
