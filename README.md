# APS Stage-0 reproducibility pipeline

This repository reconstructs a limited APS Stage-0 feasibility study from official Advanced Photon Source interfaces. It downloads inputs at run time and does **not** distribute APS data.

## Quick start

```bash
git clone REPLACE_WITH_PUBLIC_REPOSITORY_URL_AFTER_PUBLICATION
cd aps-stage0-reproducibility
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_stage0.py
```

The run verifies the API path advertised by the official APS Data Review interface, requests six configured PVs over a 36-hour interval, downloads the official 2023-1 fill list, reconstructs fills 9–12, performs signal QA, and aligns observations within ±2 hours of each event. Generated data remain under ignored `data/` directories. `results/latest_run.json` compares current counts with the original Stage-0 reference without forcing agreement.

## Scientific scope

Stage-0 is a feasibility and reproducibility study for acquisition, synchronization, temporal handling, operational-event alignment and basic quality assessment. It is not evidence that an integrated model transfers to a medical accelerator. The APS events are operational fill-termination labels, not a causal dataset of engineering interventions.

## Data availability and licensing

No original APS measurements or downloaded fill-list content are included in version control. The pipeline retrieves them from the official APS interfaces at execution time. The MIT license covers only our code and original documentation; it does not relicense APS data or imply redistribution rights. Users remain responsible for the terms and availability of upstream services.

Official sources:

- APS Accelerator Data Review: https://ops.aps.anl.gov/pvDataReview/
- API base advertised by its `config.js`: `https://ops.aps.anl.gov/cgi-bin/pvDataReviewAPI.cgi/api/v1`
- Run 2023-1 Detailed Fill List: https://ops.aps.anl.gov/statistics/2023/2023-1/fill_list.html

The API is used by the official browser interface, but no long-term stability guarantee has been identified. The script stops if the UI no longer advertises the configured API base.

## Reproducibility limitations

- The fill-list timezone is not explicit. `America/Chicago` is a configurable, reversible assumption.
- PV coverage and historical aliases vary over time.
- Sampling is heterogeneous and gaps can occur.
- Upstream services, historical data, aliases or API behavior may change.
- Row counts are not counts of statistically independent observations.
- Four selected events are insufficient for scientific model validation.
- Operational subsystem labels must not be interpreted as verified root causes or interventions.

See `docs/` for methodology, sources, limitations and the reference results.

