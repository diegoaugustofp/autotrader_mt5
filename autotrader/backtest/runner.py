from enum import Enum
from functools import lru_cache
from typing import List, Dict, Any, Tuple
from datetime import datetime
from ..core.strategies import BaseStrategy
from ..core.risk import RiskManager


class Timeframe(Enum):
    """Enum for timeframes providing type safety and preventing invalid values."""

    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"


class MarketDataCache:
    """LRU cache for historical market data to avoid repeated MT5 fetches."""

    def __init__(self, maxsize: int = 128):
        self._maxsize = maxsize
        self._get_data = lru_cache(maxsize=maxsize)(self._fetch_data)

    def _fetch_data(
        self, symbol: str, from_timestamp: float, to_timestamp: float, timeframe: str
    ) -> Tuple[Dict[str, Any], ...]:
        """Fetch data from MT5. Returns tuple for hashability."""
        # Implementation would fetch from MT5 here
        # Return as tuple for LRU cache compatibility
        ...

    def get(
        self, symbol: str, from_date: datetime, to_date: datetime, timeframe: Timeframe
    ) -> List[Dict[str, Any]]:
        """Get cached data or fetch from MT5 if not cached."""
        result = self._get_data(
            symbol, from_date.timestamp(), to_date.timestamp(), timeframe.value
        )
        return list(result) if result else []

    def clear(self) -> None:
        """Clear the cache."""
        self._get_data.cache_clear()

    def cache_info(self):
        """Return cache statistics."""
        return self._get_data.cache_info()


class BacktestRunner:
    _data_cache = MarketDataCache()

    def __init__(self, strategy: BaseStrategy, risk_manager: RiskManager):
        self.strategy = strategy
        self.risk_manager = risk_manager

    def run(
        self, symbol: str, from_date: datetime, to_date: datetime, timeframe: Timeframe
    ) -> Dict[str, Any]:
        # Load historical data via cache (fetches from MT5 only if not cached)
        _data = self._data_cache.get(symbol, from_date, to_date, timeframe)
        # executar lógica de sinais e risco
        # retornar métricas
        ...
