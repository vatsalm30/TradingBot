class Labeling:
    def __init__(self, label: str, features: list[str]):
        self.trade_data = pd.read_csv("src/data/trades.csv")