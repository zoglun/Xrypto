# Copyright (C) 2017, Philsong <songbohr@gmail.com>

import logging
import requests
from .market import Market
from lib.kkex_api import Client


class KKEX(Market):
    def __init__(self, base_currency, market_currency, pair_code):
        super().__init__(base_currency, market_currency, pair_code, 0.001)
        self.client = Client(None, None, 'http://118.190.82.40:8019/api/v1')

    def update_depth(self):
        raw_depth = self.client.depth(symbol=self.pair_code)
        self.depth = self.format_depth(raw_depth)

