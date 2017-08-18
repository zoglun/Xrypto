# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from .market import Market, TradeException
import config
import logging
from lib.viabtc.ViabtcAPI import ViabtcClient

# python3 raven/raven-cli.py -m Bitfinex_BCH_BTC get-balance

class Viabtc(Market):
    def __init__(self, base_currency, market_currency, pair_code, api_key=None, api_secret=None):
        super().__init__(base_currency, market_currency, pair_code)

        self.trade_client = ViabtcClient(
                    api_key if api_key else config.Viabtc_API_KEY,
                    api_secret if api_secret else config.Viabtc_SECRET_TOKEN)

        self.get_balances()
 
    def _buy_limit(self, amount, price):
        """Create a buy limit order"""
        res = self.trade_client.order_limit(
            'buy',
            amount=str(amount),
            price=str(price),
            market=self.pair_code)
        return res['data']['id']

    def _sell_limit(self, amount, price):
        """Create a sell limit order"""
        res = self.trade_client.order_limit(
            'sell',
            amount=str(amount),
            price=str(price),
            market=self.pair_code)
        return res['data']['id']

    def _order_status(self, res):
        print(res)

        resp = {}
        resp['order_id'] = res['id']
        resp['amount'] = float(res['amount'])
        resp['price'] = float(res['price'])
        resp['deal_size'] = float(res['deal_amount'])
        resp['avg_price'] = float(res['avg_price'])

        if res['status'] == 'not_deal' or res['status'] == 'part_deal':
            resp['status'] = 'OPEN'
        else:
            resp['status'] = 'CLOSE'

        return resp

    def _get_order(self, order_id):
        res = self.trade_client.get_order_status(int(order_id), market=self.pair_code)
        logging.info('get_order: %s' % res)

        assert str(res['data']['id']) == str(order_id)
        return self._order_status(res['data'])


    def _cancel_order(self, order_id):
        res = self.trade_client.cancel_order(int(order_id), market=self.pair_code)
        assert str(res['id']) == str(order_id)

        resp = self._order_status(res)
        if resp:
            return True
        else:
            return False

    def get_balances(self):
        """Get balance"""
        try:
            res = self.trade_client.get_account()
        except Exception as e:
            logging.error('get_balances except: %s' % e)
            return None

        logging.debug("get_balances response: %s" % res)

        entry = res['data']

        self.bch_available = float(entry['BCC']['available'])
        self.bch_balance = float(entry['BCC']['available']) + float(entry['BCC']['frozen'])
        self.btc_available = float(entry['BTC']['available'])
        self.btc_balance = float(entry['BTC']['available']) + float(entry['BTC']['frozen'])
        self.cny_available = float(entry['CNY']['available'])
        self.cny_balance = float(entry['CNY']['available']) + float(entry['CNY']['frozen'])

        return res

    def test(self):
        order_id = self.buy_limit(0.11, 0.02)
        print(order_id)
        order_status = self.get_order(order_id)
        print(order_status)
        balance = self.get_balances()
        print(balance)
        cancel_status = self.cancel_order(order_id)
        print(cancel_status)
        order_status = self.get_order(order_id)
        print(order_status)

        order_id = self.sell_limit(0.12, 0.15)
        print(order_id)
        order_status = self.get_order(order_id)
        print(order_status)

        balance = self.get_balances()
        print(balance)

        cancel_status = self.cancel_order(order_id)
        print(cancel_status)
        order_status = self.get_order(order_id)
        print(order_status)



            
        