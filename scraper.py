import requests
from bs4 import BeautifulSoup

URL = "https://www.moneycontrol.com/news/business/stocks/"
TOPIC = "akshit-moneycontrol-stocks"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Downloading page...")

r = requests.get(
    URL,
    headers=headers,
    timeout=20
)

print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

count = 0

for a in soup.find_all("a", href=True):

    href = a["href"]

    title = a.get_text(strip=True)

    if len(title) < 30:
        continue

    if "moneycontrol.com" not in href:
        continue

    print(title)

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data=f"{title}\n\n{href}".encode("utf-8")
    )

    count += 1

    # send only first 5 for testing
    if count >= 5:
        break

print("Sent", count, "notifications")
