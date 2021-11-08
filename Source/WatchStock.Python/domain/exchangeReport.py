from datetime import datetime
from domain.priceStatus import PriceStatus

class ExchangeReport():
    def __init__(self, code):
        self.code = code;
        self.priceStatus = PriceStatus.Empty;
        self.priceSpan = 0;