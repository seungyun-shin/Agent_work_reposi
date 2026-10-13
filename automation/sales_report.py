#!/usr/bin/env python3
"""Gumroad 판매 현황을 조회해 metrics.csv에 하루 한 줄씩 기록한다.

환경변수 GUMROAD_ACCESS_TOKEN 이 필요하다 (Gumroad → Settings → Advanced →
Applications 에서 발급). 토큰이 없으면 아무것도 기록하지 않고 그 사실만 출력한다.
수치를 추정하거나 지어내지 않는다.
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API = "https://api.gumroad.com/v2"
METRICS = Path(__file__).resolve().parent / "metrics.csv"
KST = timezone(timedelta(hours=9))


def get(path, **params):
    params["access_token"] = os.environ["GUMROAD_ACCESS_TOKEN"]
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    if not data.get("success"):
        raise RuntimeError(f"Gumroad API 실패: {data}")
    return data


def main():
    if not os.environ.get("GUMROAD_ACCESS_TOKEN"):
        print("GUMROAD_ACCESS_TOKEN 없음 — 판매 조회를 건너뜁니다.")
        return 0

    products = get("products")["products"]
    total_sales = sum(p.get("sales_count", 0) for p in products)
    total_usd = sum(p.get("sales_usd_cents", 0) for p in products) / 100

    today = datetime.now(KST).date()
    recent = get("sales", after=(today - timedelta(days=1)).isoformat()).get("sales", [])

    print(f"누적 판매 {total_sales}건 / 누적 매출 ${total_usd:,.2f} / 최근 24시간 {len(recent)}건")
    for p in products:
        print(f"  - {p['name']}: {p.get('sales_count', 0)}건, {p.get('formatted_price', '')}, published={p.get('published')}")

    new = not METRICS.exists()
    rows = [] if new else list(csv.DictReader(METRICS.open(encoding="utf-8")))
    rows = [r for r in rows if r["date"] != today.isoformat()]
    rows.append({"date": today.isoformat(), "total_sales": total_sales,
                 "total_usd": f"{total_usd:.2f}", "sales_last_24h": len(recent)})
    with METRICS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "total_sales", "total_usd", "sales_last_24h"])
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
