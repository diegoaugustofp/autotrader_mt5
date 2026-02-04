from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import MetaTrader5 as mt5  # noqa: F401  # [web:17][web:24][web:19]


@dataclass
class MT5Config:
    login: int
    password: str
    server: str
    path: Optional[str] = None


class MT5Client:
    def __init__(self, config: MT5Config):
        self.config = config

    def connect(self) -> bool:
        # inicializa e faz login no MT5
        ...

    def disconnect(self) -> None: ...

    def get_ticks(self, symbol: str, from_time, to_time) -> List[Dict[str, Any]]: ...

    def get_bars(self, symbol: str, timeframe, count: int) -> List[Dict[str, Any]]: ...

    def send_order(
        self,
        symbol: str,
        volume: float,
        order_type: str,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        comment: str = "",
    ) -> Dict[str, Any]: ...

    def get_open_positions(self) -> List[Dict[str, Any]]: ...

    def get_history_deals(self, from_time, to_time) -> List[Dict[str, Any]]: ...
