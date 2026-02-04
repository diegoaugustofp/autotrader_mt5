# Sistema de Trade Automático em Python Integrado ao MetaTrader 5

## 1. Visão geral do sistema

O sistema é uma plataforma em Python para execução automática de estratégias de trade integradas ao MetaTrader 5 (MT5), focada em ativos do mercado americano, como ações, índices e ETFs, conforme suporte da corretora no MT5. [web:17][web:19][web:24]  
Ele permite cadastrar várias estratégias independentes, cada uma com parâmetros próprios de entrada e saída, gerenciamento de risco, janelas de horário de operação e lista de ativos (tickets) a operar. [web:21][web:22][web:25][web:27]

## 2. Escopo e objetivos

### 2.1 Objetivos

- Automatizar a execução de estratégias de trade definidas pelo usuário através do MT5. [web:17][web:24][web:21]  
- Suportar múltiplas estratégias simultâneas, com configurações isoladas. [web:22][web:25][web:27]  
- Permitir configuração de parâmetros de risco (tamanho da posição, stop loss, take profit, risco por trade, risco diário). [web:22][web:25]  
- Respeitar janelas de horário de negociação baseadas em mercado americano (por exemplo, horário de New York). [web:27]  
- Registrar logs detalhados de sinais, ordens, execuções e erros. [web:21][web:22][web:25][web:27]  
- Fornecer backtest básico usando dados históricos do MT5. [web:17][web:21][web:22][web:27]

### 2.2 Fora de escopo (MVP)

- Interface gráfica complexa (MVP em CLI ou painel web simples). [web:27][web:38]  
- Estratégias baseadas em machine learning avançado (apenas preparar a estrutura para uso futuro). [web:21][web:22][web:25][web:37]

## 3. Requisitos funcionais

### RF01 – Cadastro de estratégias

- O sistema deve permitir criar, editar, ativar/desativar e excluir estratégias de trade. [web:22][web:25]  
- Cada estratégia deve possuir: nome, descrição, tipo (por exemplo, breakout, mean reversion, trend following) e status (ativo/inativo). [web:22][web:25]

### RF02 – Configuração de parâmetros de entrada

- Para cada estratégia, o usuário deve poder definir parâmetros de sinal, como: período de média móvel, janelas de lookback, limiares de volatilidade, indicadores técnicos (RSI, MACD etc.), conforme suportado pela lógica da estratégia. [web:22][web:25][web:27][web:32]  
- Esses parâmetros devem ser armazenados de forma estruturada, por exemplo, em JSON persistido em banco ou arquivo. [web:21][web:22]

### RF03 – Configuração de parâmetros de saída

- Para cada estratégia, o usuário deve definir regras de saída: stop loss em pontos/percentual, take profit, trailing stop, tempo máximo em posição e regras de fechamento no final do pregão. [web:22][web:25][web:27]

### RF04 – Gerenciamento de risco por estratégia

- Para cada estratégia, o sistema deve permitir configurar: [web:22][web:25]  
  - Risco por trade (em valor absoluto ou percentual do capital alocado).  
  - Risco diário máximo (drawdown diário que desativa a estratégia naquele dia).  
  - Número máximo de trades por dia. [web:25][web:27]  
- O sistema deve calcular tamanho da posição com base nesses parâmetros e, opcionalmente, na volatilidade ou preço atual do ativo, conforme a estratégia. [web:22][web:25][web:27][web:38]

### RF05 – Configuração de janelas de horário de execução

- Para cada estratégia, o usuário deve definir horários de início e fim de operação em fuso-horário do mercado americano (por exemplo, America/New_York). [web:27]  
- O sistema não deve abrir novas posições fora da janela configurada, mas pode fechar posições existentes conforme as regras de saída antes do fechamento do mercado. [web:22][web:25][web:27]

### RF06 – Configuração de tickets (ativos) por estratégia

- O sistema deve permitir associar uma lista de símbolos MT5 (por exemplo, AAPL, MSFT, SPY, ES, NQ) para cada estratégia. [web:17][web:19][web:24]  
- Para cada símbolo, podem existir parâmetros específicos, como tamanho mínimo de lote e multiplicador de contrato. [web:17][web:20][web:21][web:31]

### RF07 – Integração com MetaTrader 5

- O sistema deve conectar ao terminal MT5 usando o pacote oficial `MetaTrader5` para Python. [web:17][web:19][web:24][web:31]  
- Deve ser possível:  
  - Autenticar na conta de negociação configurando login, senha, servidor e caminho do terminal. [web:17][web:19][web:24][web:31]  
  - Consultar cotações em tempo real (ticks, barras). [web:17][web:19][web:24][web:31]  
  - Enviar ordens de mercado e pendentes, com stop loss e take profit. [web:17][web:20][web:32][web:33]  
  - Consultar posições abertas, histórico de ordens e negócios. [web:17][web:19][web:31][web:33]

### RF08 – Motor de execução de estratégias

- O sistema deve ter um scheduler que, em loop, verifica periodicamente as estratégias ativas, respeitando as janelas de horário. [web:21][web:22][web:27][web:34][web:37]  
- Para cada estratégia e ativo, o motor deve:  
  - Ler dados de mercado do MT5. [web:17][web:24][web:31]  
  - Aplicar a lógica da estratégia (sinal de compra/venda/mantém). [web:22][web:25][web:27][web:32]  
  - Verificar limites de risco (risco por trade, risco diário, número de trades). [web:22][web:25][web:27][web:38]  
  - Enviar ordens para MT5 quando as condições forem atendidas. [web:17][web:20][web:21][web:32][web:33]

### RF09 – Backtest básico

- O sistema deve permitir rodar um backtest simples por estratégia, usando dados históricos obtidos via MT5, para um intervalo de datas e lista de ativos. [web:17][web:21][web:22][web:27]  
- O resultado deve incluir métricas básicas: número de trades, retorno total, máximo drawdown e win rate. [web:22][web:25][web:27][web:38]

### RF10 – Logs e auditoria

- Todas as decisões de sinal, envio de ordens, erros de conexão e mudanças de configuração devem ser registradas com data/hora e identificador da estratégia. [web:21][web:22][web:25][web:27]  
- Os logs devem ser gravados em arquivo e, opcionalmente, em banco de dados. [web:21][web:22]

### RF11 – Interface de configuração

- MVP: interface em linha de comando (CLI) para gerenciar estratégias, parâmetros e status. [web:27][web:38]  
- Futuro: painel web (Flask ou FastAPI) com autenticação simples para CRUD de estratégias e monitoramento de posições em tempo real. [web:21][web:27][web:29][web:37]

## 4. Requisitos não funcionais

### RNF01 – Linguagem e stack

- A aplicação será implementada em Python 3.x, usando o pacote `MetaTrader5` para integração com MT5. [web:17][web:19][web:24][web:31]

### RNF02 – Desempenho

- O sistema deve ser capaz de avaliar sinais para dezenas de ativos por minuto por estratégia, com latência adicional mínima em relação ao MT5. [web:21][web:22][web:25][web:27][web:37]

### RNF03 – Confiabilidade

- Em caso de erro de conexão com MT5, o sistema deve tentar reconexão automática com política de retry exponencial limitada. [web:21][web:22][web:25][web:27]  
- Em caso de falha crítica, o sistema deve desativar estratégias e registrar erro, evitando ordens inconsistentes. [web:22][web:25][web:27]

### RNF04 – Segurança

- Credenciais de MT5 não devem ficar em texto puro no código, devendo ser lidas de arquivo de configuração protegido ou variáveis de ambiente. [web:21][web:22][web:25][web:37]

### RNF05 – Portabilidade

- O sistema deve rodar em Windows (para uso com terminal MT5 desktop) e, opcionalmente, em Linux com MT5 em contêiner/servidor dedicado. [web:19][web:21][web:27][web:29][web:37]

### RNF06 – Manutenibilidade

- O código deve seguir uma estrutura de projeto Python recomendada, com pacotes e módulos bem definidos e separação de camadas. [web:6][web:34][web:37][web:38]

## 5. Arquitetura e design

### 5.1 Visão arquitetural

Camadas principais: [web:21][web:22][web:27][web:34][web:37]

- Camada de integração MT5: abstrai o pacote `MetaTrader5`, expondo funções de alto nível (obter dados, enviar ordens, consultar posições).  
- Camada de domínio de estratégias: define entidades Estratégia, Parâmetros, Regras de risco e Ativo.  
- Motor de execução: scheduler que orquestra leitura de dados, execução de lógica, checagem de risco e envio de ordens.  
- Camada de persistência: armazenamento de configurações (por exemplo, SQLite ou arquivos YAML/JSON) e logs.  
- Interface (CLI no MVP e, futuramente, painel web).

### 5.2 Estrutura de projeto Python (sugerida)

Repositório seguindo boas práticas de layout de projetos Python. [web:6][web:34][web:37][web:38]

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
## 6. Testes
- Testes unitários para lógica de estratégia (sinais) e módulo de risco. [web:22][web:25][web:27][web:38]
- Testes de integração para o cliente MT5 em conta demo. [web:17][web:19][web:24][web:21][web:31]
- Testes de backtest em cenários controlados para validar consistência de métricas. [web:22][web:25][web:27]
- Testes de carga simples (múltiplas estratégias e ativos) para avaliar desempenho. [web:21][web:22][web:25][web:27][web:37]

## 7. Implantação
- Execução local com MT5 instalado (conta demo e real). [web:17][web:19][web:24][web:31]
- Opcional: empacotamento via ambiente virtual ou contêiner Docker com MT5 + Python, em linha com práticas atuais de servidores quant. [web:21][web:27][web:29][web:37]

## 8. Manutenção e evolução
- Rotina para desativar automaticamente estratégias em caso de comportamento anômalo (por exemplo, drawdown excessivo em curto período). [web:22][web:25][web:27]
- Processo de revisão periódica das estratégias, parâmetros e limites de risco. [web:22][web:25]
- Evoluções planejadas: painel web completo, integração com alertas externos, e uso de modelos de machine learning para geração de sinais. [web:21][web:22][web:25][web:37]
