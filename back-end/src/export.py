import requests
import pandas as pd

# URL do webhook do n8n
WEBHOOK_URL = "http://localhost:5678/webhook-test/export-csv"

# Carregar CSV e converter para JSON
df = pd.read_csv("vendas_mes.csv")
json_data = df.to_dict(orient="records")  # Transforma cada linha em um objeto JSON

# Enviar JSON via POST para o n8n
response = requests.post(WEBHOOK_URL, json=json_data)

# Exibir o retorno do n8n
print("Status:", response.status_code)
print("Resposta:", response.text)
