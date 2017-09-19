from ._okex import OKEx

class OKEx_Future_Quarter(OKEx):
    def __init__(self):
        super().__init__("USD", "BTC", "btc_usd", "quarter")
