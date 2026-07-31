import pandas as pd


class OrderBlocks:

    def find(self, df):

        result = {

            "nearest": None,

            "blocks": []

        }

        try:

            for i in range(2, len(df) - 2):

                candle = df.iloc[i]

                previous = df.iloc[i - 1]

                nxt = df.iloc[i + 1]

                # Bullish Order Block

                if previous.Close < previous.Open and \
                   nxt.Close > candle.High:

                    block = {

                        "type": "BULLISH",

                        "high": previous.High,

                        "low": previous.Low,

                        "index": i

                    }

                    result["blocks"].append(block)

                # Bearish Order Block

                if previous.Close > previous.Open and \
                   nxt.Close < candle.Low:

                    block = {

                        "type": "BEARISH",

                        "high": previous.High,

                        "low": previous.Low,

                        "index": i

                    }

                    result["blocks"].append(block)

            if result["blocks"]:

                result["nearest"] = result["blocks"][-1]

            return result

        except Exception:

            return result