from core.mt5_connector import MT5Connector

print("=" * 60)
print("        JARVIS MT5 CONNECTION TEST")
print("=" * 60)

mt = MT5Connector()

if not mt.connect():

    print("\n❌ Could not connect to MT5")

    quit()

print("\n✅ Connected Successfully")

print(f"\nDetected Gold Symbol : {mt.symbol}")

account = mt.account_info()

if account:

    print("\nACCOUNT INFORMATION")
    print("----------------------------")
    print(f"Broker  : {account.company}")
    print(f"Login   : {account.login}")
    print(f"Balance : {account.balance}")
    print(f"Equity  : {account.equity}")

tick = mt.get_tick()

if tick:

    print("\nLIVE MARKET")
    print("----------------------------")
    print(f"Bid : {tick.bid}")
    print(f"Ask : {tick.ask}")
    print(f"Spread : {(tick.ask - tick.bid):.3f}")

else:

    print("\n❌ No live market data received.")

rates = mt.get_rates()

if rates is not None:

    print(f"\nDownloaded {len(rates)} candles successfully.")

else:

    print("\n❌ Failed to download candle history.")

mt.disconnect()

print("\nMT5 connection closed.")