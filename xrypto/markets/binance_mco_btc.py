# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._binance import Binance

class Binance_MCO_BTC(Binance):
    def __init__(self):
        super().__init__("BTC", "MCO", "MCOBTC")

