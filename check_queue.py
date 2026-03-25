import os
import sys
import urllib.request
import urllib.parse
from seleniumbase import SB

URL = "https://berlin.pasport.org.ua/solutions/e-queue"
NO_SLOTS_TEXT = "Наразі всі місця зайняті."

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def notify(message: str):
    params = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": "true",
    })
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?{params}"
    urllib.request.urlopen(api_url)
    print(f"[NOTIFY] Message sent: {message}")


def check():
    print(f"Opening {URL} ...")
    with SB(uc=True, headless=True) as sb:
        sb.open(URL)
        sb.sleep(10)
        content = sb.get_page_source()

    if "документ" not in content.lower():
        print("ERROR: Page did not load correctly. HTML response:")
        print(content[:3000])
        raise RuntimeError("Page validation failed: 'документ' not found in response")

    if NO_SLOTS_TEXT in content:
        print("All slots are taken. No notification sent.")
        return False
    else:
        print("Slots may be available!")
        notify(f"Slots may be available! Check {URL}")
        return True


if __name__ == "__main__":
    check()
