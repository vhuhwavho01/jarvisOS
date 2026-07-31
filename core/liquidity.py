class Liquidity:

    def find(self, df):

        result = {

            "buy_side": None,

            "sell_side": None,

            "signal": "NONE"

        }

        try:

            recent = df.tail(50)

            buy_price = recent.High.max()

            sell_price = recent.Low.min()

            result["buy_side"] = {

                "price": buy_price

            }

            result["sell_side"] = {

                "price": sell_price

            }

            price = recent.Close.iloc[-1]

            if price > buy_price:

                result["signal"] = "BUY"

            elif price < sell_price:

                result["signal"] = "SELL"

            return result

        except Exception:

            return result