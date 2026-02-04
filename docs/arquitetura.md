# Arquitetura do Sistema de Trade Automático em Python + MetaTrader 5

## 1. Visão geral

O sistema segue uma arquitetura em camadas para separar claramente integração com corretora, lógica de estratégias, gerenciamento de risco, backtest, persistência e interface. [web:46][web:44][web:47]  
O objetivo é permitir evolução incremental (novas estratégias, novas fontes de dados, novos modos de execução) com impacto mínimo no restante do código. [web:46][web:44]

## 2. Camadas e componentes

### 2.1 Camada de integração (infra/mt5_client.py)

Responsável por toda comunicação com o MetaTrader 5 via pacote `MetaTrader5` em Python. [web:17][web:19][web:24][web:31]  

Principais responsabilidades:

- Inicializar e encerrar conexão com terminal MT5. [web:17][web:19][web:24]  
- Autenticar na conta (login, senha, servidor, caminho do terminal). [web:17][web:19][web:31]  
- Fornecer API para: obter ticks/barras, enviar ordens, consultar posições e histórico. [web:17][web:19][web:24][web:31][web:32]

### 2.2 Camada de domínio de estratégias (core/strategies.py)

Define o modelo de estratégia e parâmetros. [web:32][web:44]  

Principais elementos:

- `StrategyParams`: metadados e config arbitrária da estratégia (por exemplo, período de média, limiar de Z-score). [web:32]  
- `BaseStrategy`: interface abstrata com método `generate_signal`, que recebe dados de mercado e devolve sinal `'BUY'`, `'SELL'` ou `'HOLD'`. [web:32][web:44]

Estratégias concretas (por exemplo, `MeanReversionStrategy`) implementam essa interface. [web:32][web:45]

### 2.3 Camada de gerenciamento de risco (core/risk.py)

Aplica regras de risco por estratégia, independentes da lógica de sinal. [web:22][web:25][web:45]  

Responsabilidades:

- Controlar risco por trade, drawdown diário e número máximo de trades. [web:22][web:25]  
- Calcular tamanho de posição com base no saldo da conta, distância de stop e valor por ponto (tick). [web:45]  
- Decidir se um novo trade pode ser aberto ou se a estratégia deve ser bloqueada temporariamente. [web:22][web:25]

### 2.4 Motor de execução (core/scheduler.py)

Coordena execução ao vivo das estratégias. [web:34][web:46][web:50]  

Responsabilidades:

- Manter lista de instâncias de estratégia (`StrategyInstance`) com seus respectivos gerenciadores de risco, símbolos e janelas de horário. [web:34][web:46]  
- Em loop:  
  - Checar se cada estratégia está ativa e dentro da janela de horário. [web:46]  
  - Buscar dados de mercado via `MT5Client`. [web:17][web:21][web:24]  
  - Invocar `generate_signal` da estratégia. [web:32]  
  - Consultar `RiskManager` para autorização de novo trade. [web:22][web:25]  
  - Enviar ordens quando apropriado. [web:17][web:20][web:32]

### 2.5 Camada de backtest (backtest/runner.py, backtest/metrics.py)

Reutiliza as mesmas estratégias e lógica de risco para simular execuções em dados históricos. [web:32][web:42][web:47]  

Responsabilidades:

- Carregar histórico de preços (via MT5 ou fonte externa). [web:17][web:21][web:32][web:42]  
- Rodar a estratégia barra a barra, aplicando sinais e regras de risco. [web:32][web:42]  
- Calcular métricas: número de trades, retorno total, drawdown máximo, win rate, retorno acumulado etc. [web:42][web:41]

### 2.6 Camada de persistência (infra/repository.py, infra/logging_config.py)

Abstrai armazenamento de configurações e logging. [web:44][web:47]  

Responsabilidades:

- Ler/gravar configurações de estratégias (por exemplo, YAML/JSON, SQLite). [web:47][web:44]  
- Configurar logging em arquivo e console com formatação padronizada. [web:44][web:50]

### 2.7 Interface (cli/main.py e futuro web)

- CLI baseada em `typer` ou `argparse` para: executar sistema ao vivo, gerenciar estratégias e rodar backtests. [web:38][web:47]  
- Futuro painel web (Flask ou FastAPI) reutilizando os mesmos serviços de domínio. [web:37][web:46]

## 3. Fluxos principais

### 3.1 Fluxo de execução ao vivo

1. CLI inicia processo principal. [web:38][web:47]  
2. Configurações são carregadas (MT5, estratégias, risco, horários). [web:44][web:47]  
3. `MT5Client` conecta ao terminal e autentica. [web:17][web:19][web:24][web:31]  
4. `Scheduler` entra em loop, avaliando cada estratégia ativa para cada símbolo configurado. [web:34][web:46][web:50]  
5. Para cada símbolo:  
   - Carrega últimos dados de preço. [web:17][web:21][web:24]  
   - Chama `generate_signal`. [web:32]  
   - Checa limites de risco e, se permitido, envia ordens. [web:22][web:25][web:45]  
6. Todos os eventos relevantes são registrados em log. [web:44][web:50]

### 3.2 Fluxo de backtest

1. CLI chama `BacktestRunner`. [web:42][web:47]  
2. Dados históricos são carregados para o período e símbolo desejados. [web:17][web:21][web:32]  
3. Runner simula passagem do tempo, chamando `generate_signal` a cada barra. [web:32][web:42]  
4. Regras de risco são aplicadas em cada trade. [web:22][web:25][web:45]  
5. Métricas são calculadas ao final e retornadas/exibidas. [web:42][web:41]

## 4. Estrutura de diretórios

Segue a estrutura já alinhada, usada como referência arquitetural. [web:6][web:47][web:34]

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
  pyproject.toml
  README.md
```

5. Estratégia de evolução
- Manter a arquitetura em camadas, adicionando novos adaptadores (por exemplo, outro broker) sem alterar o domínio. [web:44][web:46]
- Permitir que novas estratégias sejam adicionadas como novas classes que estendem BaseStrategy. [web:32][web:44]
- Implementar modos distintos (backtest/simulação/live) definindo apenas camadas de execução e fonte de dados. [web:44][web:47]

 ´´´ text
 
***

## Exemplo de estratégia de mean reversion em ETF americano

Abaixo um exemplo concreto de implementação de estratégia de **mean reversion** sobre um ETF (por exemplo, SPY), inspirada em abordagens comuns com média móvel e Z-score.[5][6][1]

### Estratégia: Mean Reversion simples em SPY

Ideia:  
- Calcular média móvel e desvio padrão de N períodos.[6][1]
- Calcular Z-score \(z = (preço\_atual - média) / desvio\_padrão\).[1]
- Se \(z < -z\_limiar\): sinal de compra (preço “barato” versus média).[5][1]
- Se \(z > z\_limiar\): sinal de venda (preço “caro” versus média).[1][5]
- Caso contrário: segurar posição.[6][1]

### `autotrader/core/strategies.py` (extensão)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np  # para cálculo de média e desvio padrão

@dataclass
class StrategyParams:
    name: str
    description: str
    type: str
    config: Dict[str, Any]

class BaseStrategy(ABC):
    def __init__(self, params: StrategyParams):
        self.params = params

    @abstractmethod
    def generate_signal(self, market_data: Dict[str, Any]) -> str:
        ...

class MeanReversionStrategy(BaseStrategy):
    """
    Estratégia de Mean Reversion baseada em Z-score sobre preço de fechamento.
    market_data deve conter uma lista de fechamentos recentes em 'close_prices'.
    """
    def generate_signal(self, market_data: Dict[str, Any]) -> str:
        closes: List[float] = market_data["close_prices"]
        window: int = self.params.config.get("window", 20)
        z_entry: float = self.params.config.get("z_entry", 2.0)

        if len(closes) < window:
            return "HOLD"

        recent = np.array(closes[-window:])
        mean = recent.mean()
        std = recent.std(ddof=1) if recent.std(ddof=1) > 0 else 1e-8
        last_price = closes[-1]
        z_score = (last_price - mean) / std

        if z_score <= -z_entry:
            return "BUY"
        elif z_score >= z_entry:
            return "SELL"
        return "HOLD"
```
Exemplo de uso no scheduler (trecho conceitual)

``` python
from datetime import datetime, timedelta
from autotrader.core.strategies import StrategyParams, MeanReversionStrategy
from autotrader.core.risk import RiskConfig, RiskManager
from autotrader.core.scheduler import StrategyInstance, Scheduler
from autotrader.infra.mt5_client import MT5Client, MT5Config

# Configuração MT5 (exemplo)
mt5_config = MT5Config(
    login=123456,
    password="***",
    server="Broker-Server",
    path="C:/Program Files/MetaTrader 5/terminal64.exe",
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

# Em produção, chamaríamos:
# scheduler.run_forever()

```


