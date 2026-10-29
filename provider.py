import re
import requests
from datetime import datetime

SOURCE_URL = "https://vision.mikrofast.web.id/m3u"
EPG_URL = "https://vision.mikrofast.web.id/epg.xml"

OUTPUT_M3U = "v.m3u"
OUTPUT_LOG = "v.log"


def clean_html(text):
    # Ubah hyperlink HTML menjadi URL murni
    text = re.sub(
        r'<a[^>]*href="([^"]+)"[^>]*>.*?</a>',
        r'\1',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Hapus tag HTML lainnya
    text = re.sub(r'<[^>]+>', '', text)

    return text


try:
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()

    content = r.content.decode("utf-8", errors="ignore")

    # Bersihkan HTML
    content = clean_html(content)

    lines = content.splitlines()

    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Hapus metadata Kodi
        if line.startswith("#KODIPROP:"):
            continue

        cleaned.append(line)

    # Header EPG
    epg_header = f'#EXTM3U url-tvg="{EPG_URL}"'

    if cleaned and cleaned[0].startswith("#EXTM3U"):
        cleaned[0] = epg_header
    else:
        cleaned.insert(0, epg_header)

    final_content = "\n".join(cleaned)

    with open(OUTPUT_M3U, "w", encoding="utf-8", newline="\n") as f:
        f.write(final_content)

    channel_count = final_content.count("#EXTINF")

    log = f"""
Time        : {datetime.now()}
Source      : {SOURCE_URL}
EPG         : {EPG_URL}
Status      : {r.status_code}
Channels    : {channel_count}
Size        : {len(final_content.encode('utf-8'))}
Output      : {OUTPUT_M3U}
Result      : SUCCESS
"""

    with open(OUTPUT_LOG, "a", encoding="utf-8") as f:
        f.write(log + "\n")

    print(log)

except Exception as e:

    log = f"""
Time        : {datetime.now()}
Source      : {SOURCE_URL}
Result      : FAILED
Error       : {e}
"""

    with open(OUTPUT_LOG, "a", encoding="utf-8") as f:
        f.write(log + "\n")

    print(log)
