#!python
#cython: language_level=3

from command.intiKBar import IntiKBar
from config import Config

from datetime import date, timedelta

import shioaji as sj
import pandas as pd
import datetime
import sys

if __name__ == "__main__":
    config = Config()

    args = sys.argv[1:]

    commands = []
    commands.append(IntiKBar(config, datetime.datetime(2020, 1, 1), datetime.datetime.now(), args))

    for command in commands:
        if command.name == args[0]:
            command.execution();

    start_date = date(2013, 1, 1)
    for n in range(int((date(2015, 6, 2) - start_date).days)):
        print((start_date + timedelta(n)).strftime("%Y-%m-%d"))
