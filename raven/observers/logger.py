import logging
from .observer import Observer


class Logger(Observer):
    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc,
                    weighted_buyprice, weighted_sellprice,
                    base_currency, market_currency):
        if profit > config.profit_thresh and perc > config.perc_thresh:
            logging.info("profit: %f %s with volume: %f %s - buy at %.8f (%s) sell at %.8f (%s) ~%.2f%%" \
                % (profit, base_currency, volume, market_currency, buyprice, kask, sellprice, kbid, perc))
