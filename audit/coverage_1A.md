# 1A coverage matrices

Cell = Greek | driver | direction | call/put | moneyness | long/short. 'Answer' is the engine-verified direction for the conditions found (same direction for a small and a large shock). L1 answers are about the SIZE of the Greek; L2 answers are signed.

## Level 1: 360/360 cells producible (16 resolve to 'roughly unchanged')

| Cell | Producible | Conditions found | Answer |
|---|---|---|---|
| delta|spot|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 1.0 | grows in size |
| delta|spot|up|C|ITM|short | yes | EURUSD 1Y 85d, shock 1.0 | grows in size |
| delta|spot|up|C|ATM|long | yes | GBPUSD 1M ATM, shock 1.0 | grows in size |
| delta|spot|up|C|ATM|short | yes | NZDUSD 1M ATM, shock 1.0 | grows in size |
| delta|spot|up|C|OTM|long | yes | NZDUSD 1Y 10d, shock 1.0 | grows in size |
| delta|spot|up|C|OTM|short | yes | GBPUSD 1Y 25d, shock 1.0 | grows in size |
| delta|spot|up|P|ITM|long | yes | AUDUSD 1M 85d, shock 1.0 | shrinks in size |
| delta|spot|up|P|ITM|short | yes | EURUSD 3M 75d, shock 1.0 | shrinks in size |
| delta|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | shrinks in size |
| delta|spot|up|P|ATM|short | yes | AUDUSD 1Y ATM, shock 1.0 | shrinks in size |
| delta|spot|up|P|OTM|long | yes | GBPUSD 3M 10d, shock 1.0 | shrinks in size |
| delta|spot|up|P|OTM|short | yes | GBPUSD 6M 10d, shock 1.0 | shrinks in size |
| delta|spot|down|C|ITM|long | yes | EURUSD 1Y 85d, shock 1.0 | shrinks in size |
| delta|spot|down|C|ITM|short | yes | NZDUSD 1Y 75d, shock 1.0 | shrinks in size |
| delta|spot|down|C|ATM|long | yes | NZDUSD 1M ATM, shock 1.0 | shrinks in size |
| delta|spot|down|C|ATM|short | yes | GBPUSD 6M ATM, shock 1.0 | shrinks in size |
| delta|spot|down|C|OTM|long | yes | EURUSD 1M 15d, shock 1.0 | shrinks in size |
| delta|spot|down|C|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | shrinks in size |
| delta|spot|down|P|ITM|long | yes | GBPUSD 1Y 75d, shock 1.0 | grows in size |
| delta|spot|down|P|ITM|short | yes | GBPUSD 1M 75d, shock 1.0 | grows in size |
| delta|spot|down|P|ATM|long | yes | EURUSD 3M ATM, shock 1.0 | grows in size |
| delta|spot|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 1.0 | grows in size |
| delta|spot|down|P|OTM|long | yes | NZDUSD 1Y 25d, shock 1.0 | grows in size |
| delta|spot|down|P|OTM|short | yes | AUDUSD 1Y 10d, shock 1.0 | grows in size |
| delta|time|up|C|ITM|long | yes | GBPUSD 6M 75d, shock 2.0 | shrinks in size |
| delta|time|up|C|ITM|short | yes | EURUSD 3M 85d, shock 2.0 | shrinks in size |
| delta|time|up|C|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | grows in size |
| delta|time|up|C|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | grows in size |
| delta|time|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 2.0 | grows in size |
| delta|time|up|C|OTM|short | yes | EURUSD 3M 25d, shock 2.0 | grows in size |
| delta|time|up|P|ITM|long | yes | NZDUSD 1M 85d, shock 2.0 | shrinks in size |
| delta|time|up|P|ITM|short | yes | AUDUSD 3M 85d, shock 2.0 | shrinks in size |
| delta|time|up|P|ATM|long | yes | AUDUSD 3M ATM, shock 2.0 | shrinks in size |
| delta|time|up|P|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | shrinks in size |
| delta|time|up|P|OTM|long | yes | AUDUSD 6M 10d, shock 2.0 | grows in size |
| delta|time|up|P|OTM|short | yes | AUDUSD 6M 15d, shock 2.0 | grows in size |
| delta|time|down|C|ITM|long | yes | GBPUSD 6M 85d, shock 0.5 | grows in size |
| delta|time|down|C|ITM|short | yes | EURUSD 1Y 75d, shock 0.5 | grows in size |
| delta|time|down|C|ATM|long | yes | NZDUSD 1M ATM, shock 0.5 | shrinks in size |
| delta|time|down|C|ATM|short | yes | EURUSD 1M ATM, shock 0.5 | shrinks in size |
| delta|time|down|C|OTM|long | yes | GBPUSD 6M 25d, shock 0.5 | shrinks in size |
| delta|time|down|C|OTM|short | yes | EURUSD 6M 25d, shock 0.5 | shrinks in size |
| delta|time|down|P|ITM|long | yes | NZDUSD 1M 75d, shock 0.5 | grows in size |
| delta|time|down|P|ITM|short | yes | GBPUSD 1M 85d, shock 0.5 | grows in size |
| delta|time|down|P|ATM|long | yes | AUDUSD 6M ATM, shock 0.5 | grows in size |
| delta|time|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 0.5 | grows in size |
| delta|time|down|P|OTM|long | yes | GBPUSD 6M 25d, shock 0.5 | shrinks in size |
| delta|time|down|P|OTM|short | yes | GBPUSD 6M 10d, shock 0.5 | shrinks in size |
| delta|vol|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 2.0 | shrinks in size |
| delta|vol|up|C|ITM|short | yes | NZDUSD 6M 75d, shock 2.0 | shrinks in size |
| delta|vol|up|C|ATM|long | yes | GBPUSD 1Y ATM, shock 4.0 | grows in size |
| delta|vol|up|C|ATM|short | yes | GBPUSD 1Y ATM, shock 4.0 | grows in size |
| delta|vol|up|C|OTM|long | yes | EURUSD 3M 25d, shock 2.0 | grows in size |
| delta|vol|up|C|OTM|short | yes | AUDUSD 3M 10d, shock 2.0 | grows in size |
| delta|vol|up|P|ITM|long | yes | NZDUSD 1W 85d, shock 2.0 | shrinks in size |
| delta|vol|up|P|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | shrinks in size |
| delta|vol|up|P|ATM|long | yes | EURUSD 1Y ATM, shock 3.0 | shrinks in size |
| delta|vol|up|P|ATM|short | yes | GBPUSD 1Y ATM, shock 4.0 | shrinks in size |
| delta|vol|up|P|OTM|long | yes | EURUSD 3M 10d, shock 2.0 | grows in size |
| delta|vol|up|P|OTM|short | yes | GBPUSD 3M 15d, shock 2.0 | grows in size |
| delta|vol|down|C|ITM|long | yes | AUDUSD 6M 75d, shock 2.0 | grows in size |
| delta|vol|down|C|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | grows in size |
| delta|vol|down|C|ATM|long | yes | NZDUSD 1Y ATM, shock 3.0 | shrinks in size |
| delta|vol|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 3.0 | shrinks in size |
| delta|vol|down|C|OTM|long | yes | GBPUSD 1Y 15d, shock 2.0 | shrinks in size |
| delta|vol|down|C|OTM|short | yes | NZDUSD 1W 10d, shock 2.0 | shrinks in size |
| delta|vol|down|P|ITM|long | yes | EURUSD 1M 75d, shock 2.0 | grows in size |
| delta|vol|down|P|ITM|short | yes | AUDUSD 1W 85d, shock 2.0 | grows in size |
| delta|vol|down|P|ATM|long | yes | NZDUSD 6M ATM, shock 4.0 | grows in size |
| delta|vol|down|P|ATM|short | yes | AUDUSD 1Y ATM, shock 3.0 | grows in size |
| delta|vol|down|P|OTM|long | yes | GBPUSD 1Y 15d, shock 2.0 | shrinks in size |
| delta|vol|down|P|OTM|short | yes | AUDUSD 6M 25d, shock 2.0 | shrinks in size |
| gamma|spot|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 1.0 | shrinks in size |
| gamma|spot|up|C|ITM|short | yes | AUDUSD 3M 75d, shock 1.0 | shrinks in size |
| gamma|spot|up|C|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | shrinks in size |
| gamma|spot|up|C|ATM|short | yes | EURUSD 3M ATM, shock 1.5 | shrinks in size |
| gamma|spot|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 1.0 | grows in size |
| gamma|spot|up|C|OTM|short | yes | EURUSD 1Y 15d, shock 1.0 | grows in size |
| gamma|spot|up|P|ITM|long | yes | NZDUSD 6M 75d, shock 1.0 | grows in size |
| gamma|spot|up|P|ITM|short | yes | EURUSD 3M 85d, shock 1.0 | grows in size |
| gamma|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | shrinks in size |
| gamma|spot|up|P|ATM|short | yes | NZDUSD 6M ATM, shock 3.0 | shrinks in size |
| gamma|spot|up|P|OTM|long | yes | EURUSD 6M 10d, shock 1.0 | shrinks in size |
| gamma|spot|up|P|OTM|short | yes | GBPUSD 6M 15d, shock 1.0 | shrinks in size |
| gamma|spot|down|C|ITM|long | yes | AUDUSD 3M 75d, shock 1.0 | grows in size |
| gamma|spot|down|C|ITM|short | yes | AUDUSD 1Y 75d, shock 1.0 | grows in size |
| gamma|spot|down|C|ATM|long | yes | EURUSD 1M ATM, shock 1.0 | shrinks in size |
| gamma|spot|down|C|ATM|short | yes | EURUSD 1W ATM, shock 1.0 | shrinks in size |
| gamma|spot|down|C|OTM|long | yes | GBPUSD 1M 25d, shock 1.0 | shrinks in size |
| gamma|spot|down|C|OTM|short | yes | NZDUSD 1Y 15d, shock 1.0 | shrinks in size |
| gamma|spot|down|P|ITM|long | yes | AUDUSD 1Y 75d, shock 1.0 | shrinks in size |
| gamma|spot|down|P|ITM|short | yes | NZDUSD 6M 85d, shock 1.0 | shrinks in size |
| gamma|spot|down|P|ATM|long | yes | AUDUSD 3M ATM, shock 2.0 | shrinks in size |
| gamma|spot|down|P|ATM|short | yes | AUDUSD 3M ATM, shock 2.0 | shrinks in size |
| gamma|spot|down|P|OTM|long | yes | AUDUSD 1M 15d, shock 1.0 | grows in size |
| gamma|spot|down|P|OTM|short | yes | GBPUSD 1Y 15d, shock 1.0 | grows in size |
| gamma|time|up|C|ITM|long | yes | EURUSD 1W 85d, shock 2.0 | shrinks in size |
| gamma|time|up|C|ITM|short | yes | AUDUSD 3M 85d, shock 2.0 | shrinks in size |
| gamma|time|up|C|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | shrinks in size |
| gamma|time|up|C|ATM|short | yes | AUDUSD 3M ATM, shock 2.0 | shrinks in size |
| gamma|time|up|C|OTM|long | yes | NZDUSD 3M 15d, shock 3.0 | shrinks in size |
| gamma|time|up|C|OTM|short | yes | EURUSD 1W 10d, shock 2.0 | grows in size |
| gamma|time|up|P|ITM|long | yes | NZDUSD 6M 75d, shock 2.0 | shrinks in size |
| gamma|time|up|P|ITM|short | yes | NZDUSD 1M 85d, shock 3.0 | shrinks in size |
| gamma|time|up|P|ATM|long | yes | GBPUSD 3M ATM, shock 2.0 | shrinks in size |
| gamma|time|up|P|ATM|short | yes | GBPUSD 6M ATM, shock 2.0 | shrinks in size |
| gamma|time|up|P|OTM|long | yes | NZDUSD 1W 15d, shock 2.0 | shrinks in size |
| gamma|time|up|P|OTM|short | yes | GBPUSD 3M 10d, shock 2.0 | grows in size |
| gamma|time|down|C|ITM|long | yes | GBPUSD 1M 85d, shock 0.5 | shrinks in size |
| gamma|time|down|C|ITM|short | yes | AUDUSD 6M 75d, shock 0.5 | grows in size |
| gamma|time|down|C|ATM|long | yes | AUDUSD 1M ATM, shock 0.5 | grows in size |
| gamma|time|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 0.5 | grows in size |
| gamma|time|down|C|OTM|long | yes | AUDUSD 1M 10d, shock 0.5 | shrinks in size |
| gamma|time|down|C|OTM|short | yes | GBPUSD 1W 10d, shock 0.5 | shrinks in size |
| gamma|time|down|P|ITM|long | yes | GBPUSD 6M 85d, shock 0.5 | shrinks in size |
| gamma|time|down|P|ITM|short | yes | EURUSD 1M 75d, shock 0.5 | grows in size |
| gamma|time|down|P|ATM|long | yes | AUDUSD 6M ATM, shock 0.5 | grows in size |
| gamma|time|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 0.5 | grows in size |
| gamma|time|down|P|OTM|long | yes | EURUSD 1Y 15d, shock 0.5 | grows in size |
| gamma|time|down|P|OTM|short | yes | NZDUSD 6M 25d, shock 0.5 | grows in size |
| gamma|vol|up|C|ITM|long | yes | NZDUSD 1W 75d, shock 2.0 | shrinks in size |
| gamma|vol|up|C|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | shrinks in size |
| gamma|vol|up|C|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | shrinks in size |
| gamma|vol|up|C|ATM|short | yes | NZDUSD 3M ATM, shock 2.0 | shrinks in size |
| gamma|vol|up|C|OTM|long | yes | NZDUSD 6M 10d, shock 2.0 | grows in size |
| gamma|vol|up|C|OTM|short | yes | EURUSD 1W 25d, shock 2.0 | shrinks in size |
| gamma|vol|up|P|ITM|long | yes | EURUSD 1Y 75d, shock 2.0 | shrinks in size |
| gamma|vol|up|P|ITM|short | yes | NZDUSD 6M 75d, shock 2.0 | shrinks in size |
| gamma|vol|up|P|ATM|long | yes | GBPUSD 1Y ATM, shock 2.0 | shrinks in size |
| gamma|vol|up|P|ATM|short | yes | NZDUSD 6M ATM, shock 2.0 | shrinks in size |
| gamma|vol|up|P|OTM|long | yes | EURUSD 1Y 25d, shock 2.0 | shrinks in size |
| gamma|vol|up|P|OTM|short | yes | GBPUSD 3M 15d, shock 3.0 | shrinks in size |
| gamma|vol|down|C|ITM|long | yes | NZDUSD 1W 75d, shock 2.0 | grows in size |
| gamma|vol|down|C|ITM|short | yes | GBPUSD 3M 85d, shock 2.0 | shrinks in size |
| gamma|vol|down|C|ATM|long | yes | NZDUSD 3M ATM, shock 2.0 | grows in size |
| gamma|vol|down|C|ATM|short | yes | EURUSD 1Y ATM, shock 2.0 | grows in size |
| gamma|vol|down|C|OTM|long | yes | AUDUSD 1W 15d, shock 2.0 | shrinks in size |
| gamma|vol|down|C|OTM|short | yes | GBPUSD 1M 10d, shock 2.0 | shrinks in size |
| gamma|vol|down|P|ITM|long | yes | EURUSD 1M 85d, shock 2.0 | shrinks in size |
| gamma|vol|down|P|ITM|short | yes | GBPUSD 1W 85d, shock 2.0 | shrinks in size |
| gamma|vol|down|P|ATM|long | yes | AUDUSD 1Y ATM, shock 2.0 | grows in size |
| gamma|vol|down|P|ATM|short | yes | NZDUSD 3M ATM, shock 2.0 | grows in size |
| gamma|vol|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 2.0 | grows in size |
| gamma|vol|down|P|OTM|short | yes | EURUSD 6M 15d, shock 2.0 | shrinks in size |
| theta|spot|up|C|ITM|long | yes | GBPUSD 1M 75d, shock 1.0 | shrinks in size |
| theta|spot|up|C|ITM|short | yes | NZDUSD 6M 85d, shock 1.0 | shrinks in size |
| theta|spot|up|C|ATM|long | yes | AUDUSD 1M ATM, shock 1.5 | shrinks in size |
| theta|spot|up|C|ATM|short | yes | AUDUSD 1M ATM, shock 1.5 | shrinks in size |
| theta|spot|up|C|OTM|long | yes | AUDUSD 1W 10d, shock 1.0 | grows in size |
| theta|spot|up|C|OTM|short | yes | GBPUSD 6M 10d, shock 1.0 | grows in size |
| theta|spot|up|P|ITM|long | yes | EURUSD 1W 85d, shock 1.0 | grows in size |
| theta|spot|up|P|ITM|short | yes | NZDUSD 3M 85d, shock 1.0 | grows in size |
| theta|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | shrinks in size |
| theta|spot|up|P|ATM|short | yes | GBPUSD 1W ATM, shock 1.0 | shrinks in size |
| theta|spot|up|P|OTM|long | yes | GBPUSD 1M 25d, shock 1.0 | shrinks in size |
| theta|spot|up|P|OTM|short | yes | NZDUSD 6M 10d, shock 1.0 | shrinks in size |
| theta|spot|down|C|ITM|long | yes | AUDUSD 6M 85d, shock 1.0 | grows in size |
| theta|spot|down|C|ITM|short | yes | EURUSD 1W 85d, shock 1.0 | grows in size |
| theta|spot|down|C|ATM|long | yes | AUDUSD 1M ATM, shock 1.0 | shrinks in size |
| theta|spot|down|C|ATM|short | yes | GBPUSD 1M ATM, shock 1.0 | shrinks in size |
| theta|spot|down|C|OTM|long | yes | AUDUSD 1M 25d, shock 1.0 | shrinks in size |
| theta|spot|down|C|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | shrinks in size |
| theta|spot|down|P|ITM|long | yes | AUDUSD 1W 85d, shock 1.0 | shrinks in size |
| theta|spot|down|P|ITM|short | yes | GBPUSD 3M 75d, shock 1.0 | shrinks in size |
| theta|spot|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 1.0 | shrinks in size |
| theta|spot|down|P|ATM|short | yes | EURUSD 1M ATM, shock 1.0 | shrinks in size |
| theta|spot|down|P|OTM|long | yes | NZDUSD 6M 10d, shock 1.0 | grows in size |
| theta|spot|down|P|OTM|short | yes | EURUSD 6M 15d, shock 1.0 | grows in size |
| theta|time|up|C|ITM|long | yes | NZDUSD 1W 85d, shock 2.0 | shrinks in size |
| theta|time|up|C|ITM|short | yes | NZDUSD 1W 85d, shock 2.0 | shrinks in size |
| theta|time|up|C|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | shrinks in size |
| theta|time|up|C|ATM|short | yes | NZDUSD 3M ATM, shock 2.0 | shrinks in size |
| theta|time|up|C|OTM|long | yes | NZDUSD 1W 15d, shock 3.0 | shrinks in size |
| theta|time|up|C|OTM|short | yes | AUDUSD 1M 25d, shock 2.0 | shrinks in size |
| theta|time|up|P|ITM|long | yes | GBPUSD 1M 75d, shock 2.0 | shrinks in size |
| theta|time|up|P|ITM|short | yes | AUDUSD 1M 85d, shock 3.0 | shrinks in size |
| theta|time|up|P|ATM|long | yes | GBPUSD 6M ATM, shock 2.0 | shrinks in size |
| theta|time|up|P|ATM|short | yes | AUDUSD 1M ATM, shock 2.0 | shrinks in size |
| theta|time|up|P|OTM|long | yes | NZDUSD 1M 15d, shock 2.0 | shrinks in size |
| theta|time|up|P|OTM|short | yes | EURUSD 1W 25d, shock 2.0 | shrinks in size |
| theta|time|down|C|ITM|long | yes | NZDUSD 1W 75d, shock 0.5 | grows in size |
| theta|time|down|C|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | grows in size |
| theta|time|down|C|ATM|long | yes | NZDUSD 6M ATM, shock 0.5 | grows in size |
| theta|time|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 0.5 | grows in size |
| theta|time|down|C|OTM|long | yes | GBPUSD 1W 10d, shock 0.5 | shrinks in size |
| theta|time|down|C|OTM|short | yes | NZDUSD 3M 15d, shock 0.5 | shrinks in size |
| theta|time|down|P|ITM|long | yes | GBPUSD 6M 75d, shock 0.5 | grows in size |
| theta|time|down|P|ITM|short | yes | EURUSD 1W 85d, shock 0.5 | shrinks in size |
| theta|time|down|P|ATM|long | yes | GBPUSD 1M ATM, shock 0.5 | grows in size |
| theta|time|down|P|ATM|short | yes | EURUSD 3M ATM, shock 0.5 | grows in size |
| theta|time|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 0.5 | grows in size |
| theta|time|down|P|OTM|short | yes | AUDUSD 3M 25d, shock 0.5 | grows in size |
| theta|vol|up|C|ITM|long | yes | GBPUSD 3M 75d, shock 2.0 | grows in size |
| theta|vol|up|C|ITM|short | yes | EURUSD 1Y 85d, shock 2.0 | grows in size |
| theta|vol|up|C|ATM|long | yes | AUDUSD 3M ATM, shock 2.0 | grows in size |
| theta|vol|up|C|ATM|short | yes | AUDUSD 1Y ATM, shock 2.0 | grows in size |
| theta|vol|up|C|OTM|long | yes | GBPUSD 1W 15d, shock 2.0 | grows in size |
| theta|vol|up|C|OTM|short | yes | EURUSD 1W 15d, shock 2.0 | grows in size |
| theta|vol|up|P|ITM|long | yes | GBPUSD 1M 85d, shock 2.0 | grows in size |
| theta|vol|up|P|ITM|short | yes | GBPUSD 1Y 85d, shock 2.0 | grows in size |
| theta|vol|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 2.0 | grows in size |
| theta|vol|up|P|ATM|short | yes | NZDUSD 1M ATM, shock 2.0 | grows in size |
| theta|vol|up|P|OTM|long | yes | NZDUSD 3M 15d, shock 2.0 | grows in size |
| theta|vol|up|P|OTM|short | yes | EURUSD 6M 25d, shock 2.0 | grows in size |
| theta|vol|down|C|ITM|long | yes | EURUSD 1M 75d, shock 2.0 | shrinks in size |
| theta|vol|down|C|ITM|short | yes | NZDUSD 1Y 85d, shock 2.0 | shrinks in size |
| theta|vol|down|C|ATM|long | yes | GBPUSD 1W ATM, shock 2.0 | shrinks in size |
| theta|vol|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 2.0 | shrinks in size |
| theta|vol|down|C|OTM|long | yes | AUDUSD 1W 10d, shock 2.0 | shrinks in size |
| theta|vol|down|C|OTM|short | yes | GBPUSD 1W 25d, shock 2.0 | shrinks in size |
| theta|vol|down|P|ITM|long | yes | NZDUSD 1Y 85d, shock 2.0 | grows in size |
| theta|vol|down|P|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | shrinks in size |
| theta|vol|down|P|ATM|long | yes | GBPUSD 1W ATM, shock 2.0 | shrinks in size |
| theta|vol|down|P|ATM|short | yes | EURUSD 3M ATM, shock 2.0 | shrinks in size |
| theta|vol|down|P|OTM|long | yes | AUDUSD 6M 15d, shock 2.0 | shrinks in size |
| theta|vol|down|P|OTM|short | yes | NZDUSD 3M 15d, shock 2.0 | shrinks in size |
| vega|spot|up|C|ITM|long | yes | EURUSD 1Y 75d, shock 1.0 | shrinks in size |
| vega|spot|up|C|ITM|short | yes | AUDUSD 1M 75d, shock 1.0 | shrinks in size |
| vega|spot|up|C|ATM|long | yes | EURUSD 1M ATM, shock 1.0 | shrinks in size |
| vega|spot|up|C|ATM|short | yes | EURUSD 1W ATM, shock 1.0 | shrinks in size |
| vega|spot|up|C|OTM|long | yes | NZDUSD 3M 15d, shock 1.0 | grows in size |
| vega|spot|up|C|OTM|short | yes | EURUSD 3M 10d, shock 1.0 | grows in size |
| vega|spot|up|P|ITM|long | yes | EURUSD 1M 75d, shock 1.0 | grows in size |
| vega|spot|up|P|ITM|short | yes | EURUSD 1Y 85d, shock 1.0 | grows in size |
| vega|spot|up|P|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | shrinks in size |
| vega|spot|up|P|ATM|short | yes | EURUSD 3M ATM, shock 2.0 | shrinks in size |
| vega|spot|up|P|OTM|long | yes | EURUSD 1M 10d, shock 1.0 | shrinks in size |
| vega|spot|up|P|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | shrinks in size |
| vega|spot|down|C|ITM|long | yes | AUDUSD 1M 75d, shock 1.0 | grows in size |
| vega|spot|down|C|ITM|short | yes | GBPUSD 3M 85d, shock 1.0 | grows in size |
| vega|spot|down|C|ATM|long | yes | AUDUSD 1Y ATM, shock 3.0 | shrinks in size |
| vega|spot|down|C|ATM|short | yes | GBPUSD 1W ATM, shock 1.0 | shrinks in size |
| vega|spot|down|C|OTM|long | yes | EURUSD 1M 25d, shock 1.0 | shrinks in size |
| vega|spot|down|C|OTM|short | yes | NZDUSD 3M 10d, shock 1.0 | shrinks in size |
| vega|spot|down|P|ITM|long | yes | GBPUSD 3M 85d, shock 1.0 | shrinks in size |
| vega|spot|down|P|ITM|short | yes | NZDUSD 1W 75d, shock 1.0 | shrinks in size |
| vega|spot|down|P|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | shrinks in size |
| vega|spot|down|P|ATM|short | yes | GBPUSD 1Y ATM, shock 2.0 | shrinks in size |
| vega|spot|down|P|OTM|long | yes | GBPUSD 3M 15d, shock 1.0 | grows in size |
| vega|spot|down|P|OTM|short | yes | NZDUSD 1W 15d, shock 1.0 | grows in size |
| vega|time|up|C|ITM|long | yes | GBPUSD 1M 75d, shock 2.0 | grows in size |
| vega|time|up|C|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | grows in size |
| vega|time|up|C|ATM|long | yes | AUDUSD 1M ATM, shock 2.0 | grows in size |
| vega|time|up|C|ATM|short | yes | NZDUSD 6M ATM, shock 2.0 | grows in size |
| vega|time|up|C|OTM|long | yes | GBPUSD 1W 25d, shock 2.0 | grows in size |
| vega|time|up|C|OTM|short | yes | AUDUSD 1M 15d, shock 2.0 | grows in size |
| vega|time|up|P|ITM|long | yes | GBPUSD 6M 85d, shock 2.0 | grows in size |
| vega|time|up|P|ITM|short | yes | GBPUSD 1M 75d, shock 2.0 | grows in size |
| vega|time|up|P|ATM|long | yes | GBPUSD 1W ATM, shock 2.0 | grows in size |
| vega|time|up|P|ATM|short | yes | AUDUSD 1M ATM, shock 2.0 | grows in size |
| vega|time|up|P|OTM|long | yes | EURUSD 1W 15d, shock 2.0 | grows in size |
| vega|time|up|P|OTM|short | yes | AUDUSD 6M 10d, shock 2.0 | grows in size |
| vega|time|down|C|ITM|long | yes | NZDUSD 1M 85d, shock 0.5 | shrinks in size |
| vega|time|down|C|ITM|short | yes | GBPUSD 6M 75d, shock 0.5 | shrinks in size |
| vega|time|down|C|ATM|long | yes | EURUSD 1M ATM, shock 0.5 | shrinks in size |
| vega|time|down|C|ATM|short | yes | EURUSD 1W ATM, shock 0.5 | shrinks in size |
| vega|time|down|C|OTM|long | yes | NZDUSD 6M 25d, shock 0.5 | shrinks in size |
| vega|time|down|C|OTM|short | yes | AUDUSD 1Y 15d, shock 0.5 | shrinks in size |
| vega|time|down|P|ITM|long | yes | AUDUSD 3M 85d, shock 0.5 | shrinks in size |
| vega|time|down|P|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | shrinks in size |
| vega|time|down|P|ATM|long | yes | NZDUSD 1M ATM, shock 0.5 | shrinks in size |
| vega|time|down|P|ATM|short | yes | GBPUSD 1M ATM, shock 0.5 | shrinks in size |
| vega|time|down|P|OTM|long | yes | EURUSD 1Y 25d, shock 0.5 | shrinks in size |
| vega|time|down|P|OTM|short | yes | GBPUSD 1Y 10d, shock 0.5 | shrinks in size |
| vega|vol|up|C|ITM|long | yes | GBPUSD 3M 75d, shock 2.0 | grows in size |
| vega|vol|up|C|ITM|short | yes | AUDUSD 1Y 85d, shock 2.0 | grows in size |
| vega|vol|up|C|ATM|long | yes | EURUSD 1M ATM, shock 2.0 | unchanged |
| vega|vol|up|C|ATM|short | yes | EURUSD 1Y ATM, shock 2.0 | unchanged |
| vega|vol|up|C|OTM|long | yes | EURUSD 1M 25d, shock 2.0 | grows in size |
| vega|vol|up|C|OTM|short | yes | EURUSD 1Y 15d, shock 2.0 | grows in size |
| vega|vol|up|P|ITM|long | yes | NZDUSD 3M 85d, shock 2.0 | grows in size |
| vega|vol|up|P|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | grows in size |
| vega|vol|up|P|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | unchanged |
| vega|vol|up|P|ATM|short | yes | GBPUSD 6M ATM, shock 2.0 | unchanged |
| vega|vol|up|P|OTM|long | yes | NZDUSD 1Y 10d, shock 2.0 | grows in size |
| vega|vol|up|P|OTM|short | yes | AUDUSD 1M 15d, shock 2.0 | grows in size |
| vega|vol|down|C|ITM|long | yes | NZDUSD 1M 85d, shock 2.0 | shrinks in size |
| vega|vol|down|C|ITM|short | yes | NZDUSD 1Y 75d, shock 2.0 | shrinks in size |
| vega|vol|down|C|ATM|long | yes | GBPUSD 6M ATM, shock 2.0 | unchanged |
| vega|vol|down|C|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | unchanged |
| vega|vol|down|C|OTM|long | yes | NZDUSD 1M 25d, shock 2.0 | shrinks in size |
| vega|vol|down|C|OTM|short | yes | GBPUSD 3M 15d, shock 2.0 | shrinks in size |
| vega|vol|down|P|ITM|long | yes | GBPUSD 6M 85d, shock 2.0 | shrinks in size |
| vega|vol|down|P|ITM|short | yes | GBPUSD 1W 75d, shock 2.0 | shrinks in size |
| vega|vol|down|P|ATM|long | yes | NZDUSD 1Y ATM, shock 2.0 | unchanged |
| vega|vol|down|P|ATM|short | yes | GBPUSD 1Y ATM, shock 2.0 | unchanged |
| vega|vol|down|P|OTM|long | yes | NZDUSD 1M 10d, shock 2.0 | shrinks in size |
| vega|vol|down|P|OTM|short | yes | GBPUSD 1M 25d, shock 2.0 | shrinks in size |
| rho|spot|up|C|ITM|long | yes | GBPUSD 1M 85d, shock 1.0 | grows in size |
| rho|spot|up|C|ITM|short | yes | AUDUSD 1M 85d, shock 1.0 | grows in size |
| rho|spot|up|C|ATM|long | yes | EURUSD 1Y ATM, shock 1.0 | grows in size |
| rho|spot|up|C|ATM|short | yes | AUDUSD 3M ATM, shock 1.0 | grows in size |
| rho|spot|up|C|OTM|long | yes | NZDUSD 1W 25d, shock 1.0 | grows in size |
| rho|spot|up|C|OTM|short | yes | NZDUSD 1W 15d, shock 1.0 | grows in size |
| rho|spot|up|P|ITM|long | yes | EURUSD 1M 75d, shock 1.0 | shrinks in size |
| rho|spot|up|P|ITM|short | yes | AUDUSD 1M 75d, shock 1.0 | shrinks in size |
| rho|spot|up|P|ATM|long | yes | EURUSD 1W ATM, shock 1.0 | shrinks in size |
| rho|spot|up|P|ATM|short | yes | EURUSD 1M ATM, shock 1.0 | shrinks in size |
| rho|spot|up|P|OTM|long | yes | AUDUSD 1Y 10d, shock 1.0 | shrinks in size |
| rho|spot|up|P|OTM|short | yes | AUDUSD 1Y 25d, shock 1.0 | shrinks in size |
| rho|spot|down|C|ITM|long | yes | EURUSD 3M 85d, shock 1.0 | shrinks in size |
| rho|spot|down|C|ITM|short | yes | NZDUSD 1Y 85d, shock 1.5 | shrinks in size |
| rho|spot|down|C|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | shrinks in size |
| rho|spot|down|C|ATM|short | yes | NZDUSD 6M ATM, shock 1.0 | shrinks in size |
| rho|spot|down|C|OTM|long | yes | EURUSD 3M 25d, shock 1.0 | shrinks in size |
| rho|spot|down|C|OTM|short | yes | GBPUSD 3M 25d, shock 1.0 | shrinks in size |
| rho|spot|down|P|ITM|long | yes | NZDUSD 1W 75d, shock 1.0 | grows in size |
| rho|spot|down|P|ITM|short | yes | EURUSD 1W 85d, shock 1.0 | grows in size |
| rho|spot|down|P|ATM|long | yes | AUDUSD 1M ATM, shock 1.0 | grows in size |
| rho|spot|down|P|ATM|short | yes | NZDUSD 6M ATM, shock 1.0 | grows in size |
| rho|spot|down|P|OTM|long | yes | NZDUSD 1M 10d, shock 1.0 | grows in size |
| rho|spot|down|P|OTM|short | yes | GBPUSD 6M 10d, shock 1.0 | grows in size |
| rho|time|up|C|ITM|long | yes | EURUSD 1W 85d, shock 2.0 | grows in size |
| rho|time|up|C|ITM|short | yes | NZDUSD 1M 85d, shock 2.0 | grows in size |
| rho|time|up|C|ATM|long | yes | GBPUSD 3M ATM, shock 2.0 | grows in size |
| rho|time|up|C|ATM|short | yes | EURUSD 6M ATM, shock 2.0 | grows in size |
| rho|time|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 2.0 | grows in size |
| rho|time|up|C|OTM|short | yes | NZDUSD 1W 25d, shock 2.0 | grows in size |
| rho|time|up|P|ITM|long | yes | AUDUSD 3M 85d, shock 2.0 | grows in size |
| rho|time|up|P|ITM|short | yes | EURUSD 6M 85d, shock 2.0 | grows in size |
| rho|time|up|P|ATM|long | yes | EURUSD 3M ATM, shock 2.0 | grows in size |
| rho|time|up|P|ATM|short | yes | NZDUSD 1M ATM, shock 2.0 | grows in size |
| rho|time|up|P|OTM|long | yes | AUDUSD 6M 25d, shock 2.0 | grows in size |
| rho|time|up|P|OTM|short | yes | EURUSD 6M 25d, shock 2.0 | grows in size |
| rho|time|down|C|ITM|long | yes | AUDUSD 3M 75d, shock 0.5 | shrinks in size |
| rho|time|down|C|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | shrinks in size |
| rho|time|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 0.5 | shrinks in size |
| rho|time|down|C|ATM|short | yes | AUDUSD 6M ATM, shock 0.5 | shrinks in size |
| rho|time|down|C|OTM|long | yes | AUDUSD 6M 25d, shock 0.5 | shrinks in size |
| rho|time|down|C|OTM|short | yes | AUDUSD 1Y 25d, shock 0.5 | shrinks in size |
| rho|time|down|P|ITM|long | yes | NZDUSD 1Y 75d, shock 0.5 | shrinks in size |
| rho|time|down|P|ITM|short | yes | GBPUSD 1W 85d, shock 0.5 | shrinks in size |
| rho|time|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 0.5 | shrinks in size |
| rho|time|down|P|ATM|short | yes | AUDUSD 1W ATM, shock 0.5 | shrinks in size |
| rho|time|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 0.5 | shrinks in size |
| rho|time|down|P|OTM|short | yes | AUDUSD 1M 25d, shock 0.5 | shrinks in size |
| rho|vol|up|C|ITM|long | yes | EURUSD 6M 85d, shock 2.0 | shrinks in size |
| rho|vol|up|C|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | shrinks in size |
| rho|vol|up|C|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | unchanged |
| rho|vol|up|C|ATM|short | yes | AUDUSD 6M ATM, shock 2.0 | unchanged |
| rho|vol|up|C|OTM|long | yes | GBPUSD 1W 15d, shock 2.0 | grows in size |
| rho|vol|up|C|OTM|short | yes | NZDUSD 6M 25d, shock 2.0 | grows in size |
| rho|vol|up|P|ITM|long | yes | EURUSD 1W 75d, shock 2.0 | shrinks in size |
| rho|vol|up|P|ITM|short | yes | AUDUSD 6M 85d, shock 2.0 | shrinks in size |
| rho|vol|up|P|ATM|long | yes | GBPUSD 3M ATM, shock 2.0 | unchanged |
| rho|vol|up|P|ATM|short | yes | GBPUSD 1W ATM, shock 2.0 | unchanged |
| rho|vol|up|P|OTM|long | yes | NZDUSD 1Y 25d, shock 2.0 | grows in size |
| rho|vol|up|P|OTM|short | yes | EURUSD 1W 25d, shock 2.0 | grows in size |
| rho|vol|down|C|ITM|long | yes | GBPUSD 3M 85d, shock 2.0 | grows in size |
| rho|vol|down|C|ITM|short | yes | NZDUSD 1M 85d, shock 2.0 | grows in size |
| rho|vol|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 2.0 | unchanged |
| rho|vol|down|C|ATM|short | yes | GBPUSD 1W ATM, shock 2.0 | unchanged |
| rho|vol|down|C|OTM|long | yes | GBPUSD 3M 10d, shock 2.0 | shrinks in size |
| rho|vol|down|C|OTM|short | yes | GBPUSD 3M 25d, shock 2.0 | shrinks in size |
| rho|vol|down|P|ITM|long | yes | GBPUSD 3M 85d, shock 2.0 | grows in size |
| rho|vol|down|P|ITM|short | yes | EURUSD 1Y 85d, shock 2.0 | grows in size |
| rho|vol|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 2.0 | unchanged |
| rho|vol|down|P|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | unchanged |
| rho|vol|down|P|OTM|long | yes | EURUSD 1Y 25d, shock 2.0 | shrinks in size |
| rho|vol|down|P|OTM|short | yes | NZDUSD 1M 25d, shock 2.0 | shrinks in size |

## Level 2: 360/360 cells producible (12 resolve to 'roughly unchanged')

| Cell | Producible | Conditions found | Answer |
|---|---|---|---|
| vanna|spot|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 1.0 | up |
| vanna|spot|up|C|ITM|short | yes | EURUSD 1Y 85d, shock 3.0 | down |
| vanna|spot|up|C|ATM|long | yes | GBPUSD 1M ATM, shock 1.0 | down |
| vanna|spot|up|C|ATM|short | yes | NZDUSD 1M ATM, shock 1.0 | up |
| vanna|spot|up|C|OTM|long | yes | NZDUSD 1Y 10d, shock 1.0 | up |
| vanna|spot|up|C|OTM|short | yes | GBPUSD 1Y 25d, shock 1.0 | up |
| vanna|spot|up|P|ITM|long | yes | AUDUSD 1M 85d, shock 1.5 | down |
| vanna|spot|up|P|ITM|short | yes | EURUSD 3M 75d, shock 1.0 | up |
| vanna|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | down |
| vanna|spot|up|P|ATM|short | yes | AUDUSD 1Y ATM, shock 1.0 | up |
| vanna|spot|up|P|OTM|long | yes | GBPUSD 3M 10d, shock 1.0 | up |
| vanna|spot|up|P|OTM|short | yes | GBPUSD 6M 10d, shock 1.0 | down |
| vanna|spot|down|C|ITM|long | yes | EURUSD 1Y 85d, shock 2.0 | up |
| vanna|spot|down|C|ITM|short | yes | NZDUSD 1Y 75d, shock 1.0 | down |
| vanna|spot|down|C|ATM|long | yes | NZDUSD 1M ATM, shock 1.0 | up |
| vanna|spot|down|C|ATM|short | yes | GBPUSD 6M ATM, shock 1.0 | down |
| vanna|spot|down|C|OTM|long | yes | EURUSD 1M 15d, shock 1.0 | down |
| vanna|spot|down|C|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | down |
| vanna|spot|down|P|ITM|long | yes | GBPUSD 1Y 75d, shock 1.0 | up |
| vanna|spot|down|P|ITM|short | yes | GBPUSD 1M 75d, shock 1.0 | down |
| vanna|spot|down|P|ATM|long | yes | EURUSD 3M ATM, shock 1.0 | up |
| vanna|spot|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 1.0 | down |
| vanna|spot|down|P|OTM|long | yes | NZDUSD 1Y 25d, shock 1.0 | up |
| vanna|spot|down|P|OTM|short | yes | AUDUSD 1Y 10d, shock 1.5 | up |
| vanna|time|up|C|ITM|long | yes | GBPUSD 6M 75d, shock 2.0 | up |
| vanna|time|up|C|ITM|short | yes | EURUSD 3M 85d, shock 2.0 | down |
| vanna|time|up|C|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | down |
| vanna|time|up|C|ATM|short | yes | NZDUSD 1W ATM, shock 3.0 | up |
| vanna|time|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 2.0 | down |
| vanna|time|up|C|OTM|short | yes | EURUSD 3M 25d, shock 2.0 | up |
| vanna|time|up|P|ITM|long | yes | NZDUSD 1M 85d, shock 3.0 | down |
| vanna|time|up|P|ITM|short | yes | AUDUSD 3M 85d, shock 3.0 | up |
| vanna|time|up|P|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | down |
| vanna|time|up|P|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | up |
| vanna|time|up|P|OTM|long | yes | AUDUSD 1W 10d, shock 2.0 | down |
| vanna|time|up|P|OTM|short | yes | AUDUSD 6M 15d, shock 2.0 | down |
| vanna|time|down|C|ITM|long | yes | GBPUSD 6M 85d, shock 0.75 | up |
| vanna|time|down|C|ITM|short | yes | EURUSD 1Y 75d, shock 0.5 | up |
| vanna|time|down|C|ATM|long | yes | GBPUSD 6M ATM, shock 0.75 | up |
| vanna|time|down|C|ATM|short | yes | EURUSD 1M ATM, shock 0.5 | down |
| vanna|time|down|C|OTM|long | yes | GBPUSD 6M 25d, shock 0.5 | up |
| vanna|time|down|C|OTM|short | yes | EURUSD 6M 25d, shock 0.5 | down |
| vanna|time|down|P|ITM|long | yes | NZDUSD 1M 75d, shock 0.5 | up |
| vanna|time|down|P|ITM|short | yes | GBPUSD 1M 85d, shock 0.5 | up |
| vanna|time|down|P|ATM|long | yes | AUDUSD 6M ATM, shock 0.5 | up |
| vanna|time|down|P|ATM|short | yes | AUDUSD 1M ATM, shock 0.75 | down |
| vanna|time|down|P|OTM|long | yes | GBPUSD 6M 25d, shock 0.5 | down |
| vanna|time|down|P|OTM|short | yes | GBPUSD 6M 10d, shock 0.5 | down |
| vanna|vol|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 2.0 | up |
| vanna|vol|up|C|ITM|short | yes | NZDUSD 6M 75d, shock 2.0 | down |
| vanna|vol|up|C|ATM|long | yes | GBPUSD 6M ATM, shock 3.0 | down |
| vanna|vol|up|C|ATM|short | yes | NZDUSD 6M ATM, shock 3.0 | up |
| vanna|vol|up|C|OTM|long | yes | EURUSD 3M 25d, shock 2.0 | down |
| vanna|vol|up|C|OTM|short | yes | AUDUSD 3M 10d, shock 2.0 | up |
| vanna|vol|up|P|ITM|long | yes | NZDUSD 1W 85d, shock 2.0 | down |
| vanna|vol|up|P|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | up |
| vanna|vol|up|P|ATM|long | yes | EURUSD 1Y ATM, shock 2.0 | down |
| vanna|vol|up|P|ATM|short | yes | EURUSD 6M ATM, shock 3.0 | up |
| vanna|vol|up|P|OTM|long | yes | EURUSD 3M 10d, shock 2.0 | up |
| vanna|vol|up|P|OTM|short | yes | GBPUSD 3M 15d, shock 2.0 | down |
| vanna|vol|down|C|ITM|long | yes | AUDUSD 6M 75d, shock 2.0 | down |
| vanna|vol|down|C|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | up |
| vanna|vol|down|C|ATM|long | yes | NZDUSD 1Y ATM, shock 2.0 | up |
| vanna|vol|down|C|ATM|short | yes | AUDUSD 3M ATM, shock 2.0 | down |
| vanna|vol|down|C|OTM|long | yes | GBPUSD 1Y 15d, shock 2.0 | up |
| vanna|vol|down|C|OTM|short | yes | GBPUSD 6M 25d, shock 2.0 | down |
| vanna|vol|down|P|ITM|long | yes | EURUSD 1M 75d, shock 2.0 | up |
| vanna|vol|down|P|ITM|short | yes | AUDUSD 1W 85d, shock 2.0 | down |
| vanna|vol|down|P|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | up |
| vanna|vol|down|P|ATM|short | yes | AUDUSD 1Y ATM, shock 2.0 | down |
| vanna|vol|down|P|OTM|long | yes | GBPUSD 1Y 15d, shock 2.0 | down |
| vanna|vol|down|P|OTM|short | yes | AUDUSD 6M 25d, shock 2.0 | up |
| volga|spot|up|C|ITM|long | yes | GBPUSD 1W 85d, shock 3.0 | down |
| volga|spot|up|C|ITM|short | yes | AUDUSD 3M 75d, shock 1.0 | down |
| volga|spot|up|C|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | up |
| volga|spot|up|C|ATM|short | yes | EURUSD 3M ATM, shock 1.0 | down |
| volga|spot|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 1.0 | down |
| volga|spot|up|C|OTM|short | yes | EURUSD 1Y 15d, shock 1.0 | up |
| volga|spot|up|P|ITM|long | yes | NZDUSD 6M 75d, shock 1.0 | down |
| volga|spot|up|P|ITM|short | yes | EURUSD 3M 85d, shock 1.0 | up |
| volga|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | up |
| volga|spot|up|P|ATM|short | yes | NZDUSD 6M ATM, shock 2.0 | down |
| volga|spot|up|P|OTM|long | yes | EURUSD 6M 10d, shock 1.0 | up |
| volga|spot|up|P|OTM|short | yes | GBPUSD 6M 15d, shock 1.0 | down |
| volga|spot|down|C|ITM|long | yes | AUDUSD 3M 75d, shock 1.0 | down |
| volga|spot|down|C|ITM|short | yes | AUDUSD 1Y 75d, shock 1.0 | up |
| volga|spot|down|C|ATM|long | yes | EURUSD 1M ATM, shock 1.0 | up |
| volga|spot|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 1.0 | down |
| volga|spot|down|C|OTM|long | yes | GBPUSD 1M 25d, shock 1.0 | up |
| volga|spot|down|C|OTM|short | yes | NZDUSD 1Y 15d, shock 1.0 | down |
| volga|spot|down|P|ITM|long | yes | AUDUSD 1Y 75d, shock 1.0 | up |
| volga|spot|down|P|ITM|short | yes | NZDUSD 6M 85d, shock 1.0 | down |
| volga|spot|down|P|ATM|long | yes | AUDUSD 3M ATM, shock 1.0 | up |
| volga|spot|down|P|ATM|short | yes | GBPUSD 1Y ATM, shock 1.0 | down |
| volga|spot|down|P|OTM|long | yes | AUDUSD 1M 15d, shock 1.0 | down |
| volga|spot|down|P|OTM|short | yes | GBPUSD 1Y 15d, shock 1.0 | up |
| volga|time|up|C|ITM|long | yes | EURUSD 1W 85d, shock 3.0 | down |
| volga|time|up|C|ITM|short | yes | AUDUSD 3M 85d, shock 2.0 | up |
| volga|time|up|C|ATM|long | yes | EURUSD 6M ATM, shock 3.0 | up |
| volga|time|up|C|ATM|short | yes | EURUSD 3M ATM, shock 3.0 | down |
| volga|time|up|C|OTM|long | yes | NZDUSD 6M 15d, shock 2.0 | down |
| volga|time|up|C|OTM|short | yes | EURUSD 1W 10d, shock 2.0 | down |
| volga|time|up|P|ITM|long | yes | NZDUSD 6M 75d, shock 2.0 | down |
| volga|time|up|P|ITM|short | yes | NZDUSD 1M 85d, shock 2.0 | up |
| volga|time|up|P|ATM|long | yes | EURUSD 3M ATM, shock 3.0 | up |
| volga|time|up|P|ATM|short | yes | EURUSD 3M ATM, shock 3.0 | down |
| volga|time|up|P|OTM|long | yes | NZDUSD 6M 10d, shock 2.0 | up |
| volga|time|up|P|OTM|short | yes | GBPUSD 3M 10d, shock 2.0 | down |
| volga|time|down|C|ITM|long | yes | GBPUSD 1M 85d, shock 0.5 | down |
| volga|time|down|C|ITM|short | yes | AUDUSD 1Y 85d, shock 0.75 | up |
| volga|time|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 0.5 | up |
| volga|time|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 0.75 | down |
| volga|time|down|C|OTM|long | yes | AUDUSD 1M 10d, shock 0.5 | down |
| volga|time|down|C|OTM|short | yes | GBPUSD 1W 10d, shock 0.5 | up |
| volga|time|down|P|ITM|long | yes | GBPUSD 6M 85d, shock 0.5 | down |
| volga|time|down|P|ITM|short | yes | EURUSD 1M 75d, shock 0.5 | down |
| volga|time|down|P|ATM|long | yes | NZDUSD 3M ATM, shock 0.75 | up |
| volga|time|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 0.5 | down |
| volga|time|down|P|OTM|long | yes | EURUSD 1Y 15d, shock 0.5 | down |
| volga|time|down|P|OTM|short | yes | AUDUSD 6M 15d, shock 0.5 | up |
| volga|vol|up|C|ITM|long | yes | NZDUSD 1W 75d, shock 2.0 | down |
| volga|vol|up|C|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | up |
| volga|vol|up|C|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | unchanged |
| volga|vol|up|C|ATM|short | yes | NZDUSD 3M ATM, shock 2.0 | unchanged |
| volga|vol|up|C|OTM|long | yes | AUDUSD 1Y 15d, shock 2.0 | down |
| volga|vol|up|C|OTM|short | yes | NZDUSD 1M 15d, shock 2.0 | up |
| volga|vol|up|P|ITM|long | yes | AUDUSD 6M 85d, shock 2.0 | down |
| volga|vol|up|P|ITM|short | yes | NZDUSD 6M 75d, shock 2.0 | up |
| volga|vol|up|P|ATM|long | yes | GBPUSD 1Y ATM, shock 2.0 | unchanged |
| volga|vol|up|P|ATM|short | yes | NZDUSD 6M ATM, shock 2.0 | unchanged |
| volga|vol|up|P|OTM|long | yes | EURUSD 1Y 25d, shock 2.0 | down |
| volga|vol|up|P|OTM|short | yes | GBPUSD 3M 15d, shock 2.0 | up |
| volga|vol|down|C|ITM|long | yes | NZDUSD 1W 75d, shock 2.0 | up |
| volga|vol|down|C|ITM|short | yes | GBPUSD 3M 85d, shock 2.0 | down |
| volga|vol|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 4.0 | up |
| volga|vol|down|C|ATM|short | yes | EURUSD 1Y ATM, shock 4.0 | down |
| volga|vol|down|C|OTM|long | yes | AUDUSD 1W 15d, shock 2.0 | up |
| volga|vol|down|C|OTM|short | yes | GBPUSD 1M 10d, shock 2.0 | down |
| volga|vol|down|P|ITM|long | yes | EURUSD 1M 85d, shock 2.0 | up |
| volga|vol|down|P|ITM|short | yes | GBPUSD 1W 85d, shock 2.0 | down |
| volga|vol|down|P|ATM|long | yes | AUDUSD 1Y ATM, shock 4.0 | up |
| volga|vol|down|P|ATM|short | yes | EURUSD 1Y ATM, shock 4.0 | down |
| volga|vol|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 2.0 | up |
| volga|vol|down|P|OTM|short | yes | EURUSD 6M 15d, shock 2.0 | down |
| charm|spot|up|C|ITM|long | yes | GBPUSD 1M 75d, shock 1.0 | up |
| charm|spot|up|C|ITM|short | yes | NZDUSD 1Y 75d, shock 1.0 | down |
| charm|spot|up|C|ATM|long | yes | AUDUSD 1M ATM, shock 1.0 | up |
| charm|spot|up|C|ATM|short | yes | AUDUSD 1M ATM, shock 1.0 | down |
| charm|spot|up|C|OTM|long | yes | AUDUSD 1W 10d, shock 3.0 | up |
| charm|spot|up|C|OTM|short | yes | GBPUSD 6M 10d, shock 1.0 | up |
| charm|spot|up|P|ITM|long | yes | EURUSD 1W 85d, shock 1.0 | up |
| charm|spot|up|P|ITM|short | yes | EURUSD 1Y 75d, shock 1.0 | down |
| charm|spot|up|P|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | up |
| charm|spot|up|P|ATM|short | yes | GBPUSD 1W ATM, shock 1.0 | down |
| charm|spot|up|P|OTM|long | yes | GBPUSD 1M 25d, shock 1.0 | up |
| charm|spot|up|P|OTM|short | yes | NZDUSD 6M 10d, shock 1.0 | up |
| charm|spot|down|C|ITM|long | yes | AUDUSD 6M 85d, shock 1.5 | down |
| charm|spot|down|C|ITM|short | yes | EURUSD 1W 85d, shock 1.0 | up |
| charm|spot|down|C|ATM|long | yes | AUDUSD 1M ATM, shock 1.0 | down |
| charm|spot|down|C|ATM|short | yes | GBPUSD 1M ATM, shock 1.0 | up |
| charm|spot|down|C|OTM|long | yes | AUDUSD 1M 25d, shock 1.0 | down |
| charm|spot|down|C|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | up |
| charm|spot|down|P|ITM|long | yes | AUDUSD 1W 85d, shock 1.0 | up |
| charm|spot|down|P|ITM|short | yes | GBPUSD 3M 75d, shock 1.0 | up |
| charm|spot|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 1.0 | down |
| charm|spot|down|P|ATM|short | yes | EURUSD 1M ATM, shock 1.0 | up |
| charm|spot|down|P|OTM|long | yes | NZDUSD 1M 25d, shock 1.0 | down |
| charm|spot|down|P|OTM|short | yes | EURUSD 6M 15d, shock 1.0 | up |
| charm|time|up|C|ITM|long | yes | NZDUSD 1W 85d, shock 2.0 | down |
| charm|time|up|C|ITM|short | yes | NZDUSD 1W 85d, shock 2.0 | up |
| charm|time|up|C|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | up |
| charm|time|up|C|ATM|short | yes | NZDUSD 3M ATM, shock 2.0 | down |
| charm|time|up|C|OTM|long | yes | NZDUSD 1W 15d, shock 2.0 | up |
| charm|time|up|C|OTM|short | yes | AUDUSD 1M 25d, shock 2.0 | down |
| charm|time|up|P|ITM|long | yes | GBPUSD 1M 75d, shock 2.0 | up |
| charm|time|up|P|ITM|short | yes | AUDUSD 1M 85d, shock 2.0 | down |
| charm|time|up|P|ATM|long | yes | GBPUSD 6M ATM, shock 2.0 | up |
| charm|time|up|P|ATM|short | yes | AUDUSD 1M ATM, shock 2.0 | down |
| charm|time|up|P|OTM|long | yes | NZDUSD 1M 15d, shock 2.0 | down |
| charm|time|up|P|OTM|short | yes | EURUSD 1W 25d, shock 2.0 | up |
| charm|time|down|C|ITM|long | yes | NZDUSD 1W 75d, shock 0.5 | up |
| charm|time|down|C|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | down |
| charm|time|down|C|ATM|long | yes | NZDUSD 6M ATM, shock 0.5 | down |
| charm|time|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 0.5 | up |
| charm|time|down|C|OTM|long | yes | GBPUSD 1W 10d, shock 0.5 | down |
| charm|time|down|C|OTM|short | yes | NZDUSD 3M 15d, shock 0.5 | up |
| charm|time|down|P|ITM|long | yes | GBPUSD 6M 75d, shock 0.5 | down |
| charm|time|down|P|ITM|short | yes | NZDUSD 6M 85d, shock 0.5 | up |
| charm|time|down|P|ATM|long | yes | GBPUSD 1M ATM, shock 0.5 | down |
| charm|time|down|P|ATM|short | yes | EURUSD 3M ATM, shock 0.5 | up |
| charm|time|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 0.5 | up |
| charm|time|down|P|OTM|short | yes | AUDUSD 3M 25d, shock 0.5 | down |
| charm|vol|up|C|ITM|long | yes | GBPUSD 3M 75d, shock 2.0 | down |
| charm|vol|up|C|ITM|short | yes | EURUSD 1Y 85d, shock 2.0 | up |
| charm|vol|up|C|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | up |
| charm|vol|up|C|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | down |
| charm|vol|up|C|OTM|long | yes | GBPUSD 1W 15d, shock 4.0 | up |
| charm|vol|up|C|OTM|short | yes | EURUSD 1W 15d, shock 4.0 | down |
| charm|vol|up|P|ITM|long | yes | AUDUSD 3M 75d, shock 2.0 | up |
| charm|vol|up|P|ITM|short | yes | NZDUSD 1W 75d, shock 2.0 | down |
| charm|vol|up|P|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | up |
| charm|vol|up|P|ATM|short | yes | NZDUSD 1M ATM, shock 3.0 | down |
| charm|vol|up|P|OTM|long | yes | NZDUSD 3M 15d, shock 3.0 | down |
| charm|vol|up|P|OTM|short | yes | EURUSD 6M 25d, shock 2.0 | up |
| charm|vol|down|C|ITM|long | yes | EURUSD 1M 75d, shock 2.0 | up |
| charm|vol|down|C|ITM|short | yes | GBPUSD 6M 85d, shock 4.0 | up |
| charm|vol|down|C|ATM|long | yes | EURUSD 1W ATM, shock 2.0 | down |
| charm|vol|down|C|ATM|short | yes | AUDUSD 1Y ATM, shock 2.0 | up |
| charm|vol|down|C|OTM|long | yes | AUDUSD 1W 10d, shock 2.0 | up |
| charm|vol|down|C|OTM|short | yes | GBPUSD 1W 25d, shock 2.0 | up |
| charm|vol|down|P|ITM|long | yes | EURUSD 6M 75d, shock 2.0 | down |
| charm|vol|down|P|ITM|short | yes | NZDUSD 1M 75d, shock 2.0 | up |
| charm|vol|down|P|ATM|long | yes | EURUSD 6M ATM, shock 2.0 | down |
| charm|vol|down|P|ATM|short | yes | EURUSD 3M ATM, shock 2.0 | up |
| charm|vol|down|P|OTM|long | yes | NZDUSD 1M 10d, shock 2.0 | down |
| charm|vol|down|P|OTM|short | yes | NZDUSD 3M 15d, shock 4.0 | up |
| speed|spot|up|C|ITM|long | yes | EURUSD 1Y 75d, shock 1.0 | down |
| speed|spot|up|C|ITM|short | yes | AUDUSD 1M 75d, shock 1.0 | up |
| speed|spot|up|C|ATM|long | yes | EURUSD 1M ATM, shock 1.0 | down |
| speed|spot|up|C|ATM|short | yes | AUDUSD 6M ATM, shock 1.0 | up |
| speed|spot|up|C|OTM|long | yes | NZDUSD 3M 15d, shock 2.0 | down |
| speed|spot|up|C|OTM|short | yes | EURUSD 3M 10d, shock 1.0 | down |
| speed|spot|up|P|ITM|long | yes | EURUSD 1M 75d, shock 1.0 | down |
| speed|spot|up|P|ITM|short | yes | EURUSD 6M 75d, shock 1.0 | up |
| speed|spot|up|P|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | down |
| speed|spot|up|P|ATM|short | yes | EURUSD 3M ATM, shock 1.0 | up |
| speed|spot|up|P|OTM|long | yes | EURUSD 1M 10d, shock 1.0 | up |
| speed|spot|up|P|OTM|short | yes | NZDUSD 1Y 25d, shock 1.0 | up |
| speed|spot|down|C|ITM|long | yes | AUDUSD 1M 75d, shock 1.0 | up |
| speed|spot|down|C|ITM|short | yes | GBPUSD 3M 85d, shock 2.0 | down |
| speed|spot|down|C|ATM|long | yes | AUDUSD 1Y ATM, shock 1.0 | up |
| speed|spot|down|C|ATM|short | yes | GBPUSD 1W ATM, shock 1.0 | down |
| speed|spot|down|C|OTM|long | yes | EURUSD 1M 25d, shock 1.0 | up |
| speed|spot|down|C|OTM|short | yes | NZDUSD 3M 10d, shock 1.0 | up |
| speed|spot|down|P|ITM|long | yes | GBPUSD 3M 85d, shock 1.0 | down |
| speed|spot|down|P|ITM|short | yes | NZDUSD 1W 75d, shock 3.0 | up |
| speed|spot|down|P|ATM|long | yes | AUDUSD 1W ATM, shock 1.0 | up |
| speed|spot|down|P|ATM|short | yes | GBPUSD 1Y ATM, shock 1.0 | down |
| speed|spot|down|P|OTM|long | yes | GBPUSD 3M 15d, shock 2.0 | up |
| speed|spot|down|P|OTM|short | yes | NZDUSD 1W 15d, shock 1.0 | down |
| speed|time|up|C|ITM|long | yes | GBPUSD 1M 75d, shock 2.0 | up |
| speed|time|up|C|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | down |
| speed|time|up|C|ATM|long | yes | AUDUSD 3M ATM, shock 2.0 | down |
| speed|time|up|C|ATM|short | yes | NZDUSD 6M ATM, shock 2.0 | up |
| speed|time|up|C|OTM|long | yes | GBPUSD 1W 25d, shock 2.0 | down |
| speed|time|up|C|OTM|short | yes | AUDUSD 1M 15d, shock 2.0 | up |
| speed|time|up|P|ITM|long | yes | GBPUSD 6M 85d, shock 2.0 | down |
| speed|time|up|P|ITM|short | yes | GBPUSD 1M 75d, shock 2.0 | up |
| speed|time|up|P|ATM|long | yes | AUDUSD 3M ATM, shock 2.0 | down |
| speed|time|up|P|ATM|short | yes | AUDUSD 3M ATM, shock 2.0 | up |
| speed|time|up|P|OTM|long | yes | EURUSD 1W 15d, shock 2.0 | up |
| speed|time|up|P|OTM|short | yes | AUDUSD 6M 10d, shock 2.0 | down |
| speed|time|down|C|ITM|long | yes | NZDUSD 1M 85d, shock 0.5 | down |
| speed|time|down|C|ITM|short | yes | GBPUSD 6M 75d, shock 0.5 | up |
| speed|time|down|C|ATM|long | yes | EURUSD 1M ATM, shock 0.5 | up |
| speed|time|down|C|ATM|short | yes | EURUSD 1W ATM, shock 0.5 | down |
| speed|time|down|C|OTM|long | yes | NZDUSD 6M 25d, shock 0.5 | up |
| speed|time|down|C|OTM|short | yes | AUDUSD 1Y 15d, shock 0.5 | down |
| speed|time|down|P|ITM|long | yes | AUDUSD 3M 85d, shock 0.5 | up |
| speed|time|down|P|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | down |
| speed|time|down|P|ATM|long | yes | NZDUSD 1M ATM, shock 0.5 | up |
| speed|time|down|P|ATM|short | yes | GBPUSD 1M ATM, shock 0.5 | down |
| speed|time|down|P|OTM|long | yes | EURUSD 1Y 25d, shock 0.5 | down |
| speed|time|down|P|OTM|short | yes | GBPUSD 1Y 10d, shock 0.5 | up |
| speed|vol|up|C|ITM|long | yes | GBPUSD 3M 75d, shock 2.0 | up |
| speed|vol|up|C|ITM|short | yes | AUDUSD 1Y 85d, shock 2.0 | down |
| speed|vol|up|C|ATM|long | yes | AUDUSD 1Y ATM, shock 2.0 | down |
| speed|vol|up|C|ATM|short | yes | EURUSD 1Y ATM, shock 2.0 | up |
| speed|vol|up|C|OTM|long | yes | EURUSD 1M 25d, shock 2.0 | down |
| speed|vol|up|C|OTM|short | yes | EURUSD 1Y 15d, shock 2.0 | up |
| speed|vol|up|P|ITM|long | yes | NZDUSD 3M 85d, shock 2.0 | down |
| speed|vol|up|P|ITM|short | yes | NZDUSD 3M 75d, shock 2.0 | up |
| speed|vol|up|P|ATM|long | yes | EURUSD 6M ATM, shock 4.0 | down |
| speed|vol|up|P|ATM|short | yes | EURUSD 1Y ATM, shock 2.0 | up |
| speed|vol|up|P|OTM|long | yes | NZDUSD 1Y 10d, shock 2.0 | up |
| speed|vol|up|P|OTM|short | yes | AUDUSD 1M 15d, shock 2.0 | down |
| speed|vol|down|C|ITM|long | yes | NZDUSD 1M 85d, shock 2.0 | down |
| speed|vol|down|C|ITM|short | yes | NZDUSD 1Y 75d, shock 2.0 | up |
| speed|vol|down|C|ATM|long | yes | GBPUSD 6M ATM, shock 2.0 | up |
| speed|vol|down|C|ATM|short | yes | EURUSD 1W ATM, shock 3.0 | down |
| speed|vol|down|C|OTM|long | yes | NZDUSD 1M 25d, shock 2.0 | up |
| speed|vol|down|C|OTM|short | yes | GBPUSD 3M 15d, shock 2.0 | down |
| speed|vol|down|P|ITM|long | yes | GBPUSD 6M 85d, shock 2.0 | up |
| speed|vol|down|P|ITM|short | yes | GBPUSD 1W 75d, shock 2.0 | down |
| speed|vol|down|P|ATM|long | yes | NZDUSD 1Y ATM, shock 2.0 | up |
| speed|vol|down|P|ATM|short | yes | GBPUSD 1Y ATM, shock 2.0 | down |
| speed|vol|down|P|OTM|long | yes | NZDUSD 1M 10d, shock 2.0 | down |
| speed|vol|down|P|OTM|short | yes | GBPUSD 1M 25d, shock 2.0 | up |
| veta|spot|up|C|ITM|long | yes | GBPUSD 1M 85d, shock 1.0 | up |
| veta|spot|up|C|ITM|short | yes | AUDUSD 1M 85d, shock 1.0 | down |
| veta|spot|up|C|ATM|long | yes | EURUSD 1Y ATM, shock 1.0 | up |
| veta|spot|up|C|ATM|short | yes | AUDUSD 3M ATM, shock 3.0 | up |
| veta|spot|up|C|OTM|long | yes | NZDUSD 1W 25d, shock 1.0 | up |
| veta|spot|up|C|OTM|short | yes | NZDUSD 1W 15d, shock 1.5 | down |
| veta|spot|up|P|ITM|long | yes | EURUSD 1M 75d, shock 1.0 | up |
| veta|spot|up|P|ITM|short | yes | AUDUSD 1M 75d, shock 1.0 | down |
| veta|spot|up|P|ATM|long | yes | EURUSD 1W ATM, shock 1.0 | down |
| veta|spot|up|P|ATM|short | yes | EURUSD 1M ATM, shock 2.0 | up |
| veta|spot|up|P|OTM|long | yes | AUDUSD 1Y 10d, shock 2.0 | up |
| veta|spot|up|P|OTM|short | yes | AUDUSD 1Y 25d, shock 1.0 | up |
| veta|spot|down|C|ITM|long | yes | EURUSD 3M 85d, shock 1.5 | up |
| veta|spot|down|C|ITM|short | yes | NZDUSD 1Y 85d, shock 3.0 | down |
| veta|spot|down|C|ATM|long | yes | NZDUSD 1W ATM, shock 1.0 | down |
| veta|spot|down|C|ATM|short | yes | NZDUSD 6M ATM, shock 1.5 | up |
| veta|spot|down|C|OTM|long | yes | EURUSD 3M 25d, shock 1.0 | down |
| veta|spot|down|C|OTM|short | yes | GBPUSD 3M 25d, shock 1.0 | up |
| veta|spot|down|P|ITM|long | yes | NZDUSD 1W 75d, shock 3.0 | up |
| veta|spot|down|P|ITM|short | yes | EURUSD 1W 85d, shock 1.0 | down |
| veta|spot|down|P|ATM|long | yes | AUDUSD 1M ATM, shock 1.0 | down |
| veta|spot|down|P|ATM|short | yes | NZDUSD 6M ATM, shock 1.5 | up |
| veta|spot|down|P|OTM|long | yes | NZDUSD 1M 10d, shock 1.0 | down |
| veta|spot|down|P|OTM|short | yes | EURUSD 1M 25d, shock 1.0 | down |
| veta|time|up|C|ITM|long | yes | EURUSD 1W 85d, shock 2.0 | up |
| veta|time|up|C|ITM|short | yes | NZDUSD 1M 85d, shock 2.0 | down |
| veta|time|up|C|ATM|long | yes | GBPUSD 3M ATM, shock 2.0 | up |
| veta|time|up|C|ATM|short | yes | EURUSD 6M ATM, shock 2.0 | down |
| veta|time|up|C|OTM|long | yes | NZDUSD 3M 25d, shock 2.0 | up |
| veta|time|up|C|OTM|short | yes | NZDUSD 1W 25d, shock 2.0 | down |
| veta|time|up|P|ITM|long | yes | AUDUSD 3M 85d, shock 2.0 | up |
| veta|time|up|P|ITM|short | yes | EURUSD 6M 85d, shock 2.0 | down |
| veta|time|up|P|ATM|long | yes | EURUSD 3M ATM, shock 2.0 | up |
| veta|time|up|P|ATM|short | yes | NZDUSD 1M ATM, shock 2.0 | down |
| veta|time|up|P|OTM|long | yes | AUDUSD 6M 25d, shock 2.0 | up |
| veta|time|up|P|OTM|short | yes | EURUSD 6M 25d, shock 2.0 | down |
| veta|time|down|C|ITM|long | yes | AUDUSD 3M 75d, shock 0.5 | down |
| veta|time|down|C|ITM|short | yes | GBPUSD 3M 75d, shock 0.5 | up |
| veta|time|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 0.5 | down |
| veta|time|down|C|ATM|short | yes | AUDUSD 6M ATM, shock 0.5 | up |
| veta|time|down|C|OTM|long | yes | AUDUSD 6M 25d, shock 0.5 | down |
| veta|time|down|C|OTM|short | yes | AUDUSD 1Y 25d, shock 0.5 | up |
| veta|time|down|P|ITM|long | yes | NZDUSD 1Y 75d, shock 0.5 | down |
| veta|time|down|P|ITM|short | yes | GBPUSD 1W 85d, shock 0.5 | up |
| veta|time|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 0.5 | down |
| veta|time|down|P|ATM|short | yes | AUDUSD 1W ATM, shock 0.5 | up |
| veta|time|down|P|OTM|long | yes | GBPUSD 1Y 25d, shock 0.5 | down |
| veta|time|down|P|OTM|short | yes | AUDUSD 1M 25d, shock 0.5 | up |
| veta|vol|up|C|ITM|long | yes | GBPUSD 1M 75d, shock 2.0 | up |
| veta|vol|up|C|ITM|short | yes | NZDUSD 3M 75d, shock 4.0 | down |
| veta|vol|up|C|ATM|long | yes | NZDUSD 6M ATM, shock 2.0 | unchanged |
| veta|vol|up|C|ATM|short | yes | AUDUSD 6M ATM, shock 2.0 | unchanged |
| veta|vol|up|C|OTM|long | yes | AUDUSD 1W 10d, shock 2.0 | down |
| veta|vol|up|C|OTM|short | yes | NZDUSD 6M 25d, shock 2.0 | down |
| veta|vol|up|P|ITM|long | yes | EURUSD 1W 75d, shock 2.0 | up |
| veta|vol|up|P|ITM|short | yes | GBPUSD 3M 75d, shock 2.0 | down |
| veta|vol|up|P|ATM|long | yes | GBPUSD 3M ATM, shock 2.0 | unchanged |
| veta|vol|up|P|ATM|short | yes | GBPUSD 1W ATM, shock 2.0 | unchanged |
| veta|vol|up|P|OTM|long | yes | GBPUSD 1Y 25d, shock 2.0 | up |
| veta|vol|up|P|OTM|short | yes | EURUSD 1W 25d, shock 2.0 | down |
| veta|vol|down|C|ITM|long | yes | GBPUSD 3M 85d, shock 3.0 | up |
| veta|vol|down|C|ITM|short | yes | NZDUSD 1M 85d, shock 3.0 | down |
| veta|vol|down|C|ATM|long | yes | EURUSD 1Y ATM, shock 2.0 | unchanged |
| veta|vol|down|C|ATM|short | yes | GBPUSD 1W ATM, shock 2.0 | unchanged |
| veta|vol|down|C|OTM|long | yes | GBPUSD 3M 10d, shock 2.0 | up |
| veta|vol|down|C|OTM|short | yes | GBPUSD 3M 25d, shock 2.0 | up |
| veta|vol|down|P|ITM|long | yes | GBPUSD 3M 85d, shock 2.0 | up |
| veta|vol|down|P|ITM|short | yes | EURUSD 1Y 85d, shock 3.0 | down |
| veta|vol|down|P|ATM|long | yes | EURUSD 1Y ATM, shock 2.0 | unchanged |
| veta|vol|down|P|ATM|short | yes | EURUSD 1W ATM, shock 2.0 | unchanged |
| veta|vol|down|P|OTM|long | yes | EURUSD 1Y 25d, shock 3.0 | up |
| veta|vol|down|P|OTM|short | yes | NZDUSD 1M 25d, shock 3.0 | up |
