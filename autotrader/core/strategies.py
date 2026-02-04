from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class StrategyType(Enum):
    """Enum for strategy types providing type safety and faster comparisons."""
<<<<<<< devin/1770200586-strategy-type-enum
=======

>>>>>>> main
    MEAN_REVERSION = "mean_reversion"
    TREND_FOLLOWING = "trend_following"
    BREAKOUT = "breakout"
    SCALPING = "scalping"
    ARBITRAGE = "arbitrage"


@dataclass
class StrategyParams:
    name: str
    description: str
    type: StrategyType
    config: Dict[str, Any]


class BaseStrategy(ABC):
    def __init__(self, params: StrategyParams):
        self.params = params

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any]) -> str:
        """Retorna 'BUY', 'SELL' ou 'HOLD'."""
        ...
