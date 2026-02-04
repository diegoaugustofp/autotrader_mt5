from typing import List
from datetime import datetime
from .strategies import BaseStrategy
from .risk import RiskManager
from ..infra.mt5_client import MT5Client

class StrategyInstance:
    def __init__(self, strategy: BaseStrategy, risk_manager: RiskManager,
                 symbols: List[str], start_time, end_time, timezone):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.symbols = symbols
        self.start_time = start_time
        self.end_time = end_time
        self.timezone = timezone
        self.active = True

class Scheduler:
    def __init__(self, mt5_client: MT5Client, strategies: List[StrategyInstance]):
        self.mt5_client = mt5_client
        self.strategies = strategies

    def run_forever(self):
        while True:
            now = datetime.now()
            for s in self.strategies:
                if not s.active:
                    continue
                # checar janela de horário, risco etc.
                # buscar dados de mercado, gerar sinal, enviar ordens
                ...
            # dormir um pequeno intervalo
            ...
