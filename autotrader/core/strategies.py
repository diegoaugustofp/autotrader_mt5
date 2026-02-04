from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class StrategyParams:
    name: str
    description: str
    type: str  # "mean_reversion", "trend_following", etc.
    config: Dict[str, Any]

class BaseStrategy(ABC):
    def __init__(self, params: StrategyParams):
        self.params = params

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any]) -> str:
        """Retorna 'BUY', 'SELL' ou 'HOLD'."""
        ...
