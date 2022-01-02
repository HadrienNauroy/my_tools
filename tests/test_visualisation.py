"""The script to test visualisation"""

import cryptools.visualisation as vs
import pytest


def test_candle_1():
    with pytest.raises(TypeError):
        vs.candle([[0, 1, 1, 1]])


def test_candle_2():
    with pytest.raises(TypeError):
        vs.candle([0, 1, 1, 1])
