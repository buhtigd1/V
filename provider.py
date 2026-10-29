import re
import requests
from datetime import datetime

SOURCE_URL = "https://vision.mikrofast.web.id/m3u"
EPG_URL = "https://vision.mikrofast.web.id/epg.xml"

M3U_FILE = "v.m3u"
LOG_FILE = "v.log"


def clean_html(text):
    # Ubah <a href="URL">teks</a> menjadi URL
    text = re.sub(
        r'<a[^>]*href="([^"]+)"[^>]*>.*?</a>',
        r'\1',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Hapus tag HTML lain jika ada
    text = re.sub(
        r'<[^>]+>',
        '',
        text
    )

    return text


try:
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    content = response.content.decode("utf-8", errors="ignore")

    # Bersihkan HTML
    content = clean_html(content)

    lines = content.splitlines()

    epg_header = f'#EXTM3U url-tvg="{EPG_URL}"'

    if lines and lines[0].startswith("#EXTM3U"):
        lines[0] = epg_header
    else:
        lines.insert(0, epg_header)

    final_content = "\n".join(lines)

    with open(M3U_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(final_content)

    channel_count = final_content.count("#EXTINF")

    log_text = f"""
Time        : {datetime.now()}
Source URL  : {SOURCE_URL}
EPG URL     : {EPG_URL}
Status Code : {response.status_code}
File        : {M3U_FILE}
Size        : {len(final_content.encode('utf-8'))} bytes
Channels    : {channel_count}
Result      : SUCCESS
"""

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_text + "\n")

    print(log_text)

except Exception as e:

    log_text = f"""
Time        : {datetime.now()}
Source URL  : {SOURCE_URL}
Result      : FAILED
Error       : {str(e)}
"""

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_text + "\n")

    print(log_text)
