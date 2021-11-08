#!python
#cython: language_level=3

import sys

from command.initExchangeInfo import InitExchangeInfo
from command.initExchangeReport import InitExchangeReport
from command.plotCandle import PlotCandle
from config import Config

if __name__ == "__main__":
    config = Config()

    args = sys.argv[1:]

    commands = []
    commands.append(InitExchangeInfo(config))
    commands.append(PlotCandle(config))
    commands.append(InitExchangeReport(config))

    for command in commands:
        if command.name == args[0]:
            command.execution(args);