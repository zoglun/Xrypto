# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._huobi import Huobi

class Huobi_BTC_CNY(Huobi):
    def __init__(self):
        super().__init__("CNY", "BTC", "btc_cny")
