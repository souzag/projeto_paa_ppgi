# E-VRPSPD com VNS: Solução para Problema de Roteamento de Veículos Elétricos com Coleta e Entrega Simultâneas

Este projeto implementa uma solução avançada para o Problema de Roteamento de Veículos Elétricos com Coleta e Entrega Simultâneas (E-VRPSPD), utilizando heurísticas iniciais (Nearest Neighbor e Clarke & Wright modificado) e meta-heurística Busca em Vizinhança Variável (VNS) com operadores específicos para otimização de recarga.

## Funcionalidades Principais
- **Heurísticas Iniciais**: Nearest Neighbor (gulosa) e Clarke & Wright (savings com integração de estações).
- **Meta-heurística VNS**: Shake e local search com operadores undo-move para eficiência.
- **Operadores Específicos**: Relocate, swap, 2-opt, relocate_station, swap_station para otimizar rotas e estratégia de recarga.
- **Validação Estatística**: Múltiplas execuções, métricas de custo/tempo, análise de convergência.
- **Benchmarking**: Comparação entre métodos, geração automática de instâncias, logs detalhados.
- **Visualização**: Gráficos de rotas, benchmarks e convergência.

## Estrutura do Projeto
```
projeto_paa_ppgi/
├── data/
│   └── instancia_teste.json          # Instância exemplo
├── src/
│   ├── problem.py                    # Classes: Node, Customer, Depot, Vehicle, Route
│   ├── utils.py                      # Funções auxiliares, geração de instâncias
│   ├── initial_solution.py           # Heurísticas iniciais
│   ├── neighborhoods.py              # Operadores de vizinhança
│   ├── vns.py                        # Meta-heurística VNS
│   └── visualization.py              # Funções de plot
├── tests/
│   ├── test_neighborhoods.py         # Testes unitários
│   ├── test_integration.py           # Testes de integração
│   ├── test_performance.py           # Testes de desempenho
│   └── test_edge_cases.py            # Casos extremos
├── main.py                           # Execução principal
├── run_experiments.py                # Experimentos automatizados
├── requirements.txt                  # Dependências
├── .gitignore                        # Arquivos ignorados
└── README.md                         # Esta documentação
```

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto_paa_ppgi.git
   cd projeto_paa_ppgi
   ```

2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate no Windows
   ```

3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
### Execução Básica
```bash
python main.py [num_customers] [num_stations] [seed]
# Exemplo: python main.py 50 5 42
```
Gera instância, executa NN, C&W, VNS, salva logs e gráficos.

### Experimentos Automatizados
```bash
python run_experiments.py
```
Executa múltiplas instâncias, salva logs cumulativos em `cumulative_performance_log.json`.

### Testes
```bash
python -m pytest tests/ -v
```

## Resultados e Análise
### Comparação de Métodos (Instância 50 clientes)
- **NN**: Custo 768.61, 2 rotas, rápido (~0.0002s).
- **C&W**: Custo 1391.60, 1 rota, falha em otimizar recargas.
- **VNS pos-NN**: Custo 768.61, sem melhoria (solução já boa).
- **VNS pos-C&W**: Custo médio 1339.65 ±40.30, melhoria ~3.73% consistente.

### Impacto dos Operadores de Estação
- Em cenários onde C&W gera soluções subótimas (ex: ignorando recargas), operadores específicos recuperam qualidade.
- Melhorias de 1.7-4% em instâncias grandes, demonstrando valor para E-VRPSPD.

### Validação Estatística
- 30 execuções por método, métricas de min/max/média/desvio.
- Gráficos de convergência mostram estabilização rápida.

## Arquitetura e Design
- **Undo Moves**: Operadores modificam soluções in-place e revertem se inviáveis, reduzindo memória.
- **Modularidade**: Separação clara entre modelagem, algoritmos e testes.
- **Escalabilidade**: Suporte a instâncias 50-100+ clientes via geração automática.

## Melhorias Futuras
- Paralelização para execuções múltiplas.
- Integração com datasets padrão (Solomon VRPTW adaptado).
- Interface web para visualização interativa.
- Suporte a múltiplos veículos/depósitos.

## Contribuição
1. Fork o projeto.
2. Crie uma branch para sua feature.
3. Adicione testes.
4. Faça commit e pull request.

## Licença
Este projeto é open-source sob licença MIT.

## Contato
Para dúvidas, abra uma issue no GitHub.