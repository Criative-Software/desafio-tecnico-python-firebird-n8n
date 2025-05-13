# Frontend

Este diretório contém a interface web para visualizar os dados processados.

## Como rodar o frontend

1. **Pré-requisitos:**

   - Python 3.10+
   - Instale as dependências necessárias para o backend Flask e manipulação de dados:
     ```powershell
     pip install flask flask-cors pandas openpyxl google-generativeai
     ```
   - (Opcional) Crie um ambiente virtual:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. **Executar o backend do frontend:**

   - Rode o app Flask para expor as rotas e endpoints:
     ```powershell
     python app.py
     ```
   - O backend estará disponível em `http://localhost:5000`

3. **Executar a interface web:**

   - Utilize uma extensão como **Live Server** ou **Five Server** no VS Code para rodar o front-end estático (HTML/JS/CSS).
   - Clique com o botão direito no arquivo `index.html` e selecione "Open with Live Server" ou "Open with Five Server".
   - Acesse a URL disponibilizada pela extensão (ex: `http://127.0.0.1:5500/front-end/`).

4. **Fluxo de uso:**

   - O app Flask (`app.py`) deve estar rodando para que a interface web consiga acessar as rotas e triggar os endpoints.
   - A interface web faz requisições para:
     - `/buscar`: buscar dados do CSV filtrando por mês/ano.
     - `/gerar_insights`: obter análise da IA Gemini 2.0.
     - `/gerar_excel`: exportar o arquivo em Excel (.xlsx).

5. **Funcionalidades:**
   - Buscar dados do CSV em formato de tabela.
   - Ver mensagem de análise do Gemini 2.0.
   - Exportar o arquivo em Excel (.xlsx).

Veja o README do backend para gerar os arquivos necessários e o do n8n para o fluxo automatizado.
