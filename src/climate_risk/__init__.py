"""
climate_risk — Children-specific environmental health risk scoring.

Public API:
    composite_score(inputs) -> dict
    heat_index(temperature_c, humidity_percent) -> float
    LocationInputs (dataclass)
"""

from climate_risk.inputs import LocationInputs
from climate_risk.scoring import (
    composite_score,
    heat_index,
    respiratory_risk,
    heat_risk,
    vector_borne_suitability,
    water_borne_risk,
)

__version__ = "0.1.0"

__all__ = [
    "LocationInputs",
    "composite_score",
    "heat_index",
    "respiratory_risk",
    "heat_risk",
    "vector_borne_suitability",
    "water_borne_risk",
]
