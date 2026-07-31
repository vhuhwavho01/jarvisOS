from core.mt5_connector import MT5Connector
from core.indicators import Indicators
from core.strategy_engine import StrategyEngine

mt = MT5Connector()

if not mt.connect():
    print("Failed to connect to MT5")
    quit()

rates = mt.get_rates()

df = Indicators.to_dataframe(rates)

engine = StrategyEngine()

result = engine.analyze(df)

print("=" * 60)
print("JARVIS STRATEGY ENGINE")
print("=" * 60)

print(f"Signal      : {result['signal']}")
print(f"Confidence  : {result['confidence']}%")
print(f"Trend       : {result['trend']}")
print(f"Structure   : {result['structure']}")
print(f"EMA20       : {result['ema20']}")
print(f"EMA50       : {result['ema50']}")
print(f"EMA200      : {result['ema200']}")
print(f"RSI         : {result['rsi']}")
print(f"MACD        : {result['macd']}")

print("\nReasons:")
for reason in result["reasons"]:
    print(f"• {reason}")

mt.disconnect()