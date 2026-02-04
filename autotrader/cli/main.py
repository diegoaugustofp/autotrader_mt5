import typer  # opcional, para CLI moderna [web:38]

from autotrader.infra.mt5_client import MT5Client, MT5Config

app = typer.Typer()

@app.command()
def run_live():
    # carregar config, instanciar MT5Client, estratégias, scheduler e iniciar loop
    ...

@app.command()
def backtest(strategy_name: str, symbol: str):
    # carregar config de estratégia, rodar backtest
    ...

if __name__ == "__main__":
    app()
