# Backend

Este diretório contém o backend responsável por consultar o banco Firebird, gerar arquivos CSV e um gráfico PNG com o total de vendas por mês.

## Como rodar o backend

1. **Pré-requisitos:**

   - Python 3.10+
   - Instalar as dependências:
     ```powershell
     pip install -r requirements.txt
     ```
   - Ter o arquivo `employee.fbk` (banco Firebird) na raiz do projeto.
   - **Para usar a IA (Gemini 2.0):**
     - Crie uma conta no [Google AI Studio](https://aistudio.google.com/app/apikey)
     - Gere uma API Key e configure no ambiente conforme instruções do frontend.

2. **Executar a consulta e gerar arquivos:**

   - Rode o script principal:
     ```powershell
     python main.py
     ```
   - Isso irá gerar:
     - `vendas_mes.csv` e `total_por_vendedor.csv` (na pasta src)
     - `grafico.png` (gráfico de vendas por mês)

3. **Exportar e disparar fluxo n8n:**
   - Após gerar os arquivos, execute:
     ```powershell
     python export.py
     ```
   - Este script irá acionar o endpoint do n8n para enviar o CSV e iniciar o fluxo de automação.

Veja o README da pasta n8n para detalhes do fluxo automatizado.
