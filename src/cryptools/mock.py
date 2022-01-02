"""A script used to create mocks of binance API"""

from copy import Error
from typing import Iterator
import cryptools.visualisation as vs


class SizeError(Exception):
    def __init__(self, message):
        self.message = message


class kline_mock(Iterator):
    """
    This class is aimed to retreive candle of binance API from a kline call one by one

    input :
        - data : raw data from client.get_historical_klines

    object :
        - iterator that returns a candle in OHLC format

    usage :

        To retreive open prices :

        >>> for tick in kline_mock(data):
        >>>     print(tick["Open"])

    """

    def __init__(self, data):
        self.df = vs.organnise_data(data)
        self.iter = self.df.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()[1]


class klines_mock(Iterator):
    """
    This class is aimed to retreive candles of diffrent binance API from a kline calls one by one

    input :
        - data : raw data from client.get_historical_klines

    object :
        - iterator that returns all candles in OHLC format in a dict

    usage :

        To retreive all open prices :

        >>> for tick in klines_mock(btc=data_btc, eth=data_btc):
        >>>     print(tick["btc"]["Open"], tick["eth"]["Open"])


    """

    def __init__(self, **kwargs):

        # check if all data have same lenght
        first = True
        for key in kwargs.keys():
            if first:
                first = False
                n = len(kwargs[key])

            elif len(kwargs[key]) != n:
                raise SizeError("All kline data should have the same size")

        self.dfs = {key: vs.organnise_data(kwargs[key]) for key in kwargs.keys()}
        self.iters = {key: self.dfs[key].iterrows() for key in kwargs.keys()}
        self.kwargs = kwargs

    def __iter__(self):
        return self

    def __next__(self):
        return {key: self.iters[key].__next__()[1] for key in self.kwargs.keys()}


if __name__ == "__main__":

    # usage exemple
    import json
    import cryptools.visualisation as vs

    with open(".\data\\btc_data.json") as file:
        data = json.load(file)

    for tick in klines_mock(btc=data, eth=data):
        print(tick["btc"]["Open"], tick["eth"]["Open"])
