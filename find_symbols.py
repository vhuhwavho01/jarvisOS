import MetaTrader5 as mt5

if not mt5.initialize():
    print("Failed to connect to MT5")
    quit()

print("=" * 60)
print("AVAILABLE GOLD SYMBOLS")
print("=" * 60)

symbols = mt5.symbols_get()

for symbol in symbols:
    name = symbol.name.upper()

    if "XAU" in name or "GOLD" in name:
        print(symbol.name)

mt5.shutdown()