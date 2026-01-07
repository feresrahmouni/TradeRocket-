# ===== App Info =====
APP_NAME = "Djeja Simulator 💰🐔"
APP_DESCRIPTION = "Daily trading compounding calculator with referral extra trades."

# ===== Default Trading Parameters =====
DEFAULT_STARTING_BALANCE = 1000
DEFAULT_PROFIT_PERCENT = 62.0
DEFAULT_BASE_TRADES = 2
DEFAULT_DAYS = 52

# ===== Default Bonus Trades =====
DEFAULT_EXTRA_TRADES = 2
DEFAULT_EXTRA_DAYS = 4

# ===== Time Thresholds (Tunis time) =====
# Base trades: count only after these times
BASE_TRADE_THRESHOLDS = [
    (13, 39),  # first base trade
    (18, 39),  # second base trade
]

# Bonus trades: count only after these times
BONUS_TRADE_THRESHOLDS = [
    (18, 49),  # first bonus
    (18, 59),  # second bonus
]

# ===== Emojis / Icons =====
EMOJI_CHICKEN = "🐔"
EMOJI_CASH = "💰"
EMOJI_APP = "🚀"

# ===== Misc =====
CURRENCY_SYMBOL = "$"
