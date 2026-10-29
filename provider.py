import requests
from datetime import datetime

SOURCE_URL = "https://vision.mikrofast.web.id/m3u"
M3U_FILE = "v.m3u"
LOG_FILE = "v.log"

try:
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    with open(M3U_FILE, "wb") as f:
        f.write(response.content)

    content = response.content.decode("utf-8", errors="ignore")
    channel_count = content.count("#EXTINF")

    log_text = f"""
Time        : {datetime.now()}
Source URL  : {SOURCE_URL}
Status Code : {response.status_code}
File        : {M3U_FILE}
Size        : {len(response.content)} bytes
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
