markets = [
# "BitstampUSD",
# "BTCCCNY",
# "BtceUSD",
# "CoinbaseUSD",
# "GeminiUSD",
# "KrakenEUR",
# "KrakenUSD",
# "OKCoinCNY",
# "HuobiCNY",
# "Bitfinex_BCH_BTC",
# "Bittrex_BCH_BTC",
]

# observers if any
# ["Logger", "TraderBot", "TraderBotSim", "HistoryDumper", "Emailer", "SpecializedTraderBot"]
observers = ["Logger"]

market_expiration_time = 120  # in seconds: 2 minutes

refresh_rate = 5

trade_wait = 10

btc_profit_thresh = 0.001  # in BTC
btc_perc_thresh = 0.01  # in 0.01%
bch_max_tx_volume = 5  # in BCH
bch_min_tx_volume = 0.5  # in BCH
bch_frozen_volume = 10

price_departure_perc = 0.002 #in BTC 1%

bch_guide_dog_volume = 10

Diff = 1.001 # 0.1 % arbitrage to execute

TFEE = 1.003 # 1+3*0.001

FEE = 1.0025 # fee for every trade (0.25%)

MAKER_TRADE_ENABLE = False
TAKER_TRADE_ENABLE = True
# maker
MAKER_MAX_VOLUME = 30
MAKER_MIN_VOLUME = 1
MAKER_BUY_QUEUE = 3
MAKER_BUY_STAGE = 1
MAKER_SELL_QUEUE = 3
MAKER_SELL_STAGE = 2

TAKER_MAX_VOLUME = 10
TAKER_MIN_VOLUME = 0.01

LIQUID_BUY_ORDER_PAIRS = 50
LIQUID_SELL_ORDER_PAIRS = 50
LIQUID_DIFF = 0.001 #20%

bid_fee_rate = 0.001
ask_fee_rate = 0.001
bid_price_risk = 0
ask_price_risk = 0


#hedger

reverse_profit_thresh = 1
reverse_perc_thresh = 0.01
reverse_max_tx_volume = 1  # in BTC

stage0_percent=0.1
stage1_percent=0.2

BUY_QUEUE = 1
SELL_QUEUE = 1


broker_min_amount = 0.01

#stata
cny_init = 60000000000
btc_init = 1200000
price_init = 4450

#### Emailer Observer Config
send_trade_mail = False

EMAIL_HOST = 'mail.FIXME.com'
EMAIL_HOST_USER = 'FIXME@FIXME.com'
EMAIL_HOST_PASSWORD = 'FIXME'
EMAIL_USE_TLS = True

EMAIL_RECEIVER = ['FIXME@FIXME.com']


#### XMPP Observer
xmpp_jid = "FROM@jabber.org"
xmpp_password = "FIXME"
xmpp_to = "TO@jabber.org"

# broker thrift server
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 18030

#### Trader Bot Config
# Access to Broker APIs

bitstamp_username = "FIXME"
bitstamp_password = "FIXME"


HUOBI_API_KEY = ''
HUOBI_SECRET_TOKEN = ''

OKCOIN_API_KEY = ''
OKCOIN_SECRET_TOKEN = ''

KKEX_API_KEY = ''
KKEX_SECRET_TOKEN = ''

BITSTAR_API_KEY = ''
BITSTAR_SECRET_TOKEN = ''

Bitfinex_API_KEY = ''
Bitfinex_SECRET_TOKEN = ''

Bittrex_API_KEY = ''
Bittrex_SECRET_TOKEN = ''

Viabtc_API_KEY = ''
Viabtc_SECRET_TOKEN = ''


SUPPORT_ZMQ = True
ZMQ_HOST = "127.0.0.1"
ZMQ_PORT = 18031

SUPPORT_WEBSOCKET = False
WEBSOCKET_HOST = 'http://localhost'
WEBSOCKET_PORT = 13001

ENV = 'local'

try:
    from local_config import *
except ImportError:
    pass

