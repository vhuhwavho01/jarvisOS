from core.mt5_connector import MT5Connector
from core.indicators import Indicators
from core.market_structure import MarketStructure

mt = MT5Connector()

if not mt.connect():
    print("Failed to connect")
    quit()

rates = mt.get_rates()

df = Indicators.to_dataframe(rates)

engine = MarketStructure()

result = engine.snapshot(df)

print("=" * 60)
print("MARKET STRUCTURE TEST")
print("=" * 60)

print("Trend:", result["trend"])
print("Swings:", result["swings"])

print("\nLatest Structure:")

for item in result["last_structure"]:
    print(item)

mt.disconnect()