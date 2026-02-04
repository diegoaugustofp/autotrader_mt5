from dataclasses import dataclass

@dataclass
class RiskConfig:
    max_risk_per_trade: float  # em %
    max_daily_drawdown: float  # em %
    max_trades_per_day: int

@dataclass
class RiskState:
    current_daily_pnl: float
    trades_today: int

class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config
        self.state = RiskState(current_daily_pnl=0.0, trades_today=0)

    def can_open_new_trade(self) -> bool:
        ...

    def register_trade_result(self, pnl: float) -> None:
        ...

    def calculate_position_size(self, account_balance: float,
                                stop_loss_points: float,
                                tick_value: float) -> float:
        ...
