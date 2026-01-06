from datetime import datetime, time
import pytz

# ===== Timezone =====
tz = pytz.timezone("Africa/Tunis")

# ===== Trade Time Thresholds (Tunis time) =====
BASE_TRADE_THRESHOLDS = [
    time(13, 39),  # first base trade
    time(18, 39),  # second base trade
]

BONUS_TRADE_THRESHOLDS = [
    time(18, 49),  # first bonus
    time(18, 59),  # second bonus
]

def count_trades_now(
    base_trades_per_day: int,
    extra_trades_per_day: int,
    extra_trades_days: int,
    day_number: int
) -> int:
    """
    Count how many trades should be counted TODAY based on Tunis time.

    Rules:
    - Base trades: only count if current time is after threshold
    - Bonus trades: only count if day <= extra_trades_days and after threshold

    Parameters:
        base_trades_per_day: number of regular trades per day
        extra_trades_per_day: number of bonus trades
        extra_trades_days: number of days bonus trades are active
        day_number: which day of projection (1-based)

    Returns:
        int: total trades to count for today
    """

    now = datetime.now(tz).time()
    trades = 0

    # Base trades
    for t in BASE_TRADE_THRESHOLDS[:base_trades_per_day]:
        if now >= t:
            trades += 1

    # Bonus trades (only for first N days)
    if day_number <= extra_trades_days:
        for t in BONUS_TRADE_THRESHOLDS[:extra_trades_per_day]:
            if now >= t:
                trades += 1

    return trades
