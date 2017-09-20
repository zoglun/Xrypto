from ._kkex import KKEX
from ._bittrex import Bittrex
from ._bitfinex import Bitfinex

import logging
import config

def create_markets(exchangeNames):
    markets = {}
    for name in exchangeNames:
        if (name == 'KKEX_BCH_BTC'):
            xchg = KKEX('BCCBTC')
        elif (name == 'KKEX_ETH_BTC'):
            xchg = KKEX('ETHBTC')
        elif (name == 'Bitfinex_BCH_BTC'):
            xchg = Bitfinex('bchbtc')
        elif (name == 'Bittrex_BCH_BTC'):
            xchg = Bittrex('BTC-BCC')
        else:
            logging.warn('Exchange ' + name + ' not supported!')
            assert(False)
        logging.info('%s initialized' % (xchg.name))
        
        ticker = xchg.get_ticker()

        markets[name]= xchg
        print(markets)
    return markets