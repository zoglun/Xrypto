from .observer import Observer
import json
import time
import os
from brokers import haobtccny,huobicny,okcoincny,brokercny
import sys
import traceback
import config
import logging
from .emailer import send_email
from .basicbot import BasicBot

class BalanceDumper(BasicBot):
    exchange = 'OKCoin_BTC_CNY'

    out_dir = 'balance_dumper/'

    def __init__(self):        
        self.brokers = {
            "OKEx_BTC_Future": okex_btc_future.BrokerOKEx_BTC_Future(config.OKEX_API_KEY, config.OKEX_SECRET_TOKEN),
            "OKCoin_BTC_CNY": bittrex_bch_btc.BrokerOKCoin_BTC_CNY(config.OKCOIN_API_KEY, config.OKCOIN_SECRET_TOKEN),
            "Viabtc_BCH_BTC": viabtc_bch_btc.BrokerViabtc_BCH_BTC(config.HUOBI_API_KEY, config.HUOBI_SECRET_TOKEN),
        }

        self.cny_balance = 0
        self.btc_balance = 0
        self.cny_frozen = 0
        self.btc_frozen = 0
        self.cny_total = 0
        self.btc_total = 0
       
        try:
            os.mkdir(self.out_dir)
        except:
            pass

    def update_trade_history(self, exchange, time, price, cny, btc, cny_b, btc_b, cny_f, btc_f):
        filename = self.out_dir + exchange + '_balance.csv'
        need_header = False

        if not os.path.exists(filename):
            need_header = True

        fp = open(filename, 'a+')

        if need_header:
            fp.write("timestamp, price, cny, btc, cny_b, btc_b, cny_f, btc_f\n")

        fp.write(("%d") % time +','+("%.f") % price+','+("%.f") % cny+','+ str(("%.2f") % btc) +','+ str(("%.f") % cny_b)+','+ str(("%.2f") % btc_b)+','+ str(("%.f") % cny_f)+','+ str(("%.2f") % btc_f)+'\n')
        fp.close()

    def sum_balance(self):
        for kclient in self.brokers:
            self.cny_balance += self.brokers[kclient].cny_balance
            self.btc_balance += self.brokers[kclient].btc_balance

    def cny_balance_total(self, price):
        return self.cny_balance + self.btc_balance * price
    
    def btc_balance_total(self, price):
        return self.btc_balance + self.cny_balance / (price*1.0)


    def tick(self, depths):
        # Update client balance
        self.update_balance()
        self.sum_balance()

        # get price
        try:
            bid_price = int(depths[self.exchange]["bids"][0]['price'])
            ask_price = int(depths[self.exchange]["asks"][0]['price'])
        except  Exception as ex:
            logging.warn("exception depths:%s" % ex)
            t,v,tb = sys.exc_info()
            print(t,v)
            traceback.print_exc()

            # logging.warn(depths)
            return

        if bid_price == 0 or ask_price == 0:
            logging.warn("exception ticker")
            return
        
        cny_abs = abs(self.cny_total - self.cny_balance_total(bid_price))
        cny_diff = self.cny_total*0.1
        btc_abs = abs(self.btc_total - self.btc_balance_total(ask_price))
        btc_diff = self.btc_total*0.1

        self.cny_total = self.cny_balance_total(bid_price)
        self.btc_total = self.btc_balance_total(ask_price)

        if (cny_abs > 200 and cny_abs < cny_diff) or (btc_abs > 0.1 and btc_abs < btc_diff):
            logging.info("update_balance-->")
            self.update_trade_history(self.exchange, time.time(), bid_price, 
                self.cny_total, self.btc_total,
                self.cny_balance, self.btc_balance,
                self.cny_frozen, self.btc_frozen)
