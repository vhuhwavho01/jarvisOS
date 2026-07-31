class FairValueGap:

    def find(self, df):

        result = {

            "nearest": None,

            "gaps": []

        }

        try:

            for i in range(2, len(df)):

                c1 = df.iloc[i - 2]
                c2 = df.iloc[i - 1]
                c3 = df.iloc[i]

                # Bullish FVG
                if c1.High < c3.Low:

                    result["gaps"].append({

                        "type": "BULLISH",

                        "high": c3.Low,

                        "low": c1.High,

                        "index": i

                    })

                # Bearish FVG
                elif c1.Low > c3.High:

                    result["gaps"].append({

                        "type": "BEARISH",

                        "high": c1.Low,

                        "low": c3.High,

                        "index": i

                    })

            if result["gaps"]:

                result["nearest"] = result["gaps"][-1]

            return result

        except Exception:

            return result