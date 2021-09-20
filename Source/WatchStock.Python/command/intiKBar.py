#!python
#cython: language_level=3

from domain.kBar import KBar
from sentry_sdk.api import start_span
from config import Config

from datetime import date, timedelta
from pymongo import MongoClient

import shioaji as sj
import pandas as pd
import datetime


class IntiKBar():
    def __init__(self, config: Config, start: datetime, end: datetime, args):
        self.config = config
        self.name = "IntiKBar"
        self.stockNumber = args[1]
        self.start = start
        self.end = end

    def execution(self):
        config = self.config
        stockNumber = self.stockNumber
        start = self.start
        end = self.end
        api = sj.Shioaji()

        mongoClient = MongoClient(config.mongodbUri)
        database = mongoClient[config.mongodbDataBase]
        collection = database.KBar

        accounts = api.login(config.account, config.password)
        contract = api.Contracts.Stocks[stockNumber]
        kbars = api.kbars(contract, start=start.strftime(
            "%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))

        pandas = pd.DataFrame({**kbars})
        pandas.ts = pd.to_datetime(pandas.ts)

        collection.delete_many({
            "stockNumber": stockNumber,
            "timestamp": {
                "$gte": start,
                "$lt": end
            }
        })

        for index, row in pandas.iterrows():
            kbar = KBar(row, stockNumber)
            collection.insert_one(kbar.__dict__)
