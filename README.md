Got you! Here’s a clean, complete README for your Djeja Simulator app. I’ve written it so it’s clear, explanatory, and includes all features including dynamic trades and projections.

⸻

Djeja Simulator 🐔💰

Djeja Simulator is a dynamic daily trading compounding calculator that simulates profits based on your base trades, bonus trades, and variable profit per trade. It also considers Tunis time thresholds for when trades are counted today.

⸻

Features
	1.	Daily Compounding Projection
	•	Simulates your account balance based on:
	•	Base trades per day
	•	Extra trades (referrals, bonuses) for N days
	•	Fixed risk per trade (1%)
	•	Profit per trade (% of risk)
	2.	Dynamic Trades for Today
	•	Trades for the current day are counted dynamically based on current Tunis time.
	•	Thresholds:
	•	Base trade 1 → counted if current time ≥ 13:39
	•	Base trade 2 → counted if current time ≥ 18:39
	•	Bonus trade 1 → counted if current time ≥ 18:49
	•	Bonus trade 2 → counted if current time ≥ 18:59
	3.	Dynamic Extra Trades
	•	Add extra trades (bonus/referral) for a specific number of days.
	•	The app automatically calculates them for the first N days.
	4.	Calculation Modes
	•	Starting Balance → Projection: Input your starting balance and see projected balance and profits.
	•	Target Profit → Starting Balance: Input a desired total profit, and the app calculates the starting balance needed.
	5.	Interactive Projection Table
	•	Shows Date, Day, Number of Trades, Daily Profit, and Balance.
	•	Updates dynamically as inputs change.
	6.	Analytics & Graphs
	•	Balance Over Time (line chart)
	•	Daily Profit (bar chart)
	•	Trades per Day (line chart)
	•	Extra stats: average daily profit, maximum daily profit, total trades projected, average trades per day.

⸻

How It Works
	1.	Trade Calculation
	•	Each trade applies profit = risk × profit %.
	•	Base trades happen every day. Bonus trades only happen for the first N days and respect time thresholds.
	2.	Dynamic Time Logic
	•	Today’s trades are only counted if the current Tunis time has passed their thresholds.
	•	Future days assume all base + bonus trades occur.
	3.	Compounding
	•	Trades compound trade by trade, so each trade increases the balance for the next trade calculation.

⸻

Inputs

Input	Description
Starting Balance	Amount in $ to start the projection
Profit per Trade (% of Risk)	Average profit per trade in % of the 1% risk
Base Trades per Day	Number of base trades every day
Number of Days	Projection length
Extra Trades per Day	Bonus/referral trades per day
Extra Trades Duration	Number of days for bonus trades
Calculation Mode	Either “Starting Balance → Projection” or “Target Profit → Starting Balance”


⸻

Outputs
	•	Projection Table
Shows daily balance, daily profit, and number of trades.
	•	Analytics
	•	Line chart: Balance over time
	•	Bar chart: Daily profits
	•	Line chart: Trades per day
	•	Extra stats: averages and totals
	•	Dynamic Today Info
Shows how many trades have already counted today based on current Tunis time.

⸻

Example

Current Tunis time: 01:18 → Trades counted today dynamically: 0
Date         Day  Trades  Daily Profit  Balance
2026-01-07    1      2      33.58      2733.58
2026-01-08    2      2      34.00      2767.59
2026-01-09    3      2      34.42      2802.01

	•	Trades today will update dynamically as time passes.

⸻

Requirements
	•	Python 3.11+
	•	Streamlit
	•	pandas
	•	pytz
	•	plotly (optional for interactive charts)

Install packages:

pip install -r requirements.txt


⸻

Notes
	•	Risk per trade is fixed at 1%.
	•	Profit per trade is user-defined (default 62% of risk).
	•	Extra trades are applied only for the specified number of days.
	•	Today’s trades depend on current Tunis time.

⸻
