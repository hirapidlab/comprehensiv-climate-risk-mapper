# Methodology

This document explains how the four sub-scores work, what published evidence each one is grounded in, and what choices we made along the way. We've tried to be honest about the limitations as much as the strengths — anyone using these scores should understand both.

## The four sub-scores

The composite is the sum of four sub-scores, each on a 0-25 scale, totalling 0-100. They are independent: a location can score high on heat and low on water, or vice versa. The composite gives a single number for ranking; the sub-scores tell you *why* a location ranks where it does.

We deliberately do not weight the four axes. A village with extreme heat but no flooding is not categorically less risky than a village with the inverse — they're risky in different ways, and the screening team needs to know which. Combining them into a single weighted index would erase that signal.

## Respiratory risk (AQI)

The thresholds follow the US EPA Air Quality Index categories (Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Hazardous). The choice of US EPA over WHO 2021 is pragmatic: the WHO 2021 PM2.5 annual guideline of 5 µg/m³ would put nearly all of South Asia in the "exceeded" category, which makes the score uninformative for prioritisation between locations. The US EPA AQI gives more discrimination across the range we typically see in rural India.

Children carry a higher risk multiplier (default 1.5×) for three reasons documented in the *Lancet Countdown* series: their respiratory rate per kilogram of body mass is roughly twice an adult's, their lungs are still developing and more susceptible to lasting damage, and they spend more time outdoors during peak exposure hours in many rural settings.

Reference points:
- US EPA AQI Technical Assistance Document (2018)
- WHO Global Air Quality Guidelines (2021)
- Watts N et al., *The 2020 Report of The Lancet Countdown*, Lancet (2021)
- Schwartz J, "Air pollution and children's health", Pediatrics (2004)

## Heat risk (heat index)

We use the Rothfusz heat index (NOAA's standard) calculated in Fahrenheit and converted to Celsius for output. Below 80°F (about 27°C) the heat index is essentially the dry-bulb temperature, so we return that directly. Above 80°F the regression captures the additional physiological stress humidity adds — high humidity prevents evaporative cooling.

The CDC's heat-stress categories define caution (above 27°C heat index), extreme caution (above 32°C), danger (above 39°C), and extreme danger (above 51°C). The scoring maps these categories to 0-25.

Children carry the same 1.5× weight as for respiratory risk. The reasons are different though: children's body surface to mass ratio is higher than adults', so they gain heat faster. Their sweating response is less developed in younger children. They also depend on adults to recognise when they need fluids and shade. Tan J et al. (2007) showed paediatric admissions during heatwaves are disproportionately higher than the adult share of the population.

Reference points:
- Rothfusz LP, *NOAA Technical Attachment SR 90-23* (1990)
- CDC, *Climate Effects on Health* — heat-related illness
- Tan J et al., "The urban heat island and its impact on heat waves and human health in Shanghai", *International Journal of Biometeorology* (2007)

## Vector-borne disease climate suitability

We score for two of the most epidemiologically significant mosquito-borne disease vectors in South Asia: *Aedes aegypti* (dengue, chikungunya, zika) and *Anopheles* species (malaria). The scoring is a coarse climate-suitability proxy — not a transmission risk model.

Without standing water, mosquito breeding is limited regardless of climate. We give a small baseline score (5) when the climate is suitable but no standing water has been reported, since the absence of standing water in survey conditions doesn't mean there's none nearby. When standing water is present, temperature and humidity drive the score, weighted toward the optimal breeding window for *Aedes aegypti* (25-30°C, RH > 70%).

The scoring is climate-side only. It does not incorporate population susceptibility (no vaccination coverage data, no prior exposure rates), and it does not model spatial mosquito flight range. A village scoring 25 on this axis has conditions favourable to transmission *if* an introduced case occurs — not a guarantee that transmission will occur.

Reference points:
- Kraemer MUG et al., "The global distribution of the arbovirus vectors *Aedes aegypti* and *Ae. albopictus*", *eLife* (2015)
- Mordecai EA et al., "Thermal biology of mosquito-borne disease", *Ecology Letters* (2019)
- Bhatt S et al., "The global distribution and burden of dengue", *Nature* (2013)

## Water-borne disease risk (flooding and stagnation)

This sub-score uses recent and cumulative rainfall as proxies for flood-related and stagnation-related water-borne disease risk. Heavy rainfall in the past 7 days corresponds to acute flood risk — sanitation systems overwhelmed, faecal contamination of drinking water sources, increased gastrointestinal disease incidence. Sustained rainfall over 30 days corresponds to chronic stagnation — standing water in low-lying areas, water table contamination, prolonged exposure.

Drainage quality moderates both. Good drainage attenuates the score to 40% of the raw value; moderate drainage to 70%; poor drainage applies the full weight. The default if not specified is "poor" because most rural Indian deployment contexts the library was designed for have inadequate drainage as the baseline assumption.

The conceptual framework draws on rural stormwater hydrology research adapted from urban methodology — including the work informed by DHI's MIKE+ modelling toolset for flood-vulnerability mapping. The numerical thresholds (50 mm / 100 mm / 200 mm for 7-day rainfall, 250 mm / 500 mm for 30-day) are calibrated to South Asian monsoon ranges and would need recalibration for other climates.

Children under 5 carry the largest share of diarrhoeal disease mortality globally (Liu L et al., 2016). The post-flood window — the first 14 days after a flood event — is when paediatric diarrhoeal admissions spike most sharply.

Reference points:
- Liu L et al., "Global, regional, and national causes of under-5 mortality in 2000-15", *Lancet* (2016)
- Levy K et al., "Climate Change Impacts on Waterborne Diseases: Moving Toward Designing Interventions", *Current Environmental Health Reports* (2018)
- WHO, *Guidelines for Drinking-water Quality* (4th edition, 2022)
- Ahern M et al., "Global Health Impacts of Floods: Epidemiologic Evidence", *Epidemiologic Reviews* (2005)

## Children-specific weighting (the 1.5× multiplier)

We default to 1.5× for respiratory and heat. This is a conservative midpoint of the range in the *Lancet Countdown* and IPCC AR6 chapters on health and climate. Some studies use higher multipliers (2× for severe air pollution exposure in under-5s), others lower. We chose 1.5 to be defensible across the published range rather than aggressive at one end.

The multiplier is a parameter — users can pass a different value if they have local epidemiological data justifying it. The function signatures all accept `child_weight` as a keyword argument.

Reference for the weighting choice:
- IPCC AR6 Working Group II, Chapter 7 (Health, Wellbeing and the Changing Structure of Communities), 2022
- Watts N et al., *Lancet Countdown* 2020 and 2023 reports
- WHO, *Don't Pollute My Future! The Impact of the Environment on Children's Health* (2017)

## What this library is not

It is not a climate model — we don't project future risk; the scoring is for current observed conditions. It is not a disease incidence model — we don't predict how many children will get sick. It is not a clinical decision tool — the output is a screening prioritisation aid, not a medical assessment. And it does not replace local knowledge — drainage quality and standing-water reports require someone on the ground to provide them honestly.

If you find a place the scoring gets wrong, open an issue with the inputs and the expected output. That's how the methodology gets better.
