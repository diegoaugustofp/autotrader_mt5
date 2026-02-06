import os
import sys

import typer  # opcional, para CLI moderna [web:38]

from autotrader.infra.mt5_client import MT5Client, MT5Config  # noqa: F401

app = typer.Typer()


def _load_mt5_config() -> MT5Config:
    login_str = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    path = os.getenv("MT5_PATH")

    missing = [
        name
        for name, val in [
            ("MT5_LOGIN", login_str),
            ("MT5_PASSWORD", password),
            ("MT5_SERVER", server),
        ]
        if not val
    ]
    if missing:
        print(
            f"Error: missing required environment variables: {', '.join(missing)}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        login = int(login_str)  # type: ignore[arg-type]
    except ValueError:
        print("Error: MT5_LOGIN must be a valid integer", file=sys.stderr)
        raise SystemExit(1)

    return MT5Config(login=login, password=password, server=server, path=path)  # type: ignore[arg-type]


@app.command()
def run_live():
    config = _load_mt5_config()
    _client = MT5Client(config)  # noqa: F841
    ...


@app.command()
def backtest(strategy_name: str, symbol: str):
    # carregar config de estratégia, rodar backtest
    ...


if __name__ == "__main__":
    app()
