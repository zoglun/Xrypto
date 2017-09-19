# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._kkex import KKEX

class KKEX_BCH_BTC(KKEX):
    def __init__(self):
        super().__init__("BTC", "BCH", "BCCBTC")

if __name__ == "__main__":
    market = KKEX_BCH_BTC()
    print(market.get_ticker())