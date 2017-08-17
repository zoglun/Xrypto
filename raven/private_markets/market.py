# Copyright (C) 2013, Maxime Biais <maxime@biais.org>

import logging

class TradeException(Exception):
    pass

class Market:
    def __init__(self, base_currency, market_currency, pair_code):
        self.name = self.__class__.__name__

        self.base_currency = base_currency
        self.market_currency = market_currency
        self.pair_code = pair_code

        self.btc_balance = 0.
        self.bch_balance = 0.
        self.btc_available = 0.
        self.bch_available = 0.
        # self.market = None

    def __str__(self):
        return "%s: %s" % (self.name[7:], str({"btc_balance": self.btc_balance,
                                           "bch_balance": self.bch_balance,
                                           "btc_available": self.btc_available,
                                           "bch_available": self.bch_available}))

    def buy(self, amount, price, client_id=None):
        logging.verbose("BUY LIMIT%f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.name))
        if client_id:
            return self._buy(amount, local_currency_price, client_id)
        else:
            return self._buy(amount, local_currency_price)


    def sell(self, amount, price, client_id=None):
        logging.verbose("SELL LIMIT %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.name))
        if client_id:
            return self._sell(amount, local_currency_price, client_id)
        else:
            return self._sell(amount, local_currency_price)


    def buy_maker(self, amount, price):
        logging.verbose("BUY MAKER %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.name))

        return self._buy_maker(amount, local_currency_price)


    def sell_maker(self, amount, price):
        logging.verbose("SELL MAKER %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.name))

        return self._sell_maker(amount, local_currency_price)

    def get_order(self, order_id):
        return self._get_order(order_id)

    def cancel_order(self, order_id):
        return self._cancel_order(order_id)

    def cancel_all(self):
        return self._cancel_all()

    def _buy(self, amount, price):
        raise NotImplementedError("%s.buy(self, amount, price)" % self.name)

    def _sell(self, amount, price):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def _buy_maker(self, amount, price):
        raise NotImplementedError("%s.buy_maker(self, amount, price)" % self.name)

    def _sell_maker(self, amount, price):
        raise NotImplementedError("%s.sell_maker(self, amount, price)" % self.name)

    def _get_order(self, order_id):
        raise NotImplementedError("%s.get_order(self, order_id)" % self.name)

    def _cancel_order(self, order_id):
        raise NotImplementedError("%s.cancel_order(self, order_id)" % self.name)

    def _cancel_all(self):
        raise NotImplementedError("%s.cancel_all(self)" % self.name)

    def deposit(self):
        raise NotImplementedError("%s.deposit(self)" % self.name)

    def withdraw(self, amount, address):
        raise NotImplementedError("%s.withdraw(self, amount, address)" % self.name)

    def get_balances(self):
        raise NotImplementedError("%s.get_balances(self)" % self.name)
