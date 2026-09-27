from __future__ import annotations
import csv, statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

def _iso(epoch): return datetime.fromtimestamp(float(epoch), timezone.utc).isoformat().replace("+00:00", "Z")

def build(result, processed_dir: Path):
    processed_dir.mkdir(parents=True, exist_ok=True); rows=[]; qa=[]
    for trace in result.get("traces", []):
        times=[float(x) for x in trace.get("x", [])]; values=trace.get("y", [])
        for epoch,value in zip(times,values): rows.append({"timestamp_utc":_iso(epoch),"timestamp_epoch_seconds":repr(epoch),
            "pv_identifier":trace["name"],"value":value,"units":trace.get("units", ""),"source":"APS PV Data Review / data-logger"})
        d=[b-a for a,b in zip(times,times[1:])]; med=statistics.median(d) if d else None
        qa.append({"pv_identifier":trace["name"],"samples":len(times),"first_timestamp_utc":_iso(times[0]) if times else "",
            "last_timestamp_utc":_iso(times[-1]) if times else "","median_interval_seconds":med,
            "minimum_interval_seconds":min(d) if d else "","maximum_interval_seconds":max(d) if d else "",
            "duplicate_timestamps":sum(v-1 for v in Counter(times).values() if v>1),
            "gaps_over_1_5x_median":sum(x>med*1.5 for x in d) if med else 0,"null_values":sum(v is None for v in values)})
    rows.sort(key=lambda r:(float(r["timestamp_epoch_seconds"]),r["pv_identifier"]))
    for name,data in [("raw_sample.csv",rows),("signal_qa.csv",qa)]:
        if data:
            with (processed_dir/name).open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    return rows,qa

