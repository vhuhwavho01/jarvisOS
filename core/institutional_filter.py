from core.market_structure import MarketStructure
from core.order_blocks import OrderBlocks
from core.fair_value_gap import FairValueGap
from core.liquidity import Liquidity
from core.market_regime import MarketRegime


class InstitutionalFilter:

    def __init__(self):

        self.structure = MarketStructure()
        self.order_blocks = OrderBlocks()
        self.fvg = FairValueGap()
        self.liquidity = Liquidity()
        self.regime = MarketRegime()

    # =====================================================

    def analyze(self, df):

        result = {

            "signal": "WAIT",

            "score": 0,

            "structure": {

                "trend": "RANGE"

            },

            "order_blocks": {

                "nearest": None,

                "blocks": []

            },

            "fair_value_gap": {

                "nearest": None,

                "gaps": []

            },

            "liquidity": {

                "signal": "NONE"

            },

            "market_regime": {

                "regime": "RANGE",

                "strength": 0,

                "volatility": 0,

                "trend": "RANGE"

            }

        }

        try:

            structure = self.structure.analyze(df) or result["structure"]

            order_blocks = self.order_blocks.find(df) or result["order_blocks"]

            fvg = self.fvg.find(df) or result["fair_value_gap"]

            liquidity = self.liquidity.find(df) or result["liquidity"]

            regime = self.regime.detect(df) or result["market_regime"]

            result["structure"] = structure
            result["order_blocks"] = order_blocks
            result["fair_value_gap"] = fvg
            result["liquidity"] = liquidity
            result["market_regime"] = regime

            score = 0

            trend = structure.get("trend", "RANGE")

            if trend == "BULLISH":
                score += 25
            elif trend == "BEARISH":
                score -= 25

            nearest_ob = order_blocks.get("nearest")

            if nearest_ob:

                if nearest_ob.get("type") == "BULLISH":
                    score += 20
                elif nearest_ob.get("type") == "BEARISH":
                    score -= 20

            nearest_fvg = fvg.get("nearest")

            if nearest_fvg:

                if nearest_fvg.get("type") == "BULLISH":
                    score += 15
                elif nearest_fvg.get("type") == "BEARISH":
                    score -= 15

            liquidity_signal = liquidity.get("signal", "NONE")

            if liquidity_signal == "BUY":
                score += 20
            elif liquidity_signal == "SELL":
                score -= 20

            if regime.get("regime") == "TREND":
                score = int(score * 1.2)
            else:
                score = int(score * 0.8)

            result["score"] = score

            if score >= 40:
                result["signal"] = "BUY"
            elif score <= -40:
                result["signal"] = "SELL"
            else:
                result["signal"] = "WAIT"

            return result

        except Exception as e:

            result["error"] = str(e)

            return result