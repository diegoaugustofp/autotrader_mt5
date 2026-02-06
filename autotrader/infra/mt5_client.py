from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import MetaTrader5 as mt5  


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
        mt5.login(
            login=self.config.login,
            password=self.config.password,
            server=self.config.server,
        )   

    def disconnect(self) -> None: 
        mt5.shutdown()

    def get_ticks(self, symbol: str, from_time, to_time) -> List[Dict[str, Any]]: 
        ticks = mt5.copy_ticks_range(symbol, from_time, to_time, mt5.COPY_TICKS_ALL)
        return [tick._asdict() for tick in ticks] if ticks is not None else []


    def get_bars(self, symbol: str, timeframe, count: int) -> List[Dict[str, Any]]: 
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        return [bar._asdict() for bar in bars] if bars is not None else []     

    def send_order(
        self,symbol: str,volume: float,order_type: str,sl: Optional[float] = None,tp: Optional[float] = None,comment: str = "",) -> Dict[str, Any]: 
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL,
                "sl": sl,
                "tp": tp,
                "comment": comment,
            }
            result = mt5.order_send(request)
            return result._asdict() if result is not None else {"error": "Failed to send order"}
            

    def get_open_positions(self) -> List[Dict[str, Any]]: 
        positions = mt5.positions_get()
        return [positions._asdict() for position in positions] if positions is not None else []

    def get_history_deals(self, from_time, to_time) -> List[Dict[str, Any]]: 
        deals = mt5.history_deals_get(from_time, to_time)
        return [deals._asdict() for deal in deals] if deals is not None else []
