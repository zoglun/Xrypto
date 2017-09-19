#-*- coding: utf-8 -*-

# Copyright (C) 2017, Phil Song <songbohr@gmail.com>

import markets
import observers
import config
import time
import logging
import json
from concurrent.futures import ThreadPoolExecutor, wait
import traceback

import re,sys,re
import string
import signal
 

is_sigint_up = False

def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print ('catched interrupt signal!')

class Datafeed(object):
    def __init__(self):
        self.markets = []
        self.observers = []
        self.depths = {}
        self.init_markets(config.markets)
        self.init_observers(config.observers)
        self.threadpool = ThreadPoolExecutor(max_workers=10)

    def init_markets(self, _markets):
        logging.debug("_markets:%s" % _markets)
        self.market_names = _markets
        for market_name in _markets:
            if self.get_market(market_name):
                continue

            try:
                exec('import markets.' + market_name.lower())
                market = eval('markets.' + market_name.lower() + '.' +
                              market_name + '()')
                self.markets.append(market)
            except (ImportError, AttributeError) as e:
                print("%s market name is invalid: Ignored (you should check your config file)" % (market_name))
                logging.warn("exception import:%s" % e)
                traceback.print_exc()

    def init_observers(self, _observers):
        logging.debug("_observers:%s" % _observers)

        self.observer_names = _observers
        for observer_name in _observers:
            try:
                exec('import observers.' + observer_name.lower())
                observer = eval('observers.' + observer_name.lower() + '.' +
                                observer_name + '()')
                self.observers.append(observer)
            except (ImportError, AttributeError) as e:
                print("%s observer name is invalid: Ignored (you should check your config file)" % (observer_name))
                print(e)
                

    def get_market(self, market_name):
        for market in self.markets:
            if market.name == market_name:
                return market

        return None


    def observer_tick(self):
        for observer in self.observers:
            observer.tick(self.depths)

    def tick(self):
        self.print_tickers()
 
        self.observer_tick()

    def __get_market_depth(self, market, depths):
        depth = market.get_depth()
        if depth:
            depths[market.name] = depth

    def update_depths(self):
        depths = {}
        futures = []

        for market in self.markets:
            futures.append(self.threadpool.submit(self.__get_market_depth,
                                                  market, depths))
        wait(futures, timeout=20)
        return depths

    def print_tickers(self):
        for market in self.markets:
            logging.debug("ticker: " + market.name + " - " + str(market.get_ticker()))

    def replay_history(self, directory):
        import os
        import json
        import pprint
        files = os.listdir(directory)
        files.sort()
        for f in files:
            depths = json.load(open(directory + '/' + f, 'r'))
            self.depths = {}
            for market in self.market_names:
                if market in depths:
                    self.depths[market] = depths[market]
            self.tick()

    def update_balance(self):
        pass

    def terminate(self):
        for observer in self.observers:
            observer.terminate()

        for market in self.markets:
            market.terminate()

    def run_loop(self):
        if len(self.markets) == 0:
            print('empty markets')
            return

        if len(self.observers) == 0:
            print('empty observers')
            return
        #
        signal.signal(signal.SIGINT, sigint_handler)
        #以下那句在windows python2.4不通过,但在freebsd下通过
        signal.signal(signal.SIGHUP, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        while True:
            self.update_balance()

            self.depths = self.update_depths()

            try:
                self.tick()
            except Exception as ex:
                logging.warn("exception depths:%s" % ex)
                traceback.print_exc()
                return

            if is_sigint_up:
                # 中断时需要处理的代码
                logging.info("APP Exit")
                self.terminate()
                break
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(config.refresh_rate)
