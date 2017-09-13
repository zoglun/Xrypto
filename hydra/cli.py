
# Copyright (C) 2016-2017, Phil Song <songbohr@gmail.com>
import os
import logging
import argparse
import sys
import glob
import inspect

from logging.handlers import RotatingFileHandler
import datetime
import time
import config
import traceback

import markets
from snapshot import Snapshot
from datafeed import Datafeed
from arbitrer import Arbitrer

class CLI:
    def __init__(self):
        self.inject_verbose_info()

    def inject_verbose_info(self):
        logging.VERBOSE = 15
        logging.verbose = lambda x: logging.log(logging.VERBOSE, x)
        logging.addLevelName(logging.VERBOSE, "VERBOSE")

    def exec_command(self, args):
        logging.debug('exec_command:%s' % args)
        if "watch" in args.command:
            self.create_datafeed(args)
            self.datafeed.run_loop()

        if "b-watch" in args.command:
            self.create_arbitrer(args)
            self.arbitrer.run_loop()

        if "t-watch-viabtc-bcc" in args.command:
            self.create_t_arbitrer_viabtc_bcc(args)
            self.datafeed.run_loop()

        if "t-watch-binance-wtc" in args.command:
            self.create_t_arbitrer_binance_wtc(args)
            self.arbitrer.run_loop()

        if "t-watch-binance-bnb" in args.command:
            self.create_t_arbitrer_binance_bnb(args)
            self.arbitrer.run_loop()

        if "t-watch-binance-lrc" in args.command:
            self.create_t_arbitrer_binance_lrc(args)
            self.arbitrer.run_loop()

        if "t-watch-binance-mco" in args.command:
            self.create_t_arbitrer_binance_mco(args)
            self.arbitrer.run_loop()

        if "t-watch-binance-qtum" in args.command:
            self.create_t_arbitrer_binance_qtum(args)
            self.arbitrer.run_loop()

        if "replay-history" in args.command:
            self.create_arbitrer(args)
            self.arbitrer.replay_history(args.replay_history)
        if "get-balance" in args.command:
            self.get_balance(args)
        if "list-public-markets" in args.command:
            self.list_markets()
        if "get-broker-balance" in args.command:
            self.get_broker_balance(args)
        if "test_pub" in args.command:
            self.test_pub(args)
        if "test_pri" in args.command:
            self.test_pri(args)

    def list_markets(self):
        logging.debug('list_markets') 
        for filename in glob.glob(os.path.join(markets.__path__[0], "*.py")):
            module_name = os.path.basename(filename).replace('.py', '')
            if not module_name.startswith('_'):
                module = __import__("markets." + module_name)
                test = eval('module.' + module_name)
                for name, obj in inspect.getmembers(test):
                    if inspect.isclass(obj) and 'Market' in (j.__name__ for j in obj.mro()[1:]):
                        if not obj.__module__.split('.')[-1].startswith('_'):
                            print(obj.__name__)
        sys.exit(0)


    def test_pub(self, args):
        if not args.markets:
            logging.error("You must use --markets argument to specify markets")
            sys.exit(2)
        pmarkets = args.markets.split(",")
        pmarketsi = []
        for pmarket in pmarkets:
            exec('import markets.' + pmarket.lower())
            market = eval('markets.' + pmarket.lower() + '.' +
                           pmarket + '()')
            pmarketsi.append(market)

        for market in pmarketsi:
            print(market.get_ticker())

    def test_pri(self, args):
        if not args.markets:
            logging.error("You must use --markets argument to specify markets")
            sys.exit(2)
        pmarkets = args.markets.split(",")
        pmarketsi = []
        for pmarket in pmarkets:
            exec('import brokers.' + pmarket.lower())
            market = eval('brokers.' + pmarket.lower()
                          + '.Broker' + pmarket + '()')
            pmarketsi.append(market)

        for market in pmarketsi:
            market.test()

    def get_balance(self, args):
        if not args.markets:
            logging.error("You must use --markets argument to specify markets")
            sys.exit(2)
        pmarkets = args.markets.split(",")
        pmarketsi = []
        for pmarket in pmarkets:
            exec('import brokers.' + pmarket.lower())
            market = eval('brokers.' + pmarket.lower()
                          + '.Broker' + pmarket + '()')
            pmarketsi.append(market)

        snapshot = Snapshot()

        while True:
            total_btc = 0.
            total_bch = 0.
            for market in pmarketsi:
                market.get_balances()
                print(market)
                total_btc += market.btc_balance
                total_bch += market.bch_balance
                snapshot.snapshot_balance(market.name[7:], market.btc_balance, market.bch_balance)

            snapshot.snapshot_balance('ALL', total_btc, total_bch)

            time.sleep(60*10)

    def create_datafeed(self, args):
        self.datafeed = Datafeed()
        self.init_observers_and_markets(args)

    def create_arbitrer(self, args):
        self.arbitrer = Arbitrer()
        self.init_observers_and_markets(args)

    def create_t_arbitrer_viabtc_bcc(self, args):
        from t_arbitrer_viabtc import TrigangularArbitrer_Viabtc
        self.datafeed = TrigangularArbitrer_Viabtc(base_pair='Viabtc_BCH_CNY',
                                                    pair1='Viabtc_BCH_BTC',
                                                    pair2='Viabtc_BTC_CNY')
        self.init_observers_and_markets(args)

    def create_t_arbitrer_binance_wtc(self, args):
        from t_arbitrer_binance import TrigangularArbitrer_Binance
        self.arbitrer = TrigangularArbitrer_Binance(base_pair='Binance_WTC_BTC',
                                                    pair1='Binance_WTC_ETH',
                                                    pair2='Binance_ETH_BTC')
        self.init_observers_and_markets(args)

    def create_t_arbitrer_binance_bnb(self, args):
        from t_arbitrer_binance import TrigangularArbitrer_Binance
        self.arbitrer = TrigangularArbitrer_Binance(base_pair='Binance_BNB_BTC',
                                                    pair1='Binance_BNB_ETH',
                                                    pair2='Binance_ETH_BTC')
        self.init_observers_and_markets(args)

    def create_t_arbitrer_binance_lrc(self, args):
        from t_arbitrer_binance import TrigangularArbitrer_Binance
        self.arbitrer = TrigangularArbitrer_Binance(base_pair='Binance_LRC_BTC',
                                                    pair1='Binance_LRC_ETH',
                                                    pair2='Binance_ETH_BTC')
        self.init_observers_and_markets(args)

    def create_t_arbitrer_binance_mco(self, args):
        from t_arbitrer_binance import TrigangularArbitrer_Binance
        self.arbitrer = TrigangularArbitrer_Binance(base_pair='Binance_MCO_BTC',
                                                    pair1='Binance_MCO_ETH',
                                                    pair2='Binance_ETH_BTC')
        self.init_observers_and_markets(args)

    def create_t_arbitrer_binance_qtum(self, args):
        from t_arbitrer_binance import TrigangularArbitrer_Binance
        self.arbitrer = TrigangularArbitrer_Binance(base_pair='Binance_QTUM_BTC',
                                                    pair1='Binance_QTUM_ETH',
                                                    pair2='Binance_ETH_BTC')
        self.init_observers_and_markets(args)


    def init_observers_and_markets(self, args):
        if args.observers:
            self.datafeed.init_observers(args.observers.split(","))
        if args.markets:
            self.datafeed.init_markets(args.markets.split(","))

    def init_logger(self, args):
        level = logging.INFO
        if args.verbose:
            level = logging.VERBOSE
        if args.debug:
            level = logging.DEBUG
            
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                            level=level)

        Rthandler = RotatingFileHandler('hydra.log', maxBytes=100*1024*1024,backupCount=10)
        Rthandler.setLevel(level)
        formatter = logging.Formatter('%(asctime)-12s [%(levelname)s] %(message)s')  
        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler)

        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--debug", help="debug verbose mode",
                            action="store_true")
        parser.add_argument("-v", "--verbose", help="info verbose mode",
                            action="store_true")
        parser.add_argument("-o", "--observers", type=str,
                            help="observers, example: -oLogger,Emailer")
        parser.add_argument("-m", "--markets", type=str,
                            help="markets, example: -mHaobtcCNY,Bitstamp")
        parser.add_argument("-s", "--status", help="status", action="store_true")
        parser.add_argument("command", nargs='*', default="watch",
                            help='verb: "watch|replay-history|get-balance|list-public-markets|get-broker-balance"')
        args = parser.parse_args()
        self.init_logger(args)
        self.exec_command(args)
        print('main end')
        exit(-1)

def main():
    cli = CLI()
    cli.main()

if __name__ == "__main__":
    main()
