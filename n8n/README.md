# n8n – Fluxo de Importação de CSV para Firebird

Este diretório contém o fluxo de automação construído com o n8n para importar dados de um arquivo `.csv` para o banco Firebird.

## 📦 Conteúdo

- `workflow.json`: exportação do fluxo n8n
- `docker-compose.yml`: ambiente para execução local do n8n (opcional)
- `prints/`: imagens demonstrando o funcionamento do fluxo (mínimo 3)

## ⚙️ Funcionalidade do Fluxo

1. **Webhook (POST)** recebe um arquivo `.csv` com colunas `MES`, `ANO`, `TOTAL`.
2. **Parse CSV** transforma o conteúdo em JSON.
3. **HTTP Request** envia os dados para uma API intermediária Flask (`insert_api.py`) que grava no Firebird.
4. **Email** ou outra ação pode ser adicionada ao final como notificação (opcional).

## ▶️ Como usar

1. Execute o n8n com o Docker (opcional):
   ```bash
   docker-compose up -d
Importe workflow.json dentro da interface do n8n (http://localhost:5678).

Envie uma requisição POST com um CSV para o webhook configurado no fluxo.