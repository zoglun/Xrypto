from ._kkex import KKEX
from ._bittrex import Bittrex
from ._bitfinex import Bitfinex

import logging
import config

def create_brokers(exchangeNames):
    brokers = {}
    for name in exchangeNames:
        if (name == 'KKEX_BCH_BTC'):
            xchg = KKEX('BCCBTC', config.KKEX_API_KEY, config.KKEX_SECRET_TOKEN)
        elif (name == 'KKEX_ETH_BTC'):
            xchg = KKEX('ETHBTC', config.KKEX_API_KEY, config.KKEX_SECRET_TOKEN)
        elif (name == 'Bitfinex_BCH_BTC'):
            xchg = Bitfinex('bchbtc', config.Bitfinex_API_KEY, config.Bitfinex_SECRET_TOKEN)
        elif (name == 'Bittrex_BCH_BTC'):
            xchg = Bittrex('BTC-BCC', config.Bittrex_API_KEY, config.Bittrex_SECRET_TOKEN)
        else:
            logging.warn('Exchange ' + name + ' not supported!')
            assert(False)
        logging.info('%s initialized' % (xchg.name))
        
        balance = xchg.get_balances()


        brokers[name]= xchg
        print(brokers)
    return brokers