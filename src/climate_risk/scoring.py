"""
Scoring functions: four environmental risk axes and a composite.

Each sub-score is on a 0-25 scale. The composite is the sum, capped at 100.
Children-specific weights are applied where the underlying epidemiology shows
elevated child susceptibility. Defaults are tuned for rural South Asian
contexts where Hi Rapid Lab has deployment data; see docs/methodology.md
for the reasoning behind each threshold.
"""

from typing import Union
from climate_risk.inputs import LocationInputs


# ---------------------------------------------------------------------------
# Heat index (Rothfusz / NOAA)
# ---------------------------------------------------------------------------

def heat_index(temperature_c: float, humidity_percent: float) -> float:
    """
    Heat index in degrees Celsius, using the Rothfusz regression (NOAA).

    Below 80 degrees Fahrenheit (about 27 C), the heat index is not
    meaningfully different from the dry-bulb temperature, so we return the
    raw temperature in that range.

    Reference: Rothfusz (1990), NOAA Technical Attachment SR 90-23.
    """
    t_f = temperature_c * 9 / 5 + 32
    if t_f < 80:
        return temperature_c
    rh = humidity_percent
    hi_f = (
        -42.379
        + 2.04901523 * t_f
        + 10.14333127 * rh
        - 0.22475541 * t_f * rh
        - 0.00683783 * t_f * t_f
        - 0.05481717 * rh * rh
        + 0.00122874 * t_f * t_f * rh
        + 0.00085282 * t_f * rh * rh
        - 0.00000199 * t_f * t_f * rh * rh
    )
    return (hi_f - 32) * 5 / 9


# ---------------------------------------------------------------------------
# Sub-score 1: Respiratory risk from air quality
# ---------------------------------------------------------------------------

def respiratory_risk(aqi: float, child_weight: float = 1.5) -> float:
    """
    Respiratory risk score (0-25) based on US EPA AQI categories.

    Children's respiratory rate per kg body mass is roughly twice that of
    adults, and their lungs are still developing. The default child_weight
    of 1.5 applies a 50% uplift to the base adult risk, consistent with
    findings in the Lancet Countdown's children's-health analyses.

    AQI thresholds (US EPA):
        0-50:   Good
        51-100: Moderate
        101-150: Unhealthy for Sensitive Groups (children, elderly, pregnant)
        151-200: Unhealthy
        201-300: Very Unhealthy
        301+:   Hazardous

    Reference: US EPA AQI Technical Assistance Document (2018).
    """
    if aqi < 50:
        base = 0
    elif aqi < 100:
        base = 5
    elif aqi < 150:
        base = 10
    elif aqi < 200:
        base = 16
    elif aqi < 300:
        base = 22
    else:
        base = 25
    return min(base * child_weight, 25.0)


# ---------------------------------------------------------------------------
# Sub-score 2: Heat-related risk
# ---------------------------------------------------------------------------

def heat_risk(heat_index_c: float, child_weight: float = 1.5) -> float:
    """
    Heat-related health risk score (0-25) from the heat index, using
    CDC heat stress categories converted to Celsius.

    Children are at elevated heat risk for three reasons: higher body
    surface area to mass ratio (faster heat gain), less efficient sweating
    response (slower heat loss), and limited self-regulation of fluid
    intake. The default child_weight of 1.5 reflects these factors.

    Categories (CDC, Celsius equivalents):
        below 27 C:  Below caution
        27-32 C:     Caution
        32-39 C:     Extreme caution
        39-51 C:     Danger
        51+ C:       Extreme danger

    Reference: CDC, Climate Change and Public Health, Heat-Related Illness.
    """
    if heat_index_c < 27:
        base = 0
    elif heat_index_c < 32:
        base = 5
    elif heat_index_c < 39:
        base = 12
    elif heat_index_c < 51:
        base = 20
    else:
        base = 25
    return min(base * child_weight, 25.0)


# ---------------------------------------------------------------------------
# Sub-score 3: Vector-borne disease climate suitability
# ---------------------------------------------------------------------------

def vector_borne_suitability(
    temperature_c: float,
    humidity_percent: float,
    standing_water: bool,
) -> float:
    """
    Climate suitability score (0-25) for mosquito-borne disease transmission.

    The scoring covers Aedes aegypti (dengue, chikungunya, zika) and
    Anopheles species (malaria) breeding conditions, which together drive
    most paediatric vector-borne disease burden in South Asia. Without
    standing water as a breeding habitat, climate alone produces low
    transmission risk. With standing water present, temperature and
    humidity drive scoring.

    Aedes aegypti breeding optimal: 25-30 C, RH > 70%, container water.
    Anopheles breeding: 18-32 C, surface water for oviposition.

    Reference: Kraemer MUG et al., "The global distribution of the
    arbovirus vectors Aedes aegypti and Ae. albopictus", eLife (2015).
    """
    if not standing_water:
        # Without breeding habitat, climate alone gives only a baseline
        # risk score reflecting that the climate would support
        # transmission if habitat were introduced (e.g., monsoon onset).
        in_climate_window = (
            18 <= temperature_c <= 34 and humidity_percent >= 50
        )
        return 5.0 if in_climate_window else 0.0

    # Standing water present — temperature and humidity drive the score.
    # Temperature gates the result: if temperature is outside the viable
    # mosquito range, humidity alone doesn't matter.
    if temperature_c < 18 or temperature_c > 35:
        return 0.0

    temp_score = 0.0
    if 25 <= temperature_c <= 30:
        temp_score = 15
    elif 20 <= temperature_c < 25 or 30 < temperature_c <= 33:
        temp_score = 10
    elif 18 <= temperature_c < 20 or 33 < temperature_c <= 35:
        temp_score = 5

    humidity_score = 0.0
    if humidity_percent >= 75:
        humidity_score = 10
    elif humidity_percent >= 60:
        humidity_score = 6
    elif humidity_percent >= 50:
        humidity_score = 3

    return min(temp_score + humidity_score, 25.0)


# ---------------------------------------------------------------------------
# Sub-score 4: Water-borne disease risk
# ---------------------------------------------------------------------------

def water_borne_risk(
    rainfall_7day_mm: float,
    rainfall_30day_mm: float,
    drainage_quality: str = "poor",
) -> float:
    """
    Water-borne disease risk score (0-25) from flooding and stagnation.

    Heavy recent rainfall produces acute contamination risk through
    flooding of sanitation systems. Sustained rainfall over a longer
    window produces chronic stagnation risk. Drainage quality moderates
    both.

    Children under 5 carry the largest share of diarrhoeal disease
    mortality globally, and the post-flood window is when paediatric
    diarrhoeal disease incidence spikes most sharply.

    Reference: Levy K et al., "Climate Change Impacts on Waterborne
    Diseases: Moving Toward Designing Interventions", Curr Environ
    Health Rep (2018); WHO, Drinking Water Quality Guidelines (4th ed).
    """
    drainage_multiplier = {"good": 0.4, "moderate": 0.7, "poor": 1.0}[
        drainage_quality
    ]

    base = 0.0
    # Recent heavy rainfall — acute flood risk
    if rainfall_7day_mm > 200:
        base += 15
    elif rainfall_7day_mm > 100:
        base += 10
    elif rainfall_7day_mm > 50:
        base += 5

    # Sustained rainfall — chronic stagnation risk
    if rainfall_30day_mm > 500:
        base += 10
    elif rainfall_30day_mm > 250:
        base += 5

    return min(base * drainage_multiplier, 25.0)


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

def composite_score(inputs: Union[dict, LocationInputs]) -> dict:
    """
    Compute all four sub-scores plus the composite for a single location.

    Accepts either a dict (with the same keys as LocationInputs) or a
    LocationInputs dataclass. Returns a dict with five fields:

        respiratory_risk  (0-25)
        heat_risk         (0-25)
        vector_borne_risk (0-25)
        water_borne_risk  (0-25)
        composite         (0-100)
        heat_index_c      (Celsius)
    """
    if isinstance(inputs, LocationInputs):
        d = inputs.as_dict()
    else:
        d = inputs

    hi = heat_index(d["temperature_c"], d["humidity_percent"])

    r = respiratory_risk(d["aqi"])
    h = heat_risk(hi)
    v = vector_borne_suitability(
        d["temperature_c"],
        d["humidity_percent"],
        d.get("standing_water", False),
    )
    w = water_borne_risk(
        d.get("rainfall_7day_mm", 0.0),
        d.get("rainfall_30day_mm", 0.0),
        d.get("drainage_quality", "poor"),
    )

    return {
        "respiratory_risk": round(r, 1),
        "heat_risk": round(h, 1),
        "vector_borne_risk": round(v, 1),
        "water_borne_risk": round(w, 1),
        "composite": round(r + h + v + w, 1),
        "heat_index_c": round(hi, 1),
    }
