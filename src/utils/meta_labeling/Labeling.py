import jsonpickle
import numpy as np
import pandas as pd
from strategies.strategy import Strategy
from backtesting.backtester import Backtester
from sklearn.ensemble import RandomForestClassifier

class Labeler:
    def __init__(self, strategy: Strategy = None, model_path = None, save_model_path = None, training_data = None):
        assert strategy is not None or model_path is not None
        if model_path:
            with open(model_path + "buy_model.json", "r") as f:
                self.buy_model = jsonpickle.decode(f.read())
            with open(model_path + "sell_model.json", "r") as f:
                self.sell_model = jsonpickle.decode(f.read())
        else:
            backtester = Backtester(strategy, training_data)

            backtester.run_test()
            
            backtester.trades_df.to_csv("src/data/trades_normalization/trades.csv")

            self.trade_data = backtester.trades_df.copy()

            for i in self.trade_data["return"].index:
                if self.trade_data.loc[i, "return"] > 0:
                    self.trade_data.loc[i, "return"] = 1
                else:
                    self.trade_data.loc[i, "return"] = 0

            self.trade_data["open_price"] = self.normalize_data(self.trade_data["open_price"])
            self.trade_data["close_price"] = self.normalize_data(self.trade_data["close_price"])
            self.trade_data["adx"] = self.normalize_data(self.trade_data["adx"])
            self.trade_data["ema_24_100_diff"] = self.normalize_data(self.trade_data["ema_24_100_diff"])
            self.trade_data["support_trendline_slope"] = self.normalize_data(self.trade_data["support_trendline_slope"])
            self.trade_data["resist_trendline_slope"] = self.normalize_data(self.trade_data["resist_trendline_slope"])
            self.trade_data["ema50_slope"] = self.normalize_data(self.trade_data["ema50_slope"])
            self.trade_data["atr"] = self.normalize_data(self.trade_data["atr"])

            self.buy_trades = self.trade_data[self.trade_data["order_type"] == "buy"]
            self.sell_trades = self.trade_data[self.trade_data["order_type"] == "sell"]

            features = ["adx", "ema_24_100_diff", "support_trendline_slope", "resist_trendline_slope", "ema50_slope", "atr", "rsi"]

            # print(self.buy_trades["return"].iloc[:, -1].values.reshape(-1, 1))

            X_buy = pd.DataFrame(self.buy_trades[features].iloc[:, :-1]).values
            y_buy = pd.DataFrame(self.buy_trades["return"]).iloc[:, -1].values.reshape(-1, 1)

            self.buy_model = RandomForestClassifier(
                n_estimators=1000,
                criterion="entropy",
                min_samples_split=10,
                max_depth=14,
                random_state=69420
            )

            self.buy_model.fit(X_buy, y_buy)

            X_sell = pd.DataFrame(self.sell_trades[features].iloc[:, :-1]).values
            y_sell = pd.DataFrame(self.sell_trades["return"]).iloc[:, -1].values.reshape(-1, 1)

            self.sell_model = RandomForestClassifier(
                n_estimators=1000,
                criterion="entropy",
                min_samples_split=10,
                max_depth=14,
                random_state=69420
            )

            self.sell_model.fit(X_sell, y_sell)

        if save_model_path:
            with open(save_model_path + "buy_model.json", "w") as f:
                f.write(jsonpickle.encode(self.buy_model))
            with open(save_model_path + "sell_model.json", "w") as f:
                f.write(jsonpickle.encode(self.sell_model))

    def normalize_data(self, data):
        # Ensure data is a NumPy array
        data = np.array(data)

        # Calculate mean and std
        data_mean = np.mean(data)
        data_std = np.std(data)

        # Normalize between -1 and 1
        normalized_data = (data - data_mean) / (data_std)
        return normalized_data
    
    def predict(self, data: pd.DataFrame, model_type):
        data = data[["adx", "ema_24_100_diff", "support_trendline_slope", "resist_trendline_slope", "ema50_slope", "atr", "rsi"]]

        return self.buy_model.predict(data.iloc[:, :-1].values) if model_type == "buy" else self.sell_model.predict(data.iloc[:, :-1].values)

    def predict_proba(self, data: pd.DataFrame, model_type):
        data = data[["adx", "ema_24_100_diff", "support_trendline_slope", "resist_trendline_slope", "ema50_slope", "atr", "rsi"]]

        return self.buy_model.predict_proba(data.iloc[:, :-1].values) if model_type == "buy" else self.sell_model.predict_proba(data.iloc[:, :-1].values)