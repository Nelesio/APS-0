from __future__ import annotations
import csv, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROW = re.compile(r"^#\s*(\d+)\s+(\d\d/\d\d)\s+(\d\d:\d\d)\s+To\s+(\d\d/\d\d)\s+(\d\d:\d\d).*?\|\s*(.*?)\s*\|\s*([0-9.]+)", re.M)

def reconstruct_events(html, cfg):
    wanted=set(cfg["fill_numbers"]); zone=ZoneInfo(cfg["assumed_timezone"]); events=[]
    for m in ROW.finditer(html):
        fill=int(m.group(1))
        if fill not in wanted: continue
        end_local=datetime.strptime(f'{cfg["year"]}/{m.group(4)} {m.group(5)}','%Y/%m/%d %H:%M').replace(tzinfo=zone)
        desc=m.group(6).strip(); label=""
        lm=re.search(r"\[([^\]]+)\]\s*$",desc)
        if lm: label=lm.group(1); desc=desc[:lm.start()].strip()
        events.append({"event_id":f'APS{str(cfg["year"])[2:]}_{fill:02d}',"fill_number":fill,
            "event_timestamp_local_assumed":end_local.isoformat(),"event_timestamp_utc_derived":end_local.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00","Z"),
            "description":desc,"subsystem_label":label,"downtime_hours":m.group(7),"timezone_status":cfg["timezone_status"],
            "source_url":cfg["source_url"],"scientific_status":"Operational label; not a causal intervention label"})
    if set(e["fill_number"] for e in events)!=wanted: raise RuntimeError("Could not reconstruct all configured fills from official list")
    return events

def align(rows,events,cfg,processed_dir:Path):
    aligned=[]; window=cfg["alignment_window_seconds"]
    for e in events:
        et=datetime.fromisoformat(e["event_timestamp_utc_derived"].replace("Z","+00:00")).timestamp()
        for r in rows:
            rel=float(r["timestamp_epoch_seconds"])-et
            if -window<=rel<=window: aligned.append({"event_id":e["event_id"],"event_timestamp_utc_derived":e["event_timestamp_utc_derived"],
                "event_description":e["description"],"event_subsystem_label":e["subsystem_label"],"sample_timestamp_utc":r["timestamp_utc"],
                "relative_time_seconds":f"{rel:.6f}","pre_event_predictor_eligible":str(rel<0).lower(),"pv_identifier":r["pv_identifier"],"value":r["value"],"units":r["units"]})
    for name,data in [("events.csv",events),("event_aligned.csv",aligned)]:
        if data:
            with (processed_dir/name).open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    return aligned

