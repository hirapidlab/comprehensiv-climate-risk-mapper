# Attribution

## Origin and maintainer

This library was built at Hi Rapid Lab Pvt. Ltd. (Hyderabad, India). It is a small part of a much larger system — [Comprehensiv](https://hirapidlab.com), a community health screening platform deployed by community health workers in rural India since 2019. As of 2026, Comprehensiv has been used to screen more than 500,000 people across three Indian states (Telangana, Bihar, Andhra Pradesh).

The climate-vulnerability scoring layer was open-sourced in 2026 as Hi Rapid Lab's contribution to the UNICEF Venture Fund Climate Ventures cohort. The rest of Comprehensiv — the screening device, the icon-based UI, the clinical AI models, the operations playbook — remains proprietary.

## What we built on

Our methodology stands on the work of others. The published bodies of research we drew from are listed in [references.md](references.md). The two pieces of work that most directly shaped this code:

**WHO Global Air Quality Guidelines (2021) and the US EPA AQI framework.** These give the thresholds we used for respiratory risk. We chose US EPA over WHO for the operational scoring because WHO 2021's PM2.5 annual mean of 5 µg/m³ would flag essentially all of South Asia at the same level, eliminating discrimination between locations.

**Rural stormwater hydrology methodology.** The water-borne risk sub-score draws conceptually from urban flood-modelling research adapted for rural contexts. Our internal work on this borrows from DHI's MIKE+ modelling toolset (used widely for urban flood vulnerability in India, including Chennai and Mumbai municipal projects) and from research on rural flood early-warning systems including work from Guwahati Municipal Corporation and the Assam State Disaster Management Authority.

## Partners who shaped the operational thinking

The threshold choices and the children-specific weights reflect what we have learned from deployment partners who work in the same operational conditions this library targets:

- **American Leprosy Missions (ALM).** Field partnership since 2023. The 402-page bilingual operations manual we co-developed with ALM informed the assumptions we make about what data field teams can realistically collect (e.g., why we accept "drainage_quality" as a categorical input rather than asking for a continuous infiltration rate).

- **Public Health Foundation of India (PHFI).** Hi Rapid Lab is incubated by PHFI, and the Indian Institute of Public Health, Hyderabad (an IIPH-PHFI institution) has been the research home for much of the underlying epidemiology.

- **Malla Reddy Vishwavidyapeeth (MRVV), School of Digital Health.** Dr. Suresh Munuswamy is the founding Dean. Academic infrastructure and student research has informed the methodology.

- **Department of Science and Technology, Government of India (DST).** Earlier-stage R&D support for Comprehensiv platform development.

## The library is not the deployment

This library is one peripheral utility. It does not contain Hi Rapid Lab's clinical screening AI, our multi-sensor handheld device design, our 12-module clinical workflow, or our intervention logic. Those are protected by 25 patents and are proprietary to Hi Rapid Lab Pvt. Ltd.

What this library *does* contain is open knowledge organised into a small, usable Python package. The science behind respiratory, heat, vector, and water-borne risk scoring is public; we have packaged it in a form that NGOs, district health teams, and research groups can pick up and use without rebuilding from scratch.

## How to credit this work

If you use this library in research or in a field deployment, the suggested citation is:

> Hi Rapid Lab Pvt. Ltd. (2026). *Comprehensiv Climate Risk Mapper* (Version 0.1.0) [Software]. Available from github.com/[hrl-organisation]/comprehensiv-climate-risk-mapper. Apache License 2.0.

If your work specifically benefits from extensions or refinements you make, we would be glad to hear about it — open an issue or send an email.

## Contact

Hi Rapid Lab Pvt. Ltd.
Hi Rapid Lab — Indian Institute of Public Health Laboratories
Sy. No. 376, 377, 384, 388-391 & 387
Premavathi Pet, Rajendra Nagar Mandal
Kismatpur, Hyderabad – 500030, Telangana, INDIA

suresh@hirapidlab.com
hirapidlab.com
