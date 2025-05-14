from fastapi import FastAPI, Request, HTTPException
import fdb
import os
import traceback

app = FastAPI(
    title="CSV Importer",
    description="Recebe JSON de vendas por mês e insere no Firebird na tabela csv_import",
    version="1.0.0"
)

DB_HOST = os.getenv("FIREBIRD_HOST", "firebird")
DB_PORT = int(os.getenv("FIREBIRD_PORT", "3050"))
DB_FILE = os.getenv("FIREBIRD_DATABASE", "/firebird/data/EMPLOYEE.FDB")
DB_USER = os.getenv("FIREBIRD_USER", "sysdba")
DB_PASS = os.getenv("ISC_PASSWORD", "masterkey")

@app.post("/api/import-csv")
async def import_csv(request: Request):
    try:
        payload = await request.json()
        print("🔄 Recebido JSON:", payload)

        if not isinstance(payload, list):
            raise HTTPException(status_code=400, detail="Payload deve ser uma lista de objetos JSON.")

        print(f"🔌 Conectando ao Firebird em {DB_HOST}:{DB_PORT}, arquivo {DB_FILE}...")
        con = fdb.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_FILE,
            user=DB_USER,
            password=DB_PASS
        )
        cur = con.cursor()
        print("✅ Conexão estabelecida.")

        inserted = 0
        for row in payload:
            try:
                ano = int(row["ano"])
                mes = int(row["mes"])
                total_vendas = float(row["total_vendas"])
                print(f"📥 Inserindo: ano={ano}, mes={mes}, total_vendas={total_vendas}")
                cur.execute(
                    "INSERT INTO csv_import (ano, mes, total_vendas) VALUES (?, ?, ?)",
                    (ano, mes, total_vendas)
                )
                inserted += 1
            except Exception:
                print("❌ Erro na linha:", row)
                print(traceback.format_exc())
                continue

        con.commit()
        cur.close()
        con.close()
        print(f"✅ {inserted} linhas inseridas com sucesso.")
        return {"status": "ok", "inserted_rows": inserted}

    except HTTPException:
        raise
    except Exception as e:
        print("🔥 Erro interno:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
