# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._binance import Binance

class Binance_WTC_ETH(Binance):
    def __init__(self):
        super().__init__("ETH", "WTC", "WTCETH")

