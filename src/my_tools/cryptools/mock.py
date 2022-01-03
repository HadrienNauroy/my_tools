"""A script used to create mocks of binance API"""

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

        >>> for kline in kline_mock(data):
        >>>     print(kline["Open"])

    """

    def __init__(self, data):
        self.df = vs.organnise_data(data)
        self.iter = self.df.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()[1]


class klines_mock(Iterator):
    r"""
    This class is aimed to retreive candles of diffrent binance API from a kline calls one by one

    input :
        - \*\*kwargs : raw data from client.get_historical_klines

    object :
        - iterator that returns all candles in OHLC format in a dict

    usage :

        To retreive all open prices :

        >>> for klines in klines_mock(btc=data_btc, eth=data_btc):
        >>>     print(klines["btc"]["Open"], klines["eth"]["Open"])


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


class tickers_mock(Iterator):
    r"""
    This class is aimed to mock the get_all_tickers() functin of binance
    given a set data from previous call. It arrange data in a dict

    input :
        - data : list data from succesive call of client.get_all_tickers()

    object :
        - iterator that returns all all tickers in a dict one by one

    usage :

        To retreive BTCUSDT price :

        >>> for tick in tickers_mock(data):
        >>>     print(tick["BTCUSDT"])

    """

    def __init__(self, data):
        self.data = data
        self.id = -1
        self.len = len(data)

    def __iter__(self):
        return self

    def __next__(self):

        if self.id < self.len - 1:
            self.id += 1
            tickers = self.data[self.id]
            tickers_dict = {
                tickers[k]["symbol"]: float(tickers[k]["price"])
                for k in range(len(tickers))
            }
            return tickers_dict

        else:
            raise StopIteration


if __name__ == "__main__":

    # usage exemple
    import json

    with open(".\data\\tickers.json") as file:
        data = json.load(file)

    for tick in tickers_mock(data):
        print(tick["BTCUSDT"])
