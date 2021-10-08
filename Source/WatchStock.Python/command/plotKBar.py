#!python
#cython: language_level=3

from matplotlib.pyplot import savefig
from domain.kBar import KBar
from sentry_sdk.api import start_span

from config import Config
from pymongo import MongoClient
from datetime import date, timedelta, tzinfo

import pandas as pd
import mplfinance as mpf

import datetime


class PlotKBar():
    def __init__(self, config: Config, args):
        self.config = config
        self.name = "PlotKBar"
        self.stockNumber = args[1]
        self.start: datetime = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        self.end: datetime = datetime.datetime.strptime(
            args[3], "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)

    def execution(self):
        config = self.config
        stockNumber = self.stockNumber
        start = self.start
        end = self.end

        mongoClient = MongoClient(config.mongodbUri)
        database = mongoClient[config.mongodbDataBase]
        collection = database.KBar

        cursor = collection.find({
            "stockNumber": stockNumber,
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

        mpf.plot(pandas, savefig='./plot/{stockNumber}-{start}-{end}.jpg'.format(
            stockNumber=stockNumber, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d")), type='candle')
