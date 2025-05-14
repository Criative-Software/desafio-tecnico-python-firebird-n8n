FROM python:3.10-slim

WORKDIR /app

# Instala a biblioteca cliente do Firebird
RUN apt-get update && apt-get install -y libfbclient2 firebird-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api_import_csv:app", "--host", "0.0.0.0", "--port", "8000"]
