from strategies.strategy import Strategy

class Backtester:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
