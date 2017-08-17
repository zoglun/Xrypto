# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from .market import Market, TradeException
import config
import logging
from bittrex import bittrex
 
# python3 raven/raven-cli.py -m Bittrex_BCH_BTC get-balance

class PrivateBittrex_BCH_BTC(Market):
    def __init__(self, api_key = None, api_secret = None):
        super().__init__("BTC", "BCH", "BTC-BCC")

        self.trade_client = bittrex.Bittrex(
                    api_key if api_key else config.Bittrex_API_KEY,
                    api_secret if api_secret else config.Bittrex_SECRET_TOKEN)

        self.get_balances()
 
    def _buy(self, amount, price):
        """Create a buy limit order"""
        print("buy limit...")
        return
        res = self.trade_client.buy_limit(self.pair_code,
            amount,
            price)
        return res['result']['uuid']

    def _sell(self, amount, price):
        """Create a sell limit order"""
        print("sell limit...")
        return
        res = self.trade_client.sell_limit(self.pair_code,
            amount,
            price)
        return res['result']['uuid']

    def get_balances(self):
        """Get balance"""
        res = self.trade_client.get_balances()
        # print("get_balances response:", res)

        for entry in res['result']:
            currency = entry['Currency']
            if currency not in (
                    'BTC', 'BCC'):
                continue

            if currency == 'BCC':
                self.bch_available = entry['Available']
                self.bch_balance = entry['Balance']

            elif currency == 'BTC':
                self.btc_available = entry['Available']
                self.btc_balance = entry['Balance']  

            
        