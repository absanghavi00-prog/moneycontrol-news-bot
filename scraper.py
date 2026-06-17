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

    "fraud":"Regulatory",

    "default":"Credit Event",

    "bankruptcy":"Credit Event",

    "exclusive":"Exclusive",

    "sources":"Exclusive"

}
