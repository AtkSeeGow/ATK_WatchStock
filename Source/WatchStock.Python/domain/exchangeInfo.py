from datetime import datetime

class ExchangeInfo():
    def __init__(self, row, code):
        self.high = row['High']
        self.low = row['Low']
        self.open = row['Open']
        self.close = row['Close']
        self.volume = row['Volume']
        self.timestamp: datetime = row['ts']
        self.code = code
