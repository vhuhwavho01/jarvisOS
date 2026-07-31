from core.mt5_connector import MT5Connector
from core.indicators import Indicators
from core.smart_money import SmartMoney

mt = MT5Connector()

if not mt.connect():
    print("Failed to connect to MT5")
    quit()

rates = mt.get_rates()

df = Indicators.to_dataframe(rates)

snapshot = SmartMoney.snapshot(df)

print("=" * 60)
print("SMART MONEY TEST")
print("=" * 60)

for key, value in snapshot.items():
    print(f"{key:15}: {value}")

mt.disconnect()