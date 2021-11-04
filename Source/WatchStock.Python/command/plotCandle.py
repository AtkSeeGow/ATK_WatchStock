#!python
#cython: language_level=3

from matplotlib.pyplot import savefig
from domain.exchangeInfo import ExchangeInfo
from sentry_sdk.api import start_span
from config import Config
from pymongo import MongoClient
from datetime import date, timedelta, tzinfo

import datetime
import pandas as pd
import mplfinance as mpf

class PlotCandle():
    def __init__(self, config: Config):
        self.config = config
        self.name = "PlotCandle"

    def execution(self, args):
        config = self.config
        number = args[1]
        start: datetime = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        end : datetime = datetime.datetime.strptime(
            args[3], "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)

        mongoClient = MongoClient(config.mongodbUri)
        database = mongoClient[config.mongodbDataBase]
        collection = database.ExchangeInfo

        cursor = collection.find({
            "number": number,
            "timestamp": {
                "$gte": start,
                "$lt": end
            }
        })

        kBars = list(cursor)
        pandas = pd.DataFrame(kBars)
        pandas.index = pandas['timestamp']
        pandas = pandas.rename(columns={'open': 'Open',
                               'high': 'High',
                                        'low': 'Low',
                                        'close': 'Close',
                                        'volume': 'Volume'})

        mpf.plot(pandas, savefig='./Plot/{number}-{start}-{end}.jpg'.format(
            number=number, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d")), type='candle')
