from __future__ import annotations
def summarize(rows, qa, events, aligned, reference):
    current={"raw_rows":len(rows),"successful_pvs":len(qa),"events":len(events),"aligned_rows":len(aligned),
             "median_intervals_seconds_by_pv":{q["pv_identifier"]:q["median_interval_seconds"] for q in qa}}
    comparisons={k:{"current":current.get(k),"reference":reference.get(k),"matches":current.get(k)==reference.get(k)}
                 for k in ["raw_rows","successful_pvs","events","aligned_rows"]}
    return {"current":current,"reference_comparison":comparisons,
            "interpretation":"Counts are pipeline QA, not independent scientific sample sizes. Events are operational labels, not causal interventions."}

