#!python
#cython: language_level=3

from shioaji.data import Kbars
from domain.exchangeInfo import ExchangeInfo
from config import Config

from datetime import date, timedelta, tzinfo
from pymongo import MongoClient

import shioaji as sj
import pandas as pd

import datetime

class InitExchangeInfo():
    def __init__(self, config: Config):
        self.config = config
        self.name = "InitExchangeInfo"

    def execution(self, args):
        config = self.config
        code = args[1]
        start: datetime = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        end: datetime = datetime.datetime.strptime(
            args[3], "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)
        api = sj.Shioaji()

        mongoClient = MongoClient(config.mongodbUri, tz_aware='true')
        database = mongoClient[config.mongodbDataBase]
        collection = database.ExchangeInfo

        api.login(config.account, config.password)
        contract = api.Contracts.Stocks[code]
        kBars = api.kbars(contract, start=start.strftime(
            "%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))

        pandas = pd.DataFrame({**kBars})
        pandas.ts = pd.to_datetime(pandas.ts)
        pandas = pandas.sort_values(by=['ts'], ascending=True)
        
        collection.delete_many({
            "code": code,
            "timestamp": {
                "$gte": start,
                "$lt": end
            }
        })

        dictionary = {};
        for index, row in pandas.iterrows():
            exchangeInfo = ExchangeInfo(row, code)
            
            key = exchangeInfo.timestamp.strftime("%Y-%m-%d");
            if key not in dictionary:
                dictionary[key] = exchangeInfo;

            value: ExchangeInfo = dictionary[key]
            if value.timestamp == exchangeInfo.timestamp:
                continue;

            value.volume += exchangeInfo.volume
            value.close = exchangeInfo.close
            if exchangeInfo.high > value.high:
                value.high = exchangeInfo.high;
            if value.low > exchangeInfo.low:
                value.low = exchangeInfo.low;

        for key in dictionary:
            collection.insert_one(dictionary[key].__dict__)
