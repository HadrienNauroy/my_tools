"""A script amied to get some data to work on"""

import config
from binance.client import Client
from binance.enums import *
import json

client = Client(config.API_KEY, config.API_SECRET, tld="com")
data = client.get_historical_klines("BTCUSDT", KLINE_INTERVAL_1DAY, "1 jan 2017")
with open("data/btc_data.json", "w") as file:
    json.dump(data, file)
