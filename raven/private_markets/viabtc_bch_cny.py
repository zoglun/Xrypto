# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._viabtc import Viabtc

class PrivateViabtc_BCH_CNY(Viabtc):
    def __init__(self):
        super().__init__("CNY", "BTC", "bcccny")

    def test(self):
        order_id = self.buy_limit(0.01, 0.02)
        print(order_id)
        order_status = self.get_order(order_id)
        print(order_status)
        balance = self.get_balances()
        print(balance)
        cancel_status = self.cancel_order(order_id)
        print(cancel_status)
        order_status = self.get_order(order_id)
        print(order_status)

        order_id = self.sell_limit(0.02, 50000)
        print(order_id)
        order_status = self.get_order(order_id)
        print(order_status)

        balance = self.get_balances()
        print(balance)

        cancel_status = self.cancel_order(order_id)
        print(cancel_status)
        order_status = self.get_order(order_id)
        print(order_status)

