"""
Input dataclass and validation for location-level environmental data.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal

DrainageQuality = Literal["good", "moderate", "poor"]


@dataclass
class LocationInputs:
    """
    Environmental inputs for a single location, typically a village or
    neighbourhood-sized polygon. All values are point-in-time snapshots
    or short-window aggregates appropriate for an upcoming screening
    deployment decision.

    Required:
        aqi: Air Quality Index (US EPA scale, 0-500+)
        temperature_c: Peak daily temperature, degrees Celsius
        humidity_percent: Relative humidity, 0-100

    Optional (but the water-borne and vector scores benefit from them):
        rainfall_7day_mm: Cumulative rainfall over last 7 days, mm
        rainfall_30day_mm: Cumulative rainfall over last 30 days, mm
        standing_water: Presence of standing water at the location
        drainage_quality: "good", "moderate", or "poor" — local drainage capacity

    Metadata (purely informational, not used in scoring):
        location_id: Free-form string identifier
        name: Human-readable location name
        population_under_5: Number of children under 5 at the location
        population_5_to_18: Number of children 5-18 at the location
    """

    aqi: float
    temperature_c: float
    humidity_percent: float
    rainfall_7day_mm: float = 0.0
    rainfall_30day_mm: float = 0.0
    standing_water: bool = False
    drainage_quality: DrainageQuality = "poor"

    location_id: Optional[str] = None
    name: Optional[str] = None
    population_under_5: Optional[int] = None
    population_5_to_18: Optional[int] = None

    def __post_init__(self):
        if self.aqi < 0:
            raise ValueError(f"aqi cannot be negative (got {self.aqi})")
        if not (-30 <= self.temperature_c <= 60):
            raise ValueError(
                f"temperature_c outside plausible range -30 to 60 "
                f"(got {self.temperature_c})"
            )
        if not (0 <= self.humidity_percent <= 100):
            raise ValueError(
                f"humidity_percent must be 0-100 (got {self.humidity_percent})"
            )
        if self.rainfall_7day_mm < 0 or self.rainfall_30day_mm < 0:
            raise ValueError("rainfall values cannot be negative")
        if self.drainage_quality not in ("good", "moderate", "poor"):
            raise ValueError(
                f"drainage_quality must be 'good', 'moderate', or 'poor' "
                f"(got '{self.drainage_quality}')"
            )

    def as_dict(self) -> dict:
        """Plain-dict representation for passing to scoring functions."""
        return {
            "aqi": self.aqi,
            "temperature_c": self.temperature_c,
            "humidity_percent": self.humidity_percent,
            "rainfall_7day_mm": self.rainfall_7day_mm,
            "rainfall_30day_mm": self.rainfall_30day_mm,
            "standing_water": self.standing_water,
            "drainage_quality": self.drainage_quality,
        }
