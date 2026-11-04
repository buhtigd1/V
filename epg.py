#!/usr/bin/env python3

import re
import requests
import logging

URL = "https://vision.mikrofast.web.id/epg.xml"
OUTPUT_XML = "epg.xml"
LOG_FILE = "epg.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

try:
    logging.info("Starting EPG download")

    response = requests.get(URL, timeout=120)
    response.raise_for_status()

    xml_text = response.text

    #
    # Convert:
    # <channel id="00000000000000000044">
    # to:
    # <channel id="44">
    #
    xml_text = re.sub(
        r'(<channel\b[^>]*\bid=")0+(\d+)(")',
        r'\1\2\3',
        xml_text,
        flags=re.IGNORECASE
    )

    #
    # Convert:
    # <programme channel="00000000000000000044">
    # to:
    # <programme channel="44">
    #
    xml_text = re.sub(
        r'(<programme\b[^>]*\bchannel=")0+(\d+)(")',
        r'\1\2\3',
        xml_text,
        flags=re.IGNORECASE
    )

    #
    # Normalize possible zero-only values
    #
    xml_text = re.sub(
        r'(<channel\b[^>]*\bid=")0+(")',
        r'\g<1>0\2',
        xml_text,
        flags=re.IGNORECASE
    )

    xml_text = re.sub(
        r'(<programme\b[^>]*\bchannel=")0+(")',
        r'\g<1>0\2',
        xml_text,
        flags=re.IGNORECASE
    )

    with open(OUTPUT_XML, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml_text)

    logging.info(
        "SUCCESS: epg.xml updated (%d bytes)",
        len(xml_text.encode("utf-8"))
    )

    print("SUCCESS")

except Exception as e:
    logging.exception("FAILED")
    print(f"ERROR: {e}")
    raise
