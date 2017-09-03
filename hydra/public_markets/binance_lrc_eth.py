# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._binance import Binance

class Binance_LRC_ETH(Binance):
    def __init__(self):
        super().__init__("ETH", "LRC", "LRCETH")

