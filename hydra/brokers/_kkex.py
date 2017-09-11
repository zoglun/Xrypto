# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from .market import Market, TradeException
import config
import logging
from lib.kkex_api import Client

class KKEX(Market):
    def __init__(self, base_currency, market_currency, pair_code, api_key=None, api_secret=None):
        super().__init__(base_currency, market_currency, pair_code)

        self.orders = {}

        self.client = Client(
                    api_key if api_key else config.KKEX_API_KEY,
                    api_secret if api_secret else config.KKEX_SECRET_TOKEN,
                    api_root='http://118.190.82.40:8019/api/v1')
 
    def _buy_limit(self, amount, price):
        """Create a buy limit order"""
        res = self.client.buy_limit(
            symbol=self.pair_code,
            amount=str(amount),
            price=str(price))

        logging.verbose('_buy_limit: %s' % res)

        return res['order_id']

    def _sell_limit(self, amount, price):
        """Create a sell limit order"""
        res = self.client.sell_limit(
            symbol=self.pair_code,
            amount=str(amount),
            price=str(price))
        logging.verbose('_sell_limit: %s' % res)

        return res['order_id']

    def _order_status(self, res):
        resp = {}
        resp['order_id'] = res['order_id']
        resp['amount'] = float(res['amount'])
        resp['price'] = float(res['price'])
        resp['deal_size'] = float(res['deal_amount'])
        resp['avg_price'] = float(res['avg_price'])

        if res['status'] == 0 or res['status'] == 1 or res['status'] == 4:
            resp['status'] = 'OPEN'
        else:
            resp['status'] = 'CLOSE'

        return resp

    def _get_order(self, order_id):
        res = self.client.order_info(self.pair_code, int(order_id))
        logging.verbose('get_order: %s' % res)

        assert str(res['order']['order_id']) == str(order_id)
        return self._order_status(res['order'])

    def _cancel_order(self, order_id):
        res = self.client.cancel_order(self.pair_code, int(order_id))
        logging.verbose('cancel_order: %s' % res)

        assert str(res['order_id']) == str(order_id)

        return True

    def _get_balances(self):
        """Get balance"""
        res = self.client.get_userinfo()
        logging.debug("get_balances: %s" % res)

        entry = res['info']['funds']

        self.bch_available = float(entry['free']['BCC'])
        self.bch_balance = float(entry['freezed']['BCC']) + float(entry['free']['BCC'])
        self.btc_available = float(entry['free']['BTC'])
        self.btc_balance = float(entry['freezed']['BTC']) + float(entry['free']['BTC'])

        logging.debug(self)
        return res
