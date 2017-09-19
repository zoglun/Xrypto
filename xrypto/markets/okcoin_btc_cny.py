from ._okcoin import OKCoin

class OKCoin_BTC_CNY(OKCoin):
    def __init__(self):
        super().__init__("CNY", "BTC", "btc_cny")
