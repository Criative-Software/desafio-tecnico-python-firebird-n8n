from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Caminho do CSV de vendas
CSV_PATH = os.path.join(os.path.dirname(__file__), 'vendas.csv')

@app.route('/vendas', methods=['GET'])
def vendas():
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    
    query = f"""
        SELECT EXTRACT(MONTH FROM SALE_DATE) AS mes, 
               EXTRACT(YEAR FROM SALE_DATE) AS ano, 
               SUM(AMOUNT) AS total_vendas
        FROM SALES
        WHERE EXTRACT(MONTH FROM SALE_DATE) = {mes} 
          AND EXTRACT(YEAR FROM SALE_DATE) = {ano}
        GROUP BY EXTRACT(MONTH FROM SALE_DATE), EXTRACT(YEAR FROM SALE_DATE)
    """

    try:
        conn = connect_db()
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Verificando se as colunas "mes" e "ano" existem
        if 'mes' not in df.columns or 'ano' not in df.columns:
            return jsonify({'erro': 'CSV inválido. Colunas "mes" e "ano" ausentes.'}), 400
        
        result = df.to_dict(orient='records')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/exportar', methods=['GET'])
def exportar_excel():
    mes = int(request.args.get('mes'))
    ano = int(request.args.get('ano'))

    try:
        df = pd.read_csv(CSV_PATH)
        df_filtrado = df[(df['mes'] == mes) & (df['ano'] == ano)]

        export_path = os.path.join(os.path.dirname(__file__), 'vendas_filtradas.xlsx')
        df_filtrado.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
