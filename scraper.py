import requests
import pandas as pd
import os
import xml.etree.ElementTree as ET

TOPIC = "akshit-moneycontrol-stocks"

SEEN_FILE = "seen.csv"

RSS_FEEDS = [

    {
        "source":"Moneycontrol",
        "url":"https://www.moneycontrol.com/rss/business.xml"
    },

    {
        "source":"Mint News",
        "url":"https://www.livemint.com/rss/newsRSS"
    },

    {
        "source":"Mint Companies",
        "url":"https://www.livemint.com/rss/companiesRSS"
    },

    {
        "source":"Mint Markets",
        "url":"https://www.livemint.com/rss/marketsRSS"
    },

    {
        "source":"Reuters",
        "url":"https://news.google.com/rss/search?q=site:reuters.com+when:1d&hl=en-US&gl=US&ceid=US:en"
    }

]


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
    "in charts"

]


IMPORTANT = {

    "exclusive":"Exclusive",
    "sources":"Exclusive",

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

    "block deal":"Block Deal",
    "bulk deal":"Bulk Deal",

    "raid":"Regulatory",
    "fraud":"Regulatory",
    "ed":"Regulatory",
    "cbi":"Regulatory",
    "sebi":"Regulatory",

    "default":"Credit Event",
    "bankruptcy":"Credit Event"

}


# Read seen links

if os.path.exists(SEEN_FILE):

    df = pd.read_csv(SEEN_FILE)

    seen = set(df["link"])

else:

    seen = set()


new_seen = set(seen)

count = 0


for feed in RSS_FEEDS:

    print("\nDownloading", feed["source"])

    try:

        r = requests.get(

            feed["url"],

            timeout=20,

            headers={

                "User-Agent":

                "Mozilla/5.0"

            }

        )

        root = ET.fromstring(r.content)

    except Exception as e:

        print("Failed:", e)

        continue


    for item in root.findall(".//item"):

        title = item.findtext(

            "title",

            ""

        ).strip()

        link = item.findtext(

            "link",

            ""

        ).strip()


        if title == "" or link == "":

            continue


        if link in seen:

            continue


        t = title.lower()


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


        if score == 0:

            continue


        if category == "Exclusive":

            prefix = "🚨 EXCLUSIVE"

        elif score >= 2:

            prefix = "🔥 HIGH IMPACT"

        else:

            prefix = "⭐ IMPORTANT"


        msg = f"""

{prefix}

Source: {feed['source']}

Category: {category}

{title}

{link}

"""


        requests.post(

            f"https://ntfy.sh/{TOPIC}",

            data=msg.encode(

                "utf-8"

            )

        )


        print(

            feed["source"],

            ":",

            title

        )


        new_seen.add(

            link

        )

        count += 1



pd.DataFrame(

    {

        "link":

        list(new_seen)

    }

).to_csv(

    SEEN_FILE,

    index=False

)


print("\nSent", count, "notifications")
