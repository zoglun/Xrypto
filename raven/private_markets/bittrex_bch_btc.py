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
 
    def _buy_limit(self, amount, price):
        """Create a buy limit order"""
        print("buy limit...")
        return
        res = self.trade_client.buy_limit(self.pair_code,
            amount,
            price)
        return res['result']['uuid']

    def _sell_limit(self, amount, price):
        """Create a sell limit order"""
        print("sell limit...")
        return
        res = self.trade_client.sell_limit(self.pair_code,
            amount,
            price)
        return res['result']['uuid']

    def _order_status(self, res):
        print(res)
        resp = {}
        resp['order_id'] = res['OrderUuid']
        resp['amount'] = float(res['Quantity'])
        resp['price'] = float(res['Price'])
        resp['deal_size'] = float(res['Quantity']) - float(res['QuantityRemaining'])
        resp['avg_price'] = float(res['Price'])

        if res['IsOpen']:
            resp['status'] = 'OPEN'
        else:
            resp['status'] = 'CLOSE'

        return resp

    def _get_order(self, order_id):
        res = self.trade_client.get_order(order_id)
        assert str(res['OrderUuid']) == str(order_id)
        return self._order_status(res)


    def _cancel_order(self, order_id):
        res = self.trade_client.cancel(order_id)
        assert str(res['id']) == str(order_id)

        if res['success'] == True:
            return True
        else:
            return False

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
                self.bch_available = float(entry['Available'])
                self.bch_balance = float(entry['Balance'])

            elif currency == 'BTC':
                self.btc_available = float(entry['Available'])
                self.btc_balance = float(entry['Balance'])  

            
        