from flask import Flask, request, jsonify
from flask_cors import CORS
import fdb

app = Flask(__name__)
CORS(app)

@app.route('/insert', methods=['POST'])
def insert():
    data = request.get_json()

    if not data or 'sql' not in data:
        return jsonify({'error': 'Requisição inválida, SQL ausente'}), 400

    sql = data['sql']
    print("[INFO] Comando SQL recebido:", sql)  # <-- LOG visível no terminal

    try:
        con = fdb.connect(
            host='firebird',
            database='/firebird/data/employee.fdb',
            user='sysdba',
            password='masterkey'
        )
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        return jsonify({'executado': sql, 'status': 'success'})

    except Exception as e:
        print("[ERRO] Falha ao executar:", sql)
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)