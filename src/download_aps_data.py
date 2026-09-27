"""Download Stage-0 inputs from the official APS interfaces at run time."""
from __future__ import annotations
import json, time, urllib.request
from pathlib import Path

UI_URL = "https://ops.aps.anl.gov/pvDataReview/"
CONFIG_URL = UI_URL + "config.js"
API_BASE = "https://ops.aps.anl.gov/cgi-bin/pvDataReviewAPI.cgi/api/v1"
HEADERS = {"Accept": "application/json", "X-PVDR-Client-App": "browser"}

def _request(url, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    headers = dict(HEADERS)
    if body is not None: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers,
                                 method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=180) as response:
        content = response.read()
        return json.loads(content) if "json" in response.headers.get("Content-Type", "") else content.decode("utf-8", "replace")

def _run_job(payload):
    status = _request(API_BASE + "/trends/plots", payload)
    job_id = status["job_id"]
    while status["state"] not in {"succeeded", "failed", "cancelled"}:
        time.sleep(0.75)
        status = _request(API_BASE + f"/jobs/{job_id}")
    if status["state"] != "succeeded": raise RuntimeError(json.dumps(status))
    return _request(API_BASE + f"/jobs/{job_id}/result")

def download(config, event_config, raw_dir: Path):
    raw_dir.mkdir(parents=True, exist_ok=True)
    # config.js is saved as provenance and confirms the API base used by the official browser UI.
    ui_config = _request(CONFIG_URL)
    if "/cgi-bin/pvDataReviewAPI.cgi/api/v1" not in ui_config:
        raise RuntimeError("Official APS UI no longer advertises the expected API base; review before continuing.")
    payload = {"time_range": {"start": config["start_utc"], "end": config["end_utc"],
               "display_timezone": config["display_timezone"]}, "pv_names": config["pvs"],
               "x_pv": None, "source": "data-logger", "disable_compaction": config["disable_compaction"],
               "condition": "", "machine_filter": ""}
    result = _run_job(payload)
    fill_html = _request(event_config["source_url"])
    (raw_dir / "pv_response.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (raw_dir / "fill_list.html").write_text(fill_html, encoding="utf-8")
    (raw_dir / "provenance.json").write_text(json.dumps({"official_ui": UI_URL, "official_ui_config": CONFIG_URL,
        "api_base_verified_from_ui": API_BASE, "fill_list": event_config["source_url"], "request": payload}, indent=2), encoding="utf-8")
    return result, fill_html

