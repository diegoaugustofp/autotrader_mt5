from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class RiskConfig:
    max_risk_per_trade: float  # em %
    max_daily_drawdown: float  # em %
    max_trades_per_day: int


@dataclass
class RiskState:
    current_daily_pnl: float
    trades_today: int
    last_reset_date: Optional[date] = None


class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config
        self.state = RiskState(
            current_daily_pnl=0.0, trades_today=0, last_reset_date=date.today()
        )

    def _check_and_reset_daily_state(self) -> None:
        """Reset state if a new trading day has started."""
        today = date.today()
        if self.state.last_reset_date != today:
            self.state = RiskState(
                current_daily_pnl=0.0, trades_today=0, last_reset_date=today
            )

    def can_open_new_trade(self) -> bool:
        self._check_and_reset_daily_state()
        ...

    def register_trade_result(self, pnl: float) -> None:
        self._check_and_reset_daily_state()
        ...

    def calculate_position_size(
        self, account_balance: float, stop_loss_points: float, tick_value: float
    ) -> float: ...
