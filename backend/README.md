# Desafio Back-end Python + Firebird 2.5

Este script conecta ao banco Firebird `employee.fdb`, realiza consultas SQL para analisar vendas por mês e total por vendedor, produzindo dois relatórios principais. Os resultados são exportados em formato CSV e visualizados em gráficos de barras.

## Requisitos
- Python 3.8+ e Firebird 2.5
- Bibliotecas: `fdb`, `pandas`, `matplotlib` (instale via `pip install -r requirements.txt`)

## Execução
1. Ative o ambiente: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
2. Execute: `python main.py`
3. Resultados em `arquivos_csv/` e `graficos/`
