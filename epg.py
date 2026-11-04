#!/usr/bin/env python3

import requests
from datetime import datetime

URL = "https://vision.mikrofast.web.id/epg.xml"
OUT_XML = "epg.xml"
LOG_FILE = "epg.log"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


try:
    r = requests.get(URL, timeout=60)
    r.raise_for_status()

    with open(OUT_XML, "wb") as f:
        f.write(r.content)

    log(
        f"SUCCESS: downloaded {len(r.content)} bytes "
        f"from {URL} -> {OUT_XML}"
    )
    print(f"Saved {OUT_XML}")

except Exception as e:
    log(f"ERROR: {e}")
    print(f"ERROR: {e}")
