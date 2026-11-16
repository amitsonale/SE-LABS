
import pytest

from shipping_quote import (
    process_shipments,
    monitor_container_pressures
)


def test_invalid_shipments_input():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)

    with pytest.raises(ValueError):
        process_shipments([], -1)


def test_air_ground_and_package_conditions():
    shipments = [
        {"manifest_approved": False},
        {
            "manifest_approved": True,
            "mode": "sea",
            "packages": []
        },
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": False,
            "express_priority": True,
            "packages": [
                {"weight_kg": 0},
                {"weight_kg": 2, "is_hazmat": True},
                {"weight_kg": 31},
                {"weight_kg": 10}
            ]
        },
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": True,
            "packages": [
                {"weight_kg": 5, "is_hazmat": True},
                {"weight_kg": 10}
            ]
        }
    ]

    result = process_shipments(shipments, 5.0)

    assert result["status"] == "FLAGGED_REVIEW"
    assert result["total_quote"] == 916.25


def test_default_ground_mode_and_empty_packages():
    shipments = [
        {"manifest_approved": True}
    ]

    result = process_shipments(shipments, 10.0)

    assert result["status"] == "CLEARED"
    assert result["total_quote"] == 10.0


def test_flagged_review():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 0},
            {"weight_kg": -1},
            {"weight_kg": 0},
            {"weight_kg": -5}
        ]
    }]

    result = process_shipments(shipments, 5.0)

    assert result["status"] == "FLAGGED_REVIEW"


def test_no_cargo():
    result = process_shipments([], 10.0)

    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"


def test_pressure_no_data():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_pressure_stable_and_reset():
    logs = [
        [],
        [13.0, 14.0, 13.0, 15.0]
    ]

    assert monitor_container_pressures(logs) == "STABLE"


def test_pressure_leak_detected():
    logs = [
        [15.0, 13.0, 12.0]
    ]

    assert monitor_container_pressures(logs) == "LEAK_DETECTED"
