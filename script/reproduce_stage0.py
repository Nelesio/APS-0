#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.download_aps_data import download
from src.build_dataset import build
from src.align_events import reconstruct_events,align
from src.quality_checks import summarize

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def main():
    pvs=load(ROOT/"config/pvs.yaml"); ecfg=load(ROOT/"config/events.yaml"); ref=load(ROOT/"results/reference_stage0.json")
    result,html=download(pvs,ecfg,ROOT/"data/raw")
    rows,qa=build(result,ROOT/"data/processed")
    events=reconstruct_events(html,ecfg); aligned=align(rows,events,ecfg,ROOT/"data/processed")
    report=summarize(rows,qa,events,aligned,ref)
    (ROOT/"results/latest_run.json").write_text(json.dumps(report,indent=2,default=str),encoding="utf-8")
    print(json.dumps(report,indent=2,default=str))
if __name__=="__main__": main()

