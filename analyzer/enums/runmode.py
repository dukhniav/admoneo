from enum import Enum


class RunMode(Enum):
    """
    Bot running mode (backtest ...)
    can be "live", "backtest"
    """
    LIVE = "live"
    BACKTEST = "backtest"
    OTHER = "other"
