import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://www.moneycontrol.com/news/business/stocks/"

TOPIC = "akshit-moneycontrol-stocks"

SEEN_FILE = "seen.csv"

IGNORE = [

    "buy",

    "sell",

    "hold",

    "brokerage",

    "target price",

    "stock price",

    "share price",

    "technical",

    "stocks to watch",

    "top gainers",

    "top losers",

    "market wrap",

    "buzzing stocks",

    "opening bell",

    "closing bell"

]

IMPORTANT = {

    "acquire":"M&A",

    "acquires":"M&A",

    "merger":"M&A",

    "stake":"Stake Change",

    "order":"Order Win",

    "contract":"Order Win",

    "approval":"Approval",

    "fda":"FDA",

    "ceo":"Management",

    "cfo":"Management",

    "promoter":"Promoter",

    "buyback":"Corporate Action",

    "dividend":"Corporate Action",

    "block deal":"Block Deal",

    "bulk deal":"Bulk Deal",

    "raid":"Regulatory",

    "ed":"Regulatory",

    "cbi":"Regulatory",

    "fraud":"Regulatory",

    "default":"Credit Event",

    "bankruptcy":"Credit Event",

    "exclusive":"Exclusive"

}


if os.path.exists(SEEN_FILE):

    seen = set(pd.read_csv(SEEN_FILE)["link"])

else:

    seen = set()


headers = {

    "User-Agent":

    "Mozilla/5.0"

}


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

for a in soup.find_all("a", href=True):

    href = a["href"]

    title = a.get_text(strip=True)

    title_lower = title.lower()

    if "/news/business/stocks/" not in href:

        continue

    if len(title) < 20:

        continue

    if href in seen:

        continue


    # Remove noise

    if any(

        x in title_lower

        for x in IGNORE

    ):

        continue


    category = None

    score = 0


    for word, cat in IMPORTANT.items():

        if word in title_lower:

            category = cat

            score += 1


    if score == 0:

        continue


    prefix = "🔥 HIGH IMPACT"

    msg = f"""

{prefix}

Category: {category}

{title}

{href}

Score: {score}/10

"""


    requests.post(

        f"https://ntfy.sh/{TOPIC}",

        data=msg.encode("utf-8")

    )


    print(title)

    new_seen.add(href)


pd.DataFrame(

    {

        "link":

        list(new_seen)

    }

).to_csv(

    SEEN_FILE,

    index=False

)


print("Done")
