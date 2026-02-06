import typer  # opcional, para CLI moderna
from datetime import datetime, timedelta
from autotrader.infra.mt5_client import MT5Client, MT5Config   
from autotrader.core.strategies import StrategyParams, MeanReversionStrategy
from autotrader.core.risk import RiskConfig, RiskManager
from autotrader.core.scheduler import StrategyInstance, Scheduler

app = typer.Typer()


@app.command()
def run_live():

    # Configuração MT5 (exemplo)
    mt5_config = MT5Config(
        login=969808,
        password="BXMhqb7&",
        server="ActivTradesCorp-Server",
        path="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MetaTrader 5 - ActivTrades/ActivTrades MetaTrader 5.exe",
    )

    mt5_client = MT5Client(mt5_config)

    # Estratégia mean reversion em SPY
    params = StrategyParams(
        name="MR_SPY",
        description="Mean Reversion simples em SPY com Z-score",
        type="mean_reversion",
        config={"window": 20, "z_entry": 2.0},
    )

    strategy = MeanReversionStrategy(params)

    risk_config = RiskConfig(
        max_risk_per_trade=1.0,
        max_daily_drawdown=3.0,
        max_trades_per_day=10,
    )
    risk_manager = RiskManager(risk_config)

    start_time = datetime.now().replace(hour=9, minute=35, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=15, minute=55, second=0, microsecond=0)

    instance = StrategyInstance(
        strategy=strategy,
        risk_manager=risk_manager,
        symbols=["SPY"],
        start_time=start_time,
        end_time=end_time,
        timezone="America/New_York",
    )

    scheduler = Scheduler(mt5_client=mt5_client, strategies=[instance])


@app.command()
def backtest(strategy_name: str, symbol: str):
    # carregar config de estratégia, rodar backtest
    ...


if __name__ == "__main__":
    app()
