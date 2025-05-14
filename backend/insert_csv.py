import fdb
import sys
import json

dados_json = sys.argv[1]
registro = json.loads(dados_json)

con = fdb.connect(
    dsn='/firebird/data/employee.fdb',
    user='sysdba',
    password='masterkey'
)
cur = con.cursor()

cur.execute("INSERT INTO csv_import (mes, ano, total) VALUES (?, ?, ?)", (
    int(registro["mes"]),
    int(registro["ano"]),
    float(registro["total"])
))

con.commit()
cur.close()
con.close()
print("✅ Registro inserido:", registro)