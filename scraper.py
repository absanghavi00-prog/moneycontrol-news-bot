import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://www.moneycontrol.com/rss/business.xml"
TOPIC = "akshit-moneycontrol-stocks"

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

IMPORTANT = {

    "acquire":"M&A",
    "acquires":"M&A",
    "merger":"M&A",
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

print("Downloading RSS...")

r = requests.get(RSS_URL, timeout=20)

print("Status:", r.status_code)

root = ET.fromstring(r.content)

count = 0

for item in root.findall(".//item"):

    title = item.findtext("title", "")

    link = item.findtext("link", "")

    t = title.lower()

    if any(x in t for x in IGNORE):
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

Category: {category}

{title}

{link}

"""

    requests.post(

        f"https://ntfy.sh/{TOPIC}",

        data=msg.encode("utf-8")

    )

    print(title)

    count += 1

print("Sent", count, "notifications")
