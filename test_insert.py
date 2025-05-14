import fdb
import json

dados = {
    "mes": "1",
    "ano": "2023",
    "total": "1234.56"
}

con = fdb.connect(
    dsn='/var/www/desafio-tecnico/novo-teste/desafio-tecnico-python-firebird-n8n/firebird/data/employee.fdb',
    user='sysdba',
    password='masterkey'
)

cur = con.cursor()

cur.execute("INSERT INTO csv_import (mes, ano, total) VALUES (?, ?, ?)", (
    int(dados["mes"]),
    int(dados["ano"]),
    float(dados["total"])
))

con.commit()
cur.close()
con.close()
print("✅ Registro inserido!")
