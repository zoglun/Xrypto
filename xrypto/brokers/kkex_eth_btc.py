# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._kkex import KKEX
import time

class BrokerKKEX_ETH_BTC(KKEX):
    def __init__(self, api_key=None, api_secret=None):
        super().__init__("BTC", "ETH", "ETHBTC", api_key, api_secret)

    def test(self):
        balance = self.get_balances()

        # order_id = self.buy_limit(10, 1.3)
        # print(order_id)
        # order_status = self.get_order(order_id)
        # print(order_status)
        # # balance = self.get_balances()
        # # time.sleep(3)

        # cancel_status = self.cancel_order(order_id)
        # print(cancel_status)
        # # while(True):
        # #     order_status = self.get_order(order_id)
        # #     time.sleep(3)
        # order_status = self.get_order(order_id)
        # print(order_status)

        # balance = self.get_balances()

        # order_id = self.sell_limit(1.1, 10000)
        # print(order_id)
        # order_status = self.get_order(order_id)
        # print(order_status)

        # # balance = self.get_balances()

        # # cancel_status = self.cancel_order(order_id)
        # # print(cancel_status)
        # order_status = self.get_order(order_id)
        # print(order_status)

