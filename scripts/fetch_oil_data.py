#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "oil.json"

FEEDS = [
    {
        "sym": "WTI",
        "yahoo_symbol": "CL=F",
        "name": "WTI · Texas",
        "venue": "NYMEX",
        "unit": "USD/bbl",
    },
    {
        "sym": "BRENT",
        "yahoo_symbol": "BZ=F",
        "name": "Brent Crude",
        "venue": "ICE",
        "unit": "USD/bbl",
    },
]


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_feed(meta, timestamps, closes, feed_cfg):
    pairs = [(ts, close) for ts, close in zip(timestamps, closes) if close is not None]
    history = [round(float(close), 2) for _, close in pairs[-20:]]
    last = float(meta.get("regularMarketPrice") or pairs[-1][1])
    prev = float(meta.get("previousClose") or meta.get("chartPreviousClose") or last)
    change = last - prev
    pct = (change / prev * 100.0) if prev else 0.0
    as_of = int(meta.get("regularMarketTime") or pairs[-1][0])
    return {
        "sym": feed_cfg["sym"],
        "name": feed_cfg["name"],
        "venue": feed_cfg["venue"],
        "unit": feed_cfg["unit"],
        "sourceSymbol": feed_cfg["yahoo_symbol"],
        "last": round(last, 2),
        "previousClose": round(prev, 2),
        "change": round(change, 2),
        "pct": round(pct, 2),
        "history": history,
        "asOf": as_of,
    }


def main():
    out = {
        "source": "Yahoo Finance chart API",
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "feeds": [],
    }
    for cfg in FEEDS:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{cfg['yahoo_symbol']}?interval=5m&range=1d&includePrePost=false"
        payload = fetch_json(url)
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        timestamps = result.get("timestamp", [])
        closes = result["indicators"]["quote"][0].get("close", [])
        out["feeds"].append(build_feed(meta, timestamps, closes, cfg))
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
