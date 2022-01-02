"""The srcipt that contains visualisation tools"""


import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpl
import pandas as pd


def organnise_data(data):
    r"""this function handle the re-organisation of data in a dataframe

    parameters :
        - data : raw data from "client.get_historical_klines(*args), type list

    outputs :
        - data_frame : a panda DataFrame with Open, High, Low and Close columns with a DateTimeIndex


    """

    # tighting up data in a panda frame
    data_frame = pd.DataFrame(data)
    data_frame.columns = [
        "Open Time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close Time",
        "QAV",
        "Number of Trades",
        "TBBV",
        "TBQV",
        "Ignore",
    ]
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "QAV",
        "Number of Trades",
        "TBBV",
        "TBQV",
    ]
    data_frame[numeric_columns] = data_frame[numeric_columns].apply(
        pd.to_numeric, axis=1
    )

    data_frame["Open Time"] = pd.to_datetime(data_frame["Open Time"] / 1000, unit="s")
    data_frame["Close Time"] = pd.to_datetime(data_frame["Close Time"] / 1000, unit="s")
    data_frame.index = pd.DatetimeIndex(data_frame["Open Time"])
    data_frame.set_index("Open Time", inplace=True)

    return data_frame[["Open", "High", "Low", "Close"]]


def _candle_plot(data_df, **kwargs):
    r"""
    Internal function called by candle, handle the ploting part

    parameters :
        - data : raw data from "client.get_historical_klines(\*args), type list
        - \*\*Kwargs : all sort of argument that mpl.plot can accept

    More information here : https://github.com/matplotlib/mplfinance


    """

    style = mpl.make_mpf_style(
        base_mpf_style="charles",
        y_on_right=False,
    )

    kwargs["type"] = "candle"
    kwargs["style"] = style

    mpl.plot(data_df, **kwargs)


def candle(data, **kwargs):
    r"""
    This function is aimed to to plot candle with data from binance klines

    parameters :
        - data : raw data from "client.get_historical_klines(\*args), type list
        - \*\*Kwargs : all sort of argument that mpl.plot can accept

    More information here : https://github.com/matplotlib/mplfinance

    """

    if not type(data) == list:
        raise TypeError("data should be a list")

    if not type(data[0]) == list:
        raise TypeError("data should have two dimension")

    if not len(data[0]) == 12:
        raise TypeError("Some data are missing")

    data_df = organnise_data(data)
    _candle_plot(data_df, **kwargs)


if __name__ == "__main__":

    import json

    with open("data/btc_data.json", "r") as file:
        data = json.load(file)

    candle(data[-40:], title="BTC/USDT")
