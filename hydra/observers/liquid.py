import logging
from .observer import Observer
import json
import time
import os
from brokers import kkex_bch_btc, viabtc_bch_btc
import random
import sys
import traceback
import config
from .basicbot import BasicBot
import threading

class Liquid(BasicBot):
    def __init__(self, mm_market='KKEX_BCH_BTC', 
                        refer_markets=['Viabtc_BCH_BTC', 'Bitfinex_BCH_BTC', 'Bittrex_BCH_BTC'],
                        hedge_market='Viabtc_BCH_BTC'):
        super().__init__()

        self.mm_market = mm_market

        self.brokers = {
            # TODO: move that to the config file
            mm_market: kkex_bch_btc.BrokerKKEX_BCH_BTC(config.KKEX_API_KEY, config.KKEX_SECRET_TOKEN),
            hedge_market: viabtc_bch_btc.BrokerViabtc_BCH_BTC(config.Viabtc_API_KEY, config.Viabtc_SECRET_TOKEN),
        }

        self.mm_broker = self.brokers[mm_market]
        
        self.refer_markets = refer_markets

        self.hedge_broker = hedge_market

        self.cancel_all_orders(self.mm_market)

        logging.info('MarketMaker Setup complete')
        # time.sleep(2)

    def terminate(self):
        super().terminate()
        
        self.cancel_all_orders(self.mm_market)

        logging.info('terminate complete')

    def tick(self, depths):
        refer_market = None
        for m in self.refer_markets:
            try:
                refer_bid_price, refer_ask_price = self.get_ticker(depths, m)
                refer_market = m
                break
            except Exception as ex:
                logging.warn("%s exception depths:%s" % (m, ex))
                continue
        
        if not refer_market:
            logging.warn('no avaliable market depths')
            return
        
        if self.hedge_broker:
            try:
                self.hedge_bid_price, self.hedge_ask_price = self.get_ticker(depths, self.hedge_broker)
            except Exception as ex:
                logging.warn("%s exception depths:%s" % (m, ex))
                return
        
        self.check_orders(depths, refer_bid_price, refer_ask_price)

        # Update client balance
        self.update_balance()   

        self.place_orders(refer_bid_price, refer_ask_price)

    def get_ticker(self, depths, market):
        bid_price = (depths[market]["bids"][0]['price'])
        ask_price = (depths[market]["asks"][0]['price'])

        logging.debug("market:%s bid, ask=(%s/%s)" % (market, bid_price, ask_price))
        return bid_price, ask_price

    def place_orders(self, refer_bid_price, refer_ask_price):
        liquid_max_amount = config.LIQUID_MAX_AMOUNT
        # excute trade
        if self.buying_len() < config.LIQUID_BUY_ORDER_PAIRS:
            if self.mm_broker.btc_available < config.LIQUID_BUY_RESERVE:
                logging.verbose("btc_available(%s) < reserve(%s)" % (self.mm_broker.btc_available, config.LIQUID_BUY_RESERVE))
            else:
                bprice = refer_bid_price*(1-config.LIQUID_DIFF)

                amount = round(liquid_max_amount*random.random(), 2)
                price = round(bprice*(1-0.1*random.random()), 5)

                if self.mm_broker.btc_available < amount*price:
                    logging.verbose("btc_available(%s) < amount(%s)" % (self.mm_broker.btc_available, amount))
                else:
                    self.new_order(self.mm_market, 'buy', amount=amount, price=price)

        if self.selling_len() < config.LIQUID_SELL_ORDER_PAIRS:
            if self.mm_broker.bch_available < config.LIQUID_BUY_RESERVE:
                logging.verbose("bch_available(%s) <  reserve(%s)" % (self.mm_broker.btc_available, config.LIQUID_BUY_RESERVE))
            else:
                sprice = refer_ask_price*(1+config.LIQUID_DIFF)

                amount = round(liquid_max_amount*random.random(), 2)
                price = round(sprice*(1+0.1*random.random()), 5)
                if self.mm_broker.bch_available < amount:
                    logging.verbose("bch_available(%s) < amount(%s)" % (self.mm_broker.bch_available, amount))
                else:
                    self.new_order(self.mm_market, 'sell', amount=amount, price=price)

        return

    def check_orders(self, depths, refer_bid_price, refer_ask_price):
        max_bprice = refer_bid_price*(1-config.LIQUID_DIFF*0.5)
        min_sprice = refer_ask_price*(1+config.LIQUID_DIFF*0.5)
        
        order_ids = self.get_order_ids()
        if not order_ids:
            return
        
        orders = self.mm_broker.get_orders(order_ids)
        if orders is not None:
            for order in orders:
                local_order = self.get_order(order['order_id'])
                self.hedge_order(local_order, order)

                if order['status'] == 'CLOSE' or order['status'] == 'CANCELED':
                    logging.info("order#%s %s: amount = %s price = %s deal = %s" % (order['order_id'], order['status'], order['amount'], order['price'], order['deal_amount']))
                    self.remove_order(order['order_id'])

                if order['type'] =='buy':
                    current_time = time.time()
                    if order['price'] > max_bprice:
                        logging.info("[TraderBot] cancel last BUY trade " +
                                        "occured %.2f seconds ago" %
                                        (current_time - local_order['time']))
                        logging.info("cancel max_bprice %s order['price'] = %s" % (max_bprice, order['price']))

                        self.cancel_order(self.mm_market, 'buy', order['order_id'])
                elif order['type'] == 'sell':
                    current_time = time.time()
                    if order['price'] < min_sprice:
                        logging.info("[TraderBot] cancel last SELL trade " +
                                        "occured %.2f seconds ago" %
                                        (current_time - local_order['time']))
                        logging.info("cancel min_sprice %s order['price'] = %s" % (min_sprice, order['price']))

                        self.cancel_order(self.mm_market, 'sell', order['order_id'])
        
    def hedge_order(self, order, result):
        if result['deal_amount'] <= 0:
            return

        order_id = result['order_id']        
        deal_amount = result['deal_amount']
        price = result['avg_price']

        amount = deal_amount - order['deal_amount']
        if amount <= config.LIQUID_HEDGE_MIN_AMOUNT:
            logging.debug("[hedger]deal nothing while.", amount, config.LIQUID_HEDGE_MIN_AMOUNT)
            return

        client_id = str(order_id) + '-' + str(order['deal_index'])

        logging.info("hedge new deal: %s", result)
        hedge_side = 'sell' if order['type'] =='buy' else 'buy'
        logging.info('hedge [%s] to broker: %s %s %s', client_id, hedge_side, amount, price)

        # if hedge_side == 'sell':
        #     self.brokers[self.hedge_market].sell_limit(amount, self.hedge_bid_price*(1-1%))
        # else:
        #     self.brokers[self.hedge_market].buy_limit(amount, self.hedge_ask_price*(1+1%))

        # update the deal_amount of local order
        self.remove_order(order_id)
        order['deal_amount'] = deal_amount
        order['deal_index'] +=1
        self.orders.append(order)