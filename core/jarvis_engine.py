from core.data_manager import DataManager
from core.indicators import Indicators
from core.session_filter import SessionFilter
from core.news_service import NewsService
from core.risk_manager import RiskManager
from core.institutional_filter import InstitutionalFilter
from core.confluence import Confluence


class JarvisEngine:

    def __init__(self):

        self.data = DataManager()
        self.indicators = Indicators()
        self.session = SessionFilter()
        self.news = NewsService()
        self.risk = RiskManager()
        self.institutional = InstitutionalFilter()
        self.confluence = Confluence()

        try:
            self.news.update()
        except Exception:
            pass

    # =====================================================

    def empty_result(self, message=""):

        return {

            "status": False,

            "symbol": "XAUUSD",

            "signal": "WAIT",

            "confidence": 0,

            "grade": "N/A",

            "score": 0,

            "entry": 0.0,

            "stop_loss": 0.0,

            "take_profit": 0.0,

            "risk_reward": 0,

            "reasons": [],

            "institutional": {},

            "message": message

        }

    # =====================================================

    def analyze(self):

        try:

            df = self.data.get_dataframe()

            if df is None:
                return self.empty_result("No market data.")

            if len(df) < 250:
                return self.empty_result("Not enough candles.")

            return self.analyze_dataframe(df)

        except Exception as e:

            return self.empty_result(str(e))

    # =====================================================

    def analyze_dataframe(self, df):

        try:

            self.confluence.reset()

            institutional = self.institutional.analyze(df)

            ema50 = self.indicators.ema(df, 50).iloc[-1]
            ema200 = self.indicators.ema(df, 200).iloc[-1]

            rsi = self.indicators.rsi(df).iloc[-1]

            macd, signal = self.indicators.macd(df)

            atr = self.indicators.atr(df).iloc[-1]

            price = float(df.Close.iloc[-1])

            # Session

            allowed = self.session.trading_allowed()

            self.confluence.add(
                allowed,
                20,
                "Trading Session"
            )

            self.confluence.subtract(
                not allowed,
                40,
                "Outside Session"
            )

            # News

            self.confluence.subtract(
                self.news.high_impact_active(),
                50,
                "High Impact News"
            )

            # EMA

            self.confluence.add(
                ema50 > ema200,
                20,
                "EMA Bullish"
            )

            self.confluence.subtract(
                ema50 < ema200,
                20,
                "EMA Bearish"
            )

            # RSI

            self.confluence.add(
                rsi < 30,
                15,
                "RSI Oversold"
            )

            self.confluence.subtract(
                rsi > 70,
                15,
                "RSI Overbought"
            )

            # MACD

            self.confluence.add(
                macd.iloc[-1] > signal.iloc[-1],
                15,
                "Bullish MACD"
            )

            self.confluence.subtract(
                macd.iloc[-1] < signal.iloc[-1],
                15,
                "Bearish MACD"
            )

            # Institutional

            if institutional.get("signal") == "BUY":

                self.confluence.add(
                    True,
                    institutional.get("score", 0),
                    "Institutional BUY"
                )

            elif institutional.get("signal") == "SELL":

                self.confluence.subtract(
                    True,
                    abs(institutional.get("score", 0)),
                    "Institutional SELL"
                )

            summary = self.confluence.summary()

            rr = self.risk.calculate(

                summary["signal"],

                price,

                atr

            )

            return {

                "status": True,

                "symbol": "XAUUSD",

                "signal": summary["signal"],

                "confidence": summary["confidence"],

                "grade": summary["grade"],

                "score": summary["score"],

                "entry": rr["entry"],

                "stop_loss": rr["stop_loss"],

                "take_profit": rr["take_profit"],

                "risk_reward": rr["risk_reward"],

                "reasons": summary["reasons"],

                "institutional": institutional,

                "message": ""

            }

        except Exception as e:

            return self.empty_result(str(e))