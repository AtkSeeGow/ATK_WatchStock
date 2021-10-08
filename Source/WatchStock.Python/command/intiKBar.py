#!python
#cython: language_level=3

from shioaji.data import Kbars
from domain.kBar import KBar
from config import Config

from datetime import date, timedelta, tzinfo
from pymongo import MongoClient

import shioaji as sj
import pandas as pd

import datetime

class IntiKBar():
    def __init__(self, config: Config, args):
        self.config = config
        self.name = "IntiKBar"
        self.stockNumber = args[1]
        self.start: datetime = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        self.end: datetime = datetime.datetime.strptime(
            args[3], "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)

    def execution(self):
        config = self.config
        stockNumber = self.stockNumber
        start = self.start
        end = self.end
        api = sj.Shioaji()

        mongoClient = MongoClient(config.mongodbUri, tz_aware='true')
        database = mongoClient[config.mongodbDataBase]
        collection = database.KBar

        accounts = api.login(config.account, config.password)
        contract = api.Contracts.Stocks[stockNumber]
        kBars = api.kbars(contract, start=start.strftime(
            "%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))

        pandas = pd.DataFrame({**kBars})
        pandas.ts = pd.to_datetime(pandas.ts)
        pandas = pandas.sort_values(by=['ts'], ascending=True)
        
        collection.delete_many({
            "stockNumber": stockNumber,
            "timestamp": {
                "$gte": start,
                "$lt": end
            }
        })

        dictionary = {};
        for index, row in pandas.iterrows():
            kBar = KBar(row, stockNumber)
            
            key = kBar.timestamp.strftime("%Y-%m-%d");
            if key not in dictionary:
                dictionary[key] = kBar;

            value: KBar = dictionary[key]
            if value.timestamp == kBar.timestamp:
                continue;

            value.volume += kBar.volume
            value.close = kBar.close
            if kBar.high > value.high:
                value.high = kBar.high;
            if value.low > kBar.low:
                value.low = kBar.low;

        for key in dictionary:
            collection.insert_one(dictionary[key].__dict__)
