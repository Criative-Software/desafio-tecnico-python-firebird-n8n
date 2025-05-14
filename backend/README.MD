# Backend – Desafio Técnico

Este script conecta ao banco Firebird (`employee.fdb`), executa duas consultas SQL e gera relatórios em `.csv` e um gráfico em `.png`.

# Passos para execução:
1. Crie o ambiente virtual:
   `python3.6 -m venv venv && source venv/bin/activate`
2. Instale as dependências:
   `pip install -r backend/requirements.txt`
3. Execute o script:
   `python backend/main.py`

O script gera `vendas_por_mes.csv`, `total_por_vendedor.csv` e `grafico.png`.

---

<!--
🛠️ Dica: Restaurando o banco com Docker

1. Suba o container:
   docker compose -f firebird/docker-compose.yml up -d

2. Restaure o backup employee.fbk:
   ./firebird/restore.sh

3. Confirme que employee.fdb foi criado em firebird/data/
-->