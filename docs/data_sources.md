# Data sources

The APS Data Review landing page is the official public entry point. On 2026-09-27 its `config.js` advertised `/cgi-bin/pvDataReviewAPI.cgi/api/v1`, and `app.js` submitted trend jobs to `/trends/plots`, then polled `/jobs/{id}` and `/jobs/{id}/result`. The pipeline follows that mechanism and records the request and source URLs in ignored provenance output.

Events are reconstructed from the official Run 2023-1 Detailed Fill List. Only the four configured rows and fields required for alignment are generated locally. The source HTML itself stays in ignored `data/raw/`.

