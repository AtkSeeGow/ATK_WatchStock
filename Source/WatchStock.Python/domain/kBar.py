class KBar():
    def __init__(self, row, stockNumber):
        self.high = row['High'];
        self.low = row['Low'];
        self.open = row['Open'];
        self.close = row['Close'];
        self.volume = row['Volume'];
        self.timestamp = row['ts'];
        self.stockNumber = stockNumber;
