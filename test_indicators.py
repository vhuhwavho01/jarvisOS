from core.mt5_connector import MT5Connector
from core.indicators import Indicators

mt = MT5Connector()

if mt.connect():

    rates = mt.get_rates()

    df = Indicators.to_dataframe(rates)

    data = Indicators.snapshot(df)

    print("=" * 60)
    print("JARVIS INDICATOR TEST")
    print("=" * 60)

    for key, value in data.items():
        print(f"{key:12}: {value}")

    mt.disconnect()

else:

    print("Failed to connect to MT5")