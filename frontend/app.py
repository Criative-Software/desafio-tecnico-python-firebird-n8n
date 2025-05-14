from flask import Flask, render_template, request, send_file, session
import pandas as pd
import os
import fdb
import json

FIREBIRD_CONFIG = {
    "host": "localhost",
    "database": "/firebird/data/employee.fdb",
    "user": "sysdba",
    "password": "masterkey",
    "port": 3050
}

def get_dados_firebird_csv_import():
    try:
        con = fdb.connect(**FIREBIRD_CONFIG)
        cur = con.cursor()
        cur.execute("SELECT MES, ANO, TOTAL FROM csv_import")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Mês", "Ano", "Total"])
        con.close()
        return df
    except Exception as e:
        print("Erro ao conectar no Firebird:", e)
        return pd.DataFrame()

app = Flask(__name__)
app.secret_key = 'alguma_chave_segura'

@app.route('/', methods=['GET', 'POST'])
def index():
    vendas = []
    mes = None
    ano = None
    erro = None
    df_csv = pd.DataFrame()

    try:
        con = fdb.connect(**FIREBIRD_CONFIG)
        cur = con.cursor()
        cur.execute("SELECT DISTINCT ANO FROM csv_import ORDER BY ANO")
        anos_disponiveis = [row[0] for row in cur.fetchall()]
        con.close()
    except Exception as e:
        anos_disponiveis = []
        print("Erro ao buscar anos:", e)

    if request.method == 'POST':
        mes = request.form.get('mes', type=int)
        ano = request.form.get('ano', type=int)

        if 'buscar' in request.form and mes and ano:
            try:
                con = fdb.connect(**FIREBIRD_CONFIG)
                cur = con.cursor()
                cur.execute("SELECT MES, ANO, TOTAL FROM csv_import WHERE MES=? AND ANO=?", (mes, ano))
                rows = cur.fetchall()
                df_csv = pd.DataFrame(rows, columns=["Mês", "Ano", "Total"])
                con.close()
                session['df_csv'] = df_csv.to_json()
            except Exception as e:
                erro = f"Erro ao buscar dados: {e}"

        if 'exportar' in request.form:
            df = pd.DataFrame()
            if 'df_csv' in session:
                df = pd.read_json(session['df_csv'])
            if not df.empty:
                filepath = os.path.join('exports', 'vendas_mes.xlsx')
                df.to_excel(filepath, index=False)
                return send_file(filepath, as_attachment=True)
            else:
                erro = "Nenhum dado disponível para exportação."

    if 'df_csv' in session:
        df_csv = pd.read_json(session['df_csv'])

    return render_template('index.html', df_csv=df_csv, mes=mes, ano=ano, anos_disponiveis=anos_disponiveis, erro=erro)

if __name__ == '__main__':
    os.makedirs('exports', exist_ok=True)
    app.run(debug=True, host='0.0.0.0')