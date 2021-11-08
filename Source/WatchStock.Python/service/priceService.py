from datetime import datetime
from numpy import number
from config import Config
from domain.exchangeReport import ExchangeReport
from domain.exchangeInfo import ExchangeInfo
from domain.priceStatus import PriceStatus

import datetime

class PriceService():
    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def judgingPriceHighLowPoints(exchangeReport: ExchangeReport, price: number, exchangeInfos: list):
        now = datetime.datetime.now();
        for exchangeInfo in exchangeInfos:
            exchangeInfo: ExchangeInfo = exchangeInfo;
            if exchangeReport.priceStatus == PriceStatus.Empty:
                if exchangeInfo.close > price:
                    exchangeReport.priceStatus = PriceStatus.Low;
                else:
                    exchangeReport.priceStatus = PriceStatus.High;
                continue;
            
            if exchangeReport.priceStatus == PriceStatus.Low:
                if exchangeInfo.close > price:
                    continue;

            if exchangeReport.priceStatus == PriceStatus.High:
                if not exchangeInfo.close > price:
                    continue;

            span = now - exchangeInfo.timestamp
            exchangeReport.priceSpan = span.days;
            break;


        