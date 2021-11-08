#!python
#cython: language_level=3

from collections import namedtuple
from numpy import number, string_
from domain.exchangeInfo import ExchangeInfo
from domain.exchangeReport import ExchangeReport
from service.priceService import PriceService
from config import Config

from datetime import date, timedelta, tzinfo
from pymongo import MongoClient

import shioaji as sj
import pandas as pd

import datetime

class InitExchangeReport():
    def __init__(self, config: Config):
        self.config = config;
        self.name = "InitExchangeReport";

        now = datetime.datetime.now();
        self.start: datetime = datetime.datetime(now.year - 2, now.month, now.day, 0, 0, 0)
        self.end : datetime = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        mongoClient = MongoClient(config.mongodbUri)
        database = mongoClient[config.mongodbDataBase]
        self.collection = database.ExchangeInfo
    
    def execution(self, args):
        config = self.config
        contracts = [];
        exchangeReports = [];
        
        api = sj.Shioaji()
        api.login(config.account, config.password)

        for code in args:
            if code == self.name:
                continue;
            contracts.append(api.Contracts.Stocks[code]);

        snapshots = api.snapshots(contracts)
        for snapshot in snapshots:
            code = snapshot['code']
            price = snapshot['sell_price']

            exchangeReport = ExchangeReport(code);
            exchangeReports.append(exchangeReport)

            cursor = self.collection.find({
                "code": code,
                "timestamp": {
                    "$gte": self.start,
                    "$lt": self.end
                }
            })
            exchangeInfos = []
            datas = list(cursor)
            datas.sort(key=lambda x: x['timestamp'] ,reverse=True)
            for item in datas:
                exchangeInfo:ExchangeInfo = namedtuple('ExchangeInfo', item.keys(), rename=True)(*item.values())
                exchangeInfos.append(exchangeInfo);
            
            PriceService.judgingPriceHighLowPoints(exchangeReport, price, exchangeInfos);

        for exchangeReport in exchangeReports:
            exchangeReport: ExchangeReport = exchangeReport;
            code = exchangeReport.code