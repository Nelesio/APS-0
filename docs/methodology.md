# Methodology

The configured UTC interval corresponds to 36 hours from 2023-02-17 00:00 UTC through 2023-02-18 12:00 UTC. Six PVs are requested with compaction disabled. The pipeline preserves timestamps and values, computes per-signal cadence and gap diagnostics, parses fill-termination timestamps for fills 9–12, and aligns samples within ±7200 seconds.

Rows with negative relative time are explicitly marked as eligible pre-event predictors. This flag does not establish that a predictive model is valid; any later study must split by event and time, define controls, and prevent leakage from post-event data.

