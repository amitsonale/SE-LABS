
import pytest

from shipping_quote import (
    process_shipments,
    monitor_container_pressures
)


def test_invalid_shipments():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)

    with pytest.raises(ValueError):
        process_shipments([], -1)


def test_manifest_not_approved():
    result = process_shipments(
        [{"manifest_approved": False}], 10
    )
    assert result["status"] == "NO_CARGO"


def test_air_shipping():
    shipments = [{
        "manifest_approved": True,
        "mode": "air",
        "packages": [{"weight_kg": 10}]
    }]
    result = process_shipments(shipments, 5)
    assert result["total_quote"] == 125.0


def test_ground_shipping():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [{"weight_kg": 10}]
    }]
    result = process_shipments(shipments, 5)
    assert result["total_quote"] == 45.0


def test_unsupported_transport():
    shipments = [{
        "manifest_approved": True,
        "mode": "sea",
        "packages": []
    }]
    result = process_shipments(shipments, 5)
    assert result["status"] == "NO_CARGO"


def test_zero_and_negative_weights():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 0},
            {"weight_kg": -5}
        ]
    }]
    result = process_shipments(shipments, 5)
    assert result["status"] == "CLEARED"


def test_hazmat_fragile_and_non_fragile():
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "packages": [{"weight_kg": 2, "is_hazmat": True}]
        },
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": True,
            "packages": [{"weight_kg": 2, "is_hazmat": True}]
        }
    ]

    result = process_shipments(shipments, 5)
    assert result["status"] == "CLEARED"
    assert result["total_quote"] == 55.0


def test_heavy_and_normal_packages():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 31},
            {"weight_kg": 10}
        ]
    }]

    result = process_shipments(shipments, 5)
    assert result["total_quote"] == 231.0


def test_express_priority():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "express_priority": True,
        "packages": [{"weight_kg": 10}]
    }]

    result = process_shipments(shipments, 10)
    assert result["total_quote"] == 62.5


def test_flagged_review():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 0},
            {"weight_kg": 0},
            {"weight_kg": 0},
            {"weight_kg": 0}
        ]
    }]

    result = process_shipments(shipments, 5)
    assert result["status"] == "FLAGGED_REVIEW"


def test_no_cargo():
    result = process_shipments([], 10)
    assert result["status"] == "NO_CARGO"


def test_pressure_no_data():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_pressure_stable():
    assert monitor_container_pressures(
        [[15.0, 14.0, 16.0]]
    ) == "STABLE"


def test_pressure_streak_reset():
    assert monitor_container_pressures(
        [[13.0, 14.0, 13.0, 15.0]]
    ) == "STABLE"


def test_pressure_leak():
    assert monitor_container_pressures(
        [[15.0, 13.0, 12.0]]
    ) == "LEAK_DETECTED"
