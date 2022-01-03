"""A script amied to get some data to work on"""

import config
from binance.client import Client
from binance.enums import *
import json
import time as tm


client = Client(config.API_KEY, config.API_SECRET, tld="com")
# data = client.get_historical_klines("BTCUSDT", KLINE_INTERVAL_1DAY, "1 jan 2017")
data = []
tic = tm.time()
while tm.time() - tic < 3600:
    data += [client.get_all_tickers()]
    tm.sleep(1)


with open("data/tickers.json", "w") as file:
    json.dump(data, file)
