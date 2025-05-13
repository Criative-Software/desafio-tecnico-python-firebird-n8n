## 🔧 Desafio Back‑end (Python + Firebird 2.5)

### 🎯 Objetivo
Conectar ao banco Firebird, realizar consultas e gerar relatórios com visualização gráfica.

### 🧩 Tarefas

1. Crie um ambiente virtual:  
   `python -m venv venv && source venv/bin/activate`
2. Instale dependências:  
   `pip install -r backend/requirements.txt`  
   *(exemplos: `fdb`, `pandas`, `matplotlib`)*
3. Implemente o `main.py` com:
   - Conexão ao Firebird:  
     `host=localhost`, `database=employee.fdb`, `user=sysdba`, `password=masterkey`
   - Realize duas consultas SQL:
     - `vendas_por_mes`
     - `total_por_vendedor`
   - Salve os resultados em arquivos `.csv`
   - Gere um gráfico de barras `grafico.png`

4. Documente a execução no `backend/README.md` com até **10 linhas**.

### ✔️ Critérios de Avaliação

| Peso | Item                           |
| ---: | ------------------------------ |
| 40 % | Roda sem erros, gera CSV + PNG |
| 30 % | SQL correta e performática     |
| 20 % | Código limpo (PEP‑8, funções)  |
| 10 % | README objetivo                |
