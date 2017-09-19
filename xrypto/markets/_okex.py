# Copyright (C) 2017, Philsong <songbohr@gmail.com>

import config
from .market import Market
from exchanges.okcoin.OkcoinFutureAPI import OKCoinFuture

class OKEx(Market):
    def __init__(self, base_currency, market_currency, pair_code, contract_type):
        super().__init__(base_currency, market_currency, pair_code, 0.0003)
        self.contract_type = contract_type
        self.client = OKCoinFuture(None, None)

        self.event = 'okex_depth'
        self.subscribe_depth()

    def update_depth(self):
        raw_depth = self.client.future_depth(symbol=self.pair_code, contractType = self.contract_type)
        self.depth = self.format_depth(raw_depth)
