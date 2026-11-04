#!/usr/bin/env python3

import re
import gzip
import shutil
import requests
import logging

URL = "https://raw.githubusercontent.com/didikc/EPG-2/main/epg/id-visionplus.xml"
OUTPUT_XML = "epg.xml"
OUTPUT_GZ = "epg.xml.gz"
LOG_FILE = "epg.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

try:
    logging.info("Downloading EPG")

    response = requests.get(
        URL,
        timeout=300,
        headers={
            "User-Agent": "EPG-Updater/1.0"
        }
    )

    response.raise_for_status()

    xml_text = response.content.decode("utf-8", errors="replace")

    before_channels = len(
        re.findall(
            r'<channel\b[^>]*\bid="[^"]+"',
            xml_text,
            flags=re.IGNORECASE
        )
    )

    xml_text = re.sub(
        r'(<channel\b[^>]*\bid=")0+(\d+)(")',
        lambda m: f'{m.group(1)}{int(m.group(2))}{m.group(3)}',
        xml_text,
        flags=re.IGNORECASE
    )

    xml_text = re.sub(
        r'(<programme\b[^>]*\bchannel=")0+(\d+)(")',
        lambda m: f'{m.group(1)}{int(m.group(2))}{m.group(3)}',
        xml_text,
        flags=re.IGNORECASE
    )

    after_channels = len(
        re.findall(
            r'<channel\b[^>]*\bid="[^"]+"',
            xml_text,
            flags=re.IGNORECASE
        )
    )

    unique_channels = sorted(
        {
            int(x)
            for x in re.findall(
                r'<channel\b[^>]*\bid="(\d+)"',
                xml_text,
                flags=re.IGNORECASE
            )
        }
    )

    with open(OUTPUT_XML, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml_text)

    # buat epg.xml.gz
    with open(OUTPUT_XML, "rb") as f_in:
        with gzip.open(OUTPUT_GZ, "wb", compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)

    logging.info("Channels before : %s", before_channels)
    logging.info("Channels after  : %s", after_channels)
    logging.info("Unique channels : %s", len(unique_channels))
    logging.info("Highest channel : %s", max(unique_channels))
    logging.info("Created gzip    : %s", OUTPUT_GZ)

    print(f"Channels : {len(unique_channels)}")
    print(f"Highest  : {max(unique_channels)}")
    print(f"GZip     : {OUTPUT_GZ}")

    if before_channels != after_channels:
        raise Exception(
            f"Channel count mismatch ({before_channels} -> {after_channels})"
        )

except Exception as e:
    logging.exception("FAILED")
    raise
