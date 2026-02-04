# autotrader_mt5
Plataforma em Python para execução automática de estratégias de trade integradas ao MetaTrader 5 (MT5), com foco em ativos negociados em bolsas americanas (ações, índices, ETFs, futuros, conforme suportado pela corretora no MT5).


# Design (arquitetura)

## Visão arquitetural
Arquitetura em camadas:

- **Camada de integração MT5**: abstrai o pacote MetaTrader5, expondo funções de alto nível (obter dados, enviar ordens, consultar posições).
- **Camada de domínio de estratégias:** define entidades Estratégia, Parâmetros, Regras de risco, Ativo.
- **Motor de execução:** scheduler que orquestra leitura de dados, execução de lógica, checagem de risco e envio de ordens.
- **Camada de persistência:** armazenamento de configurações (por exemplo, SQLite ou arquivos YAML/JSON) e logs.
- **Interface (CLI e opcional web).**

​
## Estrutura de projeto Python (sugerida)
O projeto segue seguinte estrutura de pastas:

```text
autotrader_mt5/
  autotrader/
    __init__.py
    config/
      __init__.py
      settings.py
    core/
      strategies.py
      risk.py
      scheduler.py
    infra/
      mt5_client.py
      repository.py
      logging_config.py
    backtest/
      runner.py
      metrics.py
    cli/
      main.py
  tests/
    test_strategies.py
    test_risk.py
    test_mt5_client.py
  docs/
    requisitos_funcionais.md
    arquitetura.md
  pyproject.toml / setup.cfg
  README.md
