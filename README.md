# TradeCompound 🚀

TradeCompound is a daily trading compounding calculator. It calculates your account balance over 90 days based on your trades, compounding, and optional bonus trades.

---

## How the Calculation Works

1. **Daily Trades**: Each day, your account balance is updated based on the number of trades you do.
2. **Per Trade Profit**: Each trade uses a fixed **1% of your current balance** as risk, and the profit for that trade is **62% of the risk amount**.  
   - Example: If your balance is $2700, 1% risk = $27. Profit = 62% of $27 ≈ $16.74. This profit is added immediately to your balance before the next trade.
3. **Compounding**: Each trade compounds immediately. So the second trade of the day is calculated using the **updated balance** after the first trade, and so on.
4. **Extra Trades**: You can add “bonus trades” for a certain number of days starting from day 1.  
   - Example: If you choose **2 extra trades for 3 days**, then for day 1, 2, and 3, the total trades per day will be **base trades + 2 extra trades**. After that, only the base trades are used.
5. **Daily Profit**: The daily profit is the **total profit made from all trades that day**.

---

## Average Values

- **Risk per trade**: 1% of current balance (fixed)  
- **Profit per trade**: 62% of risk (fixed)  
- **Extra trades**: User-defined number of trades added for bonus days starting from day 1  
