import os
import time
import feedparser
import urllib.parse
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = os.environ["ADMIN_ID"]

SOURCES = [
    "https://feeds.bbci.co.uk/persian/rss.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml"
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": ADMIN_ID,
        "text": text,
        "disable_web_page_preview": True
    }).encode()

    request = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()

def main():
    for source in SOURCES:
        feed = feedparser.parse(source)

        for item in feed.entries[:3]:
            title = item.get("title", "بدون عنوان")
            link = item.get("link", "")

            message = (
                "🌐 نبض جهان\n\n"
                f"📰 {title}\n\n"
                f"🔗 منبع خبر:\n{link}\n\n"
                "برای بررسی و تأیید انتشار"
            )

            try:
                send_message(message)
                time.sleep(2)
            except Exception as error:
                 print("Error:", error)
                if hasattr(error, "read"):
                 print("Details:", error.read().decode("utf-8"))
                    
if __name__ == "__main__":
    main()
