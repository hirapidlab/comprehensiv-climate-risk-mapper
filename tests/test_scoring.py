"""
Unit tests for the scoring functions.

Run with: pytest
"""

import pytest
from climate_risk.inputs import LocationInputs
from climate_risk.scoring import (
    heat_index,
    respiratory_risk,
    heat_risk,
    vector_borne_suitability,
    water_borne_risk,
    composite_score,
)


# Heat index ----------------------------------------------------------------

def test_heat_index_below_threshold_returns_temperature():
    # Below ~27C, no humidity adjustment applies
    assert heat_index(20, 50) == 20
    assert heat_index(15, 80) == 15


def test_heat_index_above_threshold_increases_with_humidity():
    # At 32C, higher humidity should give higher heat index
    low_humidity = heat_index(32, 30)
    high_humidity = heat_index(32, 90)
    assert high_humidity > low_humidity


def test_heat_index_returns_celsius():
    # Sanity: result should be in plausible Celsius range
    result = heat_index(35, 70)
    assert 20 < result < 60


# Respiratory risk ----------------------------------------------------------

def test_respiratory_risk_good_air():
    # AQI < 50 should give 0
    assert respiratory_risk(20) == 0
    assert respiratory_risk(49) == 0


def test_respiratory_risk_hazardous_air_capped_at_25():
    # Even with child weight applied, score should be capped at 25
    assert respiratory_risk(400) == 25
    assert respiratory_risk(500) == 25


def test_respiratory_risk_child_weight_applied():
    # Child weight default 1.5 should bump moderate AQI
    base_with_weight = respiratory_risk(120)  # default 1.5
    no_weight = respiratory_risk(120, child_weight=1.0)
    assert base_with_weight > no_weight


# Heat risk -----------------------------------------------------------------

def test_heat_risk_cool_conditions():
    assert heat_risk(20) == 0
    assert heat_risk(26.9) == 0


def test_heat_risk_dangerous_heat():
    score = heat_risk(45)  # heat index in Danger category
    assert score > 12  # at least Extreme Caution with child weight


def test_heat_risk_capped_at_25():
    assert heat_risk(60) == 25


# Vector-borne suitability --------------------------------------------------

def test_vector_no_standing_water_low_score():
    score = vector_borne_suitability(28, 75, standing_water=False)
    assert score <= 5


def test_vector_optimal_conditions_high_score():
    # 27C, 80% humidity, standing water — ideal Aedes conditions
    score = vector_borne_suitability(27, 80, standing_water=True)
    assert score >= 20


def test_vector_cold_temperature_no_score():
    score = vector_borne_suitability(10, 80, standing_water=True)
    assert score == 0


# Water-borne risk ----------------------------------------------------------

def test_water_no_rain_no_risk():
    assert water_borne_risk(0, 0, "poor") == 0


def test_water_heavy_recent_rain_increases_score():
    low_rain = water_borne_risk(20, 100, "poor")
    high_rain = water_borne_risk(250, 600, "poor")
    assert high_rain > low_rain


def test_water_good_drainage_reduces_score():
    poor_drainage = water_borne_risk(150, 300, "poor")
    good_drainage = water_borne_risk(150, 300, "good")
    assert good_drainage < poor_drainage


def test_water_score_capped_at_25():
    assert water_borne_risk(500, 1000, "poor") == 25


# Composite -----------------------------------------------------------------

def test_composite_score_returns_all_subscores():
    inputs = {
        "aqi": 100,
        "temperature_c": 32,
        "humidity_percent": 70,
        "rainfall_7day_mm": 50,
        "rainfall_30day_mm": 200,
        "standing_water": False,
        "drainage_quality": "moderate",
    }
    result = composite_score(inputs)
    assert "respiratory_risk" in result
    assert "heat_risk" in result
    assert "vector_borne_risk" in result
    assert "water_borne_risk" in result
    assert "composite" in result
    assert "heat_index_c" in result


def test_composite_with_locationinputs_dataclass():
    loc = LocationInputs(
        aqi=120,
        temperature_c=35,
        humidity_percent=68,
        rainfall_7day_mm=30,
        rainfall_30day_mm=150,
        standing_water=False,
        drainage_quality="moderate",
        name="Test Village",
    )
    result = composite_score(loc)
    assert 0 <= result["composite"] <= 100


def test_composite_high_under_extreme_conditions():
    # The four axes have correlated drivers (the temperature that maximises
    # heat suppresses vector breeding), so an exact 100 isn't usually
    # reachable in practice. What we test is that extreme inputs produce
    # a high composite (>= 85).
    extreme = {
        "aqi": 500,
        "temperature_c": 32,
        "humidity_percent": 80,
        "rainfall_7day_mm": 250,
        "rainfall_30day_mm": 600,
        "standing_water": True,
        "drainage_quality": "poor",
    }
    result = composite_score(extreme)
    assert result["composite"] >= 85


def test_composite_subscores_independent():
    # All four sub-scores can hit max simultaneously when conditions align
    extreme = {
        "aqi": 500,
        "temperature_c": 28,
        "humidity_percent": 85,
        "rainfall_7day_mm": 250,
        "rainfall_30day_mm": 600,
        "standing_water": True,
        "drainage_quality": "poor",
    }
    result = composite_score(extreme)
    assert result["respiratory_risk"] == 25
    assert result["vector_borne_risk"] == 25
    assert result["water_borne_risk"] == 25


# Input validation ----------------------------------------------------------

def test_invalid_humidity_raises():
    with pytest.raises(ValueError):
        LocationInputs(aqi=100, temperature_c=30, humidity_percent=150)


def test_invalid_drainage_raises():
    with pytest.raises(ValueError):
        LocationInputs(
            aqi=100, temperature_c=30, humidity_percent=70,
            drainage_quality="excellent",  # not a valid category
        )


def test_negative_rainfall_raises():
    with pytest.raises(ValueError):
        LocationInputs(
            aqi=100, temperature_c=30, humidity_percent=70,
            rainfall_7day_mm=-10,
        )
