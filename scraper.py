import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://www.moneycontrol.com/news/business/stocks/"

TOPIC = "akshit-moneycontrol-stocks"

SEEN_FILE = "seen.csv"


# Things to ignore

IGNORE = [

    "buy",

    "sell",

    "hold",

    "brokerage",

    "target",

    "target price",

    "price target",

    "share price",

    "stock price",

    "technical",

    "technical view",

    "market wrap",

    "stocks to watch",

    "top gainers",

    "top losers",

    "buzzing stocks",

    "opening bell",

    "closing bell",

    "trading idea",

    "analyst",

    "upgrade",

    "downgrade",

    "jumps",

    "surges",

    "slips",

    "falls",

    "rallies",

    "in charts"

]


# News categories

IMPORTANT = {

    "acquire":"M&A",

    "acquires":"M&A",

    "merger":"M&A",

    "merges":"M&A",

    "stake":"Stake Change",

    "promoter":"Promoter",

    "order":"Order Win",

    "contract":"Order Win",

    "approval":"Approval",

    "fda":"FDA",

    "ceo":"Management",

    "cfo":"Management",

    "resigns":"Management",

    "buyback":"Corporate Action",

    "dividend":"Corporate Action",

    "block deal":"Block Deal",

    "bulk deal":"Bulk Deal",

    "raid":"Regulatory",

    "fraud":"Regulatory",

    "ed":"Regulatory",

    "cbi":"Regulatory",

    "sebi":"Regulatory",

    "default":"Credit Event",

    "bankruptcy":"Credit Event",

    "exclusive":"Exclusive",

    "sources":"Exclusive"

}


# Read old links

if os.path.exists(SEEN_FILE):

    df = pd.read_csv(SEEN_FILE)

    seen = set(df["link"])

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


for a in soup.find_all(

    "a",

    href=True

):

    href = a["href"]

    title = a.get_text(

        strip=True

    )

    t = title.lower()


    # Only stocks page articles

    if "/news/business/stocks/" not in href:

        continue


    if len(title) < 25:

        continue


    if href in seen:

        continue


    # Ignore junk

    if any(

        x in t

        for x in IGNORE

    ):

        continue


    category = None

    score = 0


    for word, cat in IMPORTANT.items():

        if word in t:

            category = cat

            score += 1


    # Ignore if no important keyword

    if score == 0:

        continue


    # Extra filtering

    if score == 1 and category in [

        "Corporate Action"

    ]:

        continue


    if category == "Exclusive":

        prefix = "🚨 EXCLUSIVE"

    elif score >= 2:

        prefix = "🔥 HIGH IMPACT"

    else:

        prefix = "⭐ IMPORTANT"


    msg = f"""

{prefix}

Category: {category}

{title}

{href}

"""


    requests.post(

        f"https://ntfy.sh/{TOPIC}",

        data=msg.encode(

            "utf-8"

        )

    )


    print(title)


    new_seen.add(href)


# Save seen links

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
