from core.jarvis_engine import JarvisEngine

engine = JarvisEngine()

result = engine.analyze_gold()

print("=" * 60)
print("JARVIS AI")
print("=" * 60)

if result["status"]:

    print(f"Symbol      : {result['symbol']}")
    print(f"Price       : {result['price']}")
    print(f"Trend       : {result['trend']}")
    print(f"Structure   : {result['structure']}")
    print(f"Signal      : {result['signal']}")
    print(f"Confidence  : {result['confidence']}%")

    print()

    print(f"Entry        : {result['entry']}")
    print(f"Stop Loss    : {result['stop_loss']}")
    print(f"Take Profit  : {result['take_profit']}")
    print(f"Risk Reward  : 1:{result['risk_reward']}")

    print("\nReasons:")

    for reason in result["reasons"]:
        print(f"✓ {reason}")

else:

    print(result["message"])