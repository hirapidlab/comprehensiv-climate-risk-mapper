"""
Output formatting helpers for risk scoring results.
"""

from typing import Iterable
from climate_risk.inputs import LocationInputs
from climate_risk.scoring import composite_score


def format_summary(
    inputs: LocationInputs,
    result: dict,
) -> str:
    """
    Plain-text summary of a single location's risk profile.
    Useful for printing in CLI tools or notebook outputs.
    """
    name = inputs.name or inputs.location_id or "unnamed location"
    return (
        f"{name}\n"
        f"  Composite score:  {result['composite']:5.1f} / 100\n"
        f"  Respiratory:      {result['respiratory_risk']:5.1f} / 25  (AQI {inputs.aqi:.0f})\n"
        f"  Heat:             {result['heat_risk']:5.1f} / 25  (Heat Index {result['heat_index_c']:.1f} C)\n"
        f"  Vector-borne:     {result['vector_borne_risk']:5.1f} / 25\n"
        f"  Water-borne:      {result['water_borne_risk']:5.1f} / 25\n"
    )


def priority_order(
    inputs_list: Iterable[LocationInputs],
) -> list[tuple[LocationInputs, dict]]:
    """
    Score all locations and return them ordered by composite score, highest first.
    Useful for producing a ranked screening priority list from a set of villages.
    """
    pairs = [(loc, composite_score(loc)) for loc in inputs_list]
    pairs.sort(key=lambda p: p[1]["composite"], reverse=True)
    return pairs


def screening_modules_to_prioritise(result: dict) -> list[str]:
    """
    Translate sub-scores into the screening modules that should be prioritised.
    This is a domain mapping that field teams can override based on local knowledge.
    """
    modules = []
    if result["respiratory_risk"] >= 12:
        modules.append("Respiratory examination (cough, tachypnoea, chest indrawing)")
    if result["heat_risk"] >= 12:
        modules.append("Heat-related illness screening (dehydration, electrolyte status)")
        modules.append("Nutrition and growth assessment (MUAC, weight-for-height)")
    if result["vector_borne_risk"] >= 12:
        modules.append("Fever-and-rash screening (dengue, chikungunya, malaria suspect cases)")
        modules.append("Skin examination (vector-bite distribution patterns)")
    if result["water_borne_risk"] >= 12:
        modules.append("Diarrhoeal disease screening (children under 5)")
        modules.append("WASH household assessment (water source, sanitation, hygiene)")
    if not modules:
        modules.append("Routine screening — no environment-driven priorities")
    return modules
