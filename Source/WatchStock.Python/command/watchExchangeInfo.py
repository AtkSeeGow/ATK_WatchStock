#!python
#cython: language_level=3

from pydantic.errors import DataclassTypeError
from shioaji.data import Kbars
from domain.exchangeInfo import ExchangeInfo
from config import Config

from datetime import date, timedelta, tzinfo
from pymongo import MongoClient

import shioaji as sj
import pandas as pd

import datetime

class WatchExchangeInfo():
    def __init__(self, config: Config):
        self.config = config;
        self.name = "WatchExchangeInfo";
    
    def execution(self, args):
        config = self.config
        contracts = [];
        now = datetime.datetime.now();

        start: datetime = datetime.datetime(now.year - 2, now.month, now.day, 0, 0, 0)
        end : datetime = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        api = sj.Shioaji()
        api.login(config.account, config.password)

        for code in args:
            if code == self.name:
                continue;
            contracts.append(api.Contracts.Stocks[code]);

        mongoClient = MongoClient(config.mongodbUri)
        database = mongoClient[config.mongodbDataBase]
        collection = database.ExchangeInfo

        snapshots = api.snapshots(contracts)
        for snapshot in snapshots:
            code = snapshot['code']
            price = snapshot['sell_price']

            cursor = collection.find({
                "code": code,
                "timestamp": {
                    "$gte": start,
                    "$lt": end
                }
            })
            exchangeInfos = list(cursor)
            exchangeInfos.sort(key=lambda x: x['timestamp'] ,reverse=True)
            print(snapshot);



            
        # 取得兩年內資料，判斷目前是多久以來得最低點/最高點
        # 產生報告郵件