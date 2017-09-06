# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._binance import Binance

class Binance_WTC_BTC(Binance):
    def __init__(self):
        super().__init__("BTC", "WTC", "WTCBTC")

if __name__ == "__main__":
    market = Binance_WTC_BTC()
    print(market.get_ticker())
