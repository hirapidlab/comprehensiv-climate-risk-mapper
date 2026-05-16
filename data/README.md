# Sample data

`sample_villages.csv` contains environmental inputs for five fictional villages, designed to illustrate the range of scoring outcomes the library produces.

These are not real villages. The names and numbers are illustrative. If you want to use the library on real data, you can either replace the file with your own CSV (same columns) or build `LocationInputs` objects directly in code from your data source.

The five villages span the scoring range:

| Village | Composite range expected | Why |
|---------|-------------------------|-----|
| Anandpur | low | Moderate AQI, comfortable temperature, no standing water |
| Bishnupur | medium-high | Polluted air, hot, humid, standing water present |
| Chandkhera | low-medium | Slightly elevated AQI, decent drainage, no standing water |
| Devripura | high | Very polluted, extreme heat, heavy recent rainfall, standing water, poor drainage |
| Eklavyapur | low | Moderate conditions across the board |
