# Copyright (C) 2017, Philsong <songbohr@gmail.com>

import logging

class TradeException(Exception):
    pass

class Market:
    def __init__(self, base_currency, market_currency, pair_code):
        self.name = self.__class__.__name__
        self.brief_name  = self.name[7:]

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

    def buy_limit(self, amount, price, client_id=None):
        logging.verbose("BUY LIMIT %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.brief_name))
        if client_id:
            return self._buy_limit(amount, price, client_id)
        else:
            return self._buy_limit(amount, price)


    def sell_limit(self, amount, price, client_id=None):
        logging.verbose("SELL LIMIT %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.brief_name))
        if client_id:
            return self._sell_limit(amount, price, client_id)
        else:
            return self._sell_limit(amount, price)


    def buy_maker(self, amount, price):
        logging.verbose("BUY MAKER %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.brief_name))

        return self._buy_maker(amount, price)


    def sell_maker(self, amount, price):
        logging.verbose("SELL MAKER %f %s at %f %s @%s" % (amount, self.market_currency, 
                        price, self.base_currency, self.brief_name))

        return self._sell_maker(amount, price)

    def get_order(self, order_id):
        if not order_id:
            raise
        return self._get_order(order_id)

    def cancel_order(self, order_id):
        if not order_id:
            raise
        return self._cancel_order(order_id)

    def cancel_all(self):
        return self._cancel_all()

    def _buy_limit(self, amount, price):
        raise NotImplementedError("%s.buy(self, amount, price)" % self.name)

    def _sell_limit(self, amount, price):
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

    def test(self):
        pass
