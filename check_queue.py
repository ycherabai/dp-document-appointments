import asyncio
import os
import sys
import urllib.request
import urllib.parse
import nodriver as uc

URL = "https://berlin.pasport.org.ua/solutions/e-queue"
NO_SLOTS_TEXT = "Наразі всі місця зайняті."

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def notify(message: str):
    params = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message})
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?{params}"
    urllib.request.urlopen(api_url)
    print(f"[NOTIFY] Message sent: {message}")


async def check():
    print(f"Opening {URL} ...")
    browser = await uc.start(headless=False, sandbox=False)
    try:
        page = await browser.get(URL)
        await asyncio.sleep(12)
        content = await page.get_content()
    finally:
        browser.stop()

    if NO_SLOTS_TEXT in content:
        print("All slots are taken. No notification sent.")
        return False
    else:
        print("Slots may be available!")
        notify(f"Slots may be available! Check {URL}")
        return True


if __name__ == "__main__":
    found = asyncio.run(check())
    sys.exit(0 if found else 0)
