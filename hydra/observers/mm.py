import logging
from .observer import Observer
import json
import time
import os
from brokers import kkex_bch_btc
import math
import random
import sys
import traceback
import config
from .basicbot import BasicBot
import threading

class MM(BasicBot):
    def __init__(self, mm_market='KKEX_BCH_BTC'):
        super().__init__()

        self.mm_market = mm_market

        self.clients = {
            # TODO: move that to the config file
            "KKEX_BCH_BTC": kkex_bch_btc.BrokerKKEX_BCH_BTC(config.KKEX_API_KEY, config.KKEX_SECRET_TOKEN),
        }
        
        self.refer_market ='Viabtc_BCH_BTC'

        self.cancel_all_orders(self.mm_market)

        logging.info('MarketMaker Setup complete')
        # time.sleep(2)

    def terminate(self):
        super().terminate()
        
        self.cancel_all_orders(self.mm_market)

        logging.info('terminate complete')

    def tick(self, depths):
        try:
            refer_bid_price, refer_ask_price = self.get_refer_ticker(depths)
        except Exception as ex:
            logging.warn("exception depths:%s" % ex)
            traceback.print_exc()
            return

        self.check_orders(depths, refer_bid_price, refer_ask_price)

        # Update client balance
        self.update_balance()   

        self.place_orders(refer_bid_price, refer_ask_price)

    def get_refer_ticker(self, depths):
        refer_bid_price = (depths[self.refer_market]["bids"][0]['price'])
        refer_ask_price = (depths[self.refer_market]["asks"][0]['price'])

        logging.debug("refer_bid_price, refer_ask_price=(%s/%s)" % (refer_bid_price, refer_ask_price))
        return refer_bid_price, refer_ask_price

    def place_orders(self, refer_bid_price, refer_ask_price):
        bprice = refer_bid_price*(1-config.LIQUID_DIFF)
        sprice = refer_ask_price*(1+config.LIQUID_DIFF)
        
        base_amount = 10
        # excute trade
        if self.buying_len() < config.LIQUID_BUY_ORDER_PAIRS:
            amount = round(base_amount*random.random(), 2)
            go_bprice = round(bprice*(1-0.1*random.random()), 5)
            self.new_order(self.mm_market, 'buy', amount=amount, price=go_bprice)
        if self.selling_len() < config.LIQUID_SELL_ORDER_PAIRS:
            amount = round(base_amount*random.random(), 2)
            go_sprice = round(sprice*(1+0.1*random.random()), 5)
            self.new_order(self.mm_market, 'sell',amount=amount, price=go_sprice)


    def check_orders(self, depths, refer_bid_price, refer_ask_price):
        max_bprice = refer_bid_price*(1-config.LIQUID_DIFF*0.5)
        min_sprice = refer_ask_price*(1+config.LIQUID_DIFF*0.5)
        
        order_ids = self.get_order_ids()
        if not order_ids:
            return
        
        orders = self.clients[self.mm_market].get_orders(order_ids)
        if orders is not None:
            for order in orders:
                local_order = self.get_order(order['order_id'])
                self.hedge_order(local_order, order)

                if order['status'] == 'CLOSE' or order['status'] == 'CANCELED':
                    self.remove_order(order['id'])

                if order['type'] =='buy':
                    current_time = time.time()
                    if order['price'] > max_bprice:
                        logging.info("[TraderBot] cancel last BUY trade " +
                                        "occured %.2f seconds ago" %
                                        (current_time - buy_order['time']))
                        logging.info("cancel bprice %s order['price'] = %s" % (bprice, order['price']))

                        self.cancel_order(self.mm_market, 'buy', buy_order['id'])
                elif order['type'] == 'sell':
                    current_time = time.time()
                    if order['price'] < min_sprice:
                        logging.info("[TraderBot] cancel last SELL trade " +
                                        "occured %.2f seconds ago" %
                                        (current_time - sell_order['time']))
                        logging.info("cancel sprice %s order['price'] = %s" % (sprice, order['price']))

                        self.cancel_order(self.mm_market, 'sell', sell_order['id'])
        
            # # query orders
            # if self.is_buying():
            #     for buy_order in self.get_orders('buy'):
            #         logging.debug(buy_order)
            #         result = self.clients[self.mm_market].get_order(buy_order['id'])
            #         logging.debug(result)
            #         if not result:
            #             logging.warn("get_order buy #%s failed" % (buy_order['id']))
            #             return

            #         self.hedge_order(buy_order, result)

            #         if result['status'] == 'CLOSE' or result['status'] == 'CANCELED':
            #             self.remove_order(buy_order['id'])
            #         else:
            #             current_time = time.time()
            #             if result['price'] > max_bprice:
            #                 logging.info("[TraderBot] cancel last buy trade " +
            #                              "occured %.2f seconds ago" %
            #                              (current_time - buy_order['time']))
            #                 logging.info("cancel bprice %s result['price'] = %s" % (bprice, result['price']))

            #                 self.cancel_order(self.mm_market, 'buy', buy_order['id'])


            # if self.is_selling():
            #     for sell_order in self.get_orders('sell'):
            #         logging.debug(sell_order)
            #         result = self.clients[self.mm_market].get_order(sell_order['id'])
            #         logging.debug(result)
            #         if not result:
            #             logging.warn("get_order sell #%s failed" % (sell_order['id']))
            #             return

            #         self.hedge_order(sell_order, result)

            #         if result['status'] == 'CLOSE' or result['status'] == 'CANCELED':
            #             self.remove_order(sell_order['id'])
            #         else:
            #             current_time = time.time()
            #             if result['price'] < min_sprice:
            #                 logging.info("[TraderBot] cancel last SELL trade " +
            #                              "occured %.2f seconds ago" %
            #                              (current_time - sell_order['time']))
            #                 logging.info("cancel sprice %s result['price'] = %s" % (sprice, result['price']))

            #                 self.cancel_order(self.mm_market, 'sell', sell_order['id'])
            
    def update_balance(self):
        for kclient in self.clients:
            if kclient == self.mm_market:
                self.clients[kclient].get_balances()

    def hedge_order(self, order, result):
        pass