"""A script used to create mocks of binance API"""

from typing import Iterator
import cryptools.visualisation as vs


class kline_mock(Iterator):
    """
    This class is aimed to mock the get_ticker function of binance API from a kline call

    input :
        - data : raw data from client.get_historical_klines

    object :
        - iterator that returns the equivalent of get_ticker() in OHLC format

    usage :

        To retreive open prices :

        >>> for tick in kline_mock(data):
        >>>     print(tick[1]["Open"])

    """

    def __init__(self, data):
        self.df = vs.organnise_data(data)
        self.iter = self.df.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()


if __name__ == "__main__":

    # usage exemple
    import json
    import cryptools.visualisation as vs

    with open(".\data\\btc_data.json") as file:
        data = json.load(file)

    for tick in kline_mock(data):
        print(tick[1]["Open"])
