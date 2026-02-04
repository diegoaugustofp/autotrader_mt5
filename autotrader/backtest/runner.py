from typing import List, Dict, Any
from datetime import datetime
from ..core.strategies import BaseStrategy
from ..core.risk import RiskManager

class BacktestRunner:
    def __init__(self, strategy: BaseStrategy, risk_manager: RiskManager):
        self.strategy = strategy
        self.risk_manager = risk_manager

    def run(self, symbol: str, from_date: datetime,
            to_date: datetime, timeframe: str) -> Dict[str, Any]:
        # carregar dados históricos via MT5 ou cache
        # executar lógica de sinais e risco
        # retornar métricas
        ...
