# Comprehensiv Climate Risk Mapper

A small Python library for estimating children-specific health risk from environmental exposure data. Designed for community health programs that need to decide where to send field teams first — based on the climate conditions that disproportionately affect children in low-resource rural settings.

## What it does

You give it inputs for a location — air quality index, temperature, humidity, recent rainfall, presence of standing water, drainage quality — and it returns a composite health-risk score (0-100) for children at that location, disaggregated by four domains:

- **Respiratory risk** from air quality (PM2.5, AQI)
- **Heat risk** from temperature × humidity (heat index)
- **Vector-borne disease risk** from climate suitability for mosquito breeding
- **Water-borne disease risk** from flooding and stagnation patterns

Children-specific weights are applied because children are 1.5–2× more susceptible than adults on most of these axes — higher respiratory rate per kilogram of body mass, less efficient thermoregulation, more hand-to-mouth contact, immature immunity.

The library does not replace clinical assessment. It informs *where* clinical assessment should go first when resources are limited.

## Who it's for

Field teams running community health screening, district health officers prioritising outreach visits, NGOs operating in flood- or heat-prone rural areas, public health researchers studying climate-attributable health burden in children. It assumes you have basic environmental data for the locations you're working in (from monitoring stations, satellite-derived products like NASA POWER or ERA5, or even a weather API). It does not require sensor hardware.

## A note on what this is and isn't

This is not a diagnostic tool. It scores environmental conditions, not individuals. A village with high score doesn't mean the children there are sick; it means the conditions there put them at elevated risk and clinical screening should happen sooner. A village with low score doesn't mean it's safe; it means the climate isn't actively driving up risk right now.

The scoring is also not a substitute for local knowledge. Drainage quality, standing water, building stock, livelihoods — these are inputs we ask for, not things we infer. Field teams who know the geography will know more than the model.

## Installation

Requirements: Python 3.9 or later. If you don't have Python on your machine, the easiest way to get it is by installing [Anaconda](https://www.anaconda.com/download) — it's free and includes Python plus the standard scientific libraries.

Once you have Python, clone the repository and install:

```bash
git clone https://github.com/hirapidlab/comprehensiv-climate-risk-mapper.git
cd comprehensiv-climate-risk-mapper
pip install -e .
```

That installs the library in place. You can now use it from any Python script or Jupyter notebook.

To also install the development dependencies (Jupyter, pandas, pytest — needed if you want to run the example notebook or the unit tests):

```bash
pip install -e ".[dev]"
```

To verify the install worked, run the tests:

```bash
pytest tests/
```

You should see 23 passing tests.

To run the example notebook (the easiest way to see the library in action):

```bash
jupyter notebook notebooks/example_usage.ipynb
```

The notebook scores five fictional villages and walks through how to translate the output into a screening priority list.

## Quick start

```python
from climate_risk.scoring import composite_score

inputs = {
    "aqi": 142,
    "temperature_c": 36.0,
    "humidity_percent": 72,
    "rainfall_7day_mm": 85,
    "rainfall_30day_mm": 340,
    "standing_water": True,
    "drainage_quality": "poor",
}

result = composite_score(inputs)
print(result)
# {
#     "respiratory_risk": 15.0,
#     "heat_risk": 18.0,
#     "vector_borne_risk": 25.0,
#     "water_borne_risk": 10.5,
#     "composite": 68.5,
#     "heat_index_c": 44.2,
# }
```

The notebook in `notebooks/example_usage.ipynb` walks through scoring a small set of fictional villages and showing how field teams would translate the output into a screening priority list.

## What's inside

```
comprehensiv-climate-risk-mapper/
├── README.md                    you are here
├── LICENSE                      Apache 2.0
├── pyproject.toml               package metadata
├── CONTRIBUTING.md              how to contribute
├── .gitignore
├── src/climate_risk/
│   ├── __init__.py
│   ├── inputs.py                input dataclass and validation
│   ├── scoring.py               the four scoring functions and composite
│   └── outputs.py               output formatting helpers
├── notebooks/
│   └── example_usage.ipynb      walkthrough on five fictional villages
├── data/
│   ├── README.md
│   └── sample_villages.csv      example inputs for five locations
├── docs/
│   ├── methodology.md           the science behind the scoring
│   ├── references.md            bibliography
│   └── attribution.md           credit and acknowledgments
└── tests/
    └── test_scoring.py          unit tests
```

## Methodology in one paragraph

Each of the four scoring axes maps environmental input ranges to risk levels published by an authoritative source. Air quality follows the WHO Global Air Quality Guidelines (2021) and the US EPA AQI categories. Heat risk uses the Rothfusz heat index (NOAA) with CDC's heat-stress categories. Vector-borne suitability is based on the published climatic envelopes for *Aedes aegypti* (dengue) and *Anopheles* (malaria) mosquito breeding. Water-borne risk follows the conceptual framework from rural stormwater hydrology research — cumulative rainfall, drainage capacity, and surface stagnation as inputs to flood-related disease risk. Children-specific susceptibility weights come from the WHO Children's Environmental Health framework and the *Lancet Countdown on Health and Climate Change* annual reports. Citations are in `docs/methodology.md` and `docs/references.md`.

## Limitations

The scoring is calibrated for South Asian rural contexts (specifically informed by deployment data from Telangana, Bihar, and Andhra Pradesh). The vector-borne sub-score is tuned for *Aedes* and *Anopheles* mosquito biology; it does not cover tick-borne or sandfly-borne diseases. The water-borne sub-score assumes faecal-oral disease transmission as the dominant pathway and does not separately model arsenic, fluoride, or industrial contamination. Heat risk assumes typical rural Indian housing (limited indoor cooling); applying it to populations with reliable air conditioning will overstate risk.

These are real limitations and we'd rather state them up front. Pull requests improving the methodology or extending it to other contexts are welcome.

## License

Apache 2.0. You can use, modify, and distribute this freely, including commercially. See LICENSE for details.

## Attribution

This library was built as part of [Comprehensiv](https://hirapidlab.com), a community health screening platform developed by Hi Rapid Lab Pvt. Ltd. (Hyderabad, India) since 2020. The climate-risk scoring layer was open-sourced in 2026 as Hi Rapid Lab's contribution to the UNICEF Venture Fund's Climate Ventures cohort.

The work draws on the methodology in:
- *WHO Global Air Quality Guidelines*, World Health Organization, 2021
- *CDC Heat-Related Illness Categories*, US Centers for Disease Control and Prevention
- *Lancet Countdown on Health and Climate Change*, annual reports 2020–2025
- *IPCC AR6 Working Group II*, Chapter 7 (Health, Wellbeing, and Changing Structure of Communities), 2022
- *Aedes aegypti and Aedes albopictus climate suitability* — Kraemer et al., *eLife* 2015
- Rural stormwater management methodology used internally by Hi Rapid Lab, adapted from urban hydrology research at Manipal Academy of Higher Education and DHI's MIKE+ documentation

We thank American Leprosy Missions for field collaboration that informed the operational realities the scoring is intended to address, and the Public Health Foundation of India for ongoing institutional support.

## Contact

For questions about methodology or extensions to other contexts: open a GitHub issue, or email the maintainers.

Hi Rapid Lab Pvt. Ltd.
suresh@hirapidlab.com
hirapidlab.com
