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
import requests

class PriceMonitor(Observer):
    out_dir = './data/'
    last_diff = 0

    def __init__(self):
        super().__init__()
        self.OKCoin_BTC_CNY = 'OKCoin_BTC_CNY'
        self.OKEx_Future_Quarter = 'OKEx_Future_Quarter'
        self.rate = self.get_exchange_rate()

    def get_exchange_rate(self):
        response = requests.request("GET", 'https://www.okex.com/api/v1/exchange_rate.do', timeout=10)
        exchange_rate = response.json()
        return exchange_rate['rate']

    def tick(self, depths):

        OKEx_Future_Quarter_bid = (depths[self.OKEx_Future_Quarter]["bids"][0]['price'])
        OKCoin_BTC_CNY_ask = (depths[self.OKCoin_BTC_CNY]["asks"][0]['price'])

        diff = int(OKEx_Future_Quarter_bid*self.rate - OKCoin_BTC_CNY_ask)

        if self.last_diff != diff:
            self.last_diff = diff
        else:
            self.rate = self.get_exchange_rate()
            return

        logging.info("OKEx_Future_Quarter_bid, OKCoin_BTC_CNY_ask=(%s/%s), rate=%s, diff=%s" % (OKEx_Future_Quarter_bid*self.rate, OKCoin_BTC_CNY_ask, self.rate, diff))
       
        need_header = False

        filename = self.out_dir + 'diff.csv'

        if not os.path.exists(filename):
            need_header = True

        fp = open(filename, 'a+')

        if need_header:
            fp.write("timestamp, diff\n")

        fp.write(("%d") % time.time() +','+("%.2f") % diff +'\n')
        fp.close()

        return

  