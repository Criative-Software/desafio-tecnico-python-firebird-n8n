# n8n

Este diretório contém a automação do fluxo usando o n8n.

## Como rodar o n8n

1. **Pré-requisitos:**

   - Docker e Docker Compose instalados.

2. **Subir o n8n:**

   - Execute o comando:
     ```powershell
     docker-compose up -d
     ```
   - O n8n estará disponível em `http://localhost:5678`.

3. **Fluxo automatizado:**

   - O backend dispara um webhook do n8n ao rodar `export.py`.
   - O fluxo do n8n:
     1. Recebe o CSV via webhook.
     2. Passa o CSV para um node Function que converte para JSON.
     3. Envia um e-mail para `processo@empresa.com` com os dados.

4. **Gerenciamento do fluxo:**
   - O fluxo está salvo em `WorkFlow.json`.
   - Imagens do fluxo estão em `prints/`.

Veja o README do backend para saber como disparar o fluxo e o do frontend para consumir os dados.
