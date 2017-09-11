# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._kkex import KKEX

class KKEX_ETH_BTC(KKEX):
    def __init__(self):
        super().__init__("BTC", "ETH", "ETHBTC")

if __name__ == "__main__":
    market = KKEX_ETH_BTC()
    print(market.get_ticker())