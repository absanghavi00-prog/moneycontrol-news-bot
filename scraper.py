import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://www.moneycontrol.com/news/business/stocks/"

TOPIC = "akshit-moneycontrol-stocks"

SEEN_FILE = "seen.csv"

headers = {
    "User-Agent":
    "Mozilla/5.0"
}

# Load seen links

if os.path.exists(SEEN_FILE):

    df = pd.read_csv(SEEN_FILE)

    seen = set(df["link"])

else:

    seen = set()

# Download page

r = requests.get(
    URL,
    headers=headers,
    timeout=20
)

r.raise_for_status()

soup = BeautifulSoup(
    r.text,
    "html.parser"
)

new_seen = set(seen)

# Find all links

for a in soup.find_all("a", href=True):

    href = a["href"]

    title = a.get_text(strip=True)

    if "/news/business/stocks/" not in href:

        continue

    if len(title) < 20:

        continue

    if href in seen:

        continue

    print("NEW:", title)

    msg = f"📰 {title}\n\n{href}"

    requests.post(

        f"https://ntfy.sh/{TOPIC}",

        data=msg.encode("utf-8")

    )

    new_seen.add(href)

# Save seen links

pd.DataFrame({

    "link": list(new_seen)

}).to_csv(

    SEEN_FILE,

    index=False

)

print("Done")
