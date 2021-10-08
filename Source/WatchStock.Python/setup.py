#!python
#cython: language_level=3

from command.plotKBar import PlotKBar
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
    commands.append(IntiKBar(config, args))
    commands.append(PlotKBar(config, args))

    for command in commands:
        if command.name == args[0]:
            command.execution();
