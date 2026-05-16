# Contributing

The library is small and we'd like to keep it small. Useful contributions:

- Threshold corrections backed by published evidence (with a citation we can read)
- Extensions to new geographies — vector-borne sub-score for *Anopheles stephensi* in urban contexts, for example, or recalibration of rainfall thresholds for monsoon vs non-monsoon climates
- Better test coverage, especially for edge cases at sub-score boundaries
- Documentation improvements that make the methodology more accessible to non-epidemiologists
- Integration helpers — readers for common climate-data formats (NetCDF, GeoTIFF), simple CLI wrappers

Less useful:

- Architectural rewrites that add abstraction without adding capability
- ML-based scoring overlays that obscure what the scoring is actually doing
- Web service / API layers (this is a library; deployment patterns are downstream)

## Process

Open an issue first if you're proposing anything substantive — it saves both of us time. For small fixes, a PR with a clear commit message and an updated or new test is fine.

If your change touches the scoring thresholds or the children-specific weights, please include the citation that backs the new value, and update `docs/methodology.md` to reflect the change.

## Code style

Python 3.9+. Type hints where they help readability. Docstrings on public functions explaining what the function does, what its parameters mean, and (where relevant) what published source the numbers come from.

We don't enforce a specific formatter, but consistency within a file is appreciated.

## Tests

Run with `pytest` from the repo root after `pip install -e ".[dev]"`.
