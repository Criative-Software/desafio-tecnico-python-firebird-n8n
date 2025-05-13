from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# ✅ Configurar API da IA com segurança
GOOGLE_API_KEY = "YOUR_API_KEY" # Pegue da variável de ambiente
genai.configure(api_key=GOOGLE_API_KEY)

# 📌 Caminhos dos arquivos
CSV_PATH = os.path.abspath("../back-end/src/vendas_mes.csv")
EXCEL_PATH = os.path.abspath("../back-end/src/dados_completos.xlsx")

@app.route("/", methods=["GET"])
def home():
    return jsonify("Bem-vindo ao back-end do desafio!")

@app.route("/buscar", methods=["GET"])
def buscar():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"erro": "Arquivo CSV não encontrado."})

        df = pd.read_csv(CSV_PATH)
        mes, ano = int(request.args.get("mes")), int(request.args.get("ano"))
        df_filtrado = df[(df["mes"] == mes) & (df["ano"] == ano)]

        return jsonify(df_filtrado.to_dict(orient="records")) if not df_filtrado.empty else jsonify([])
    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route("/gerar_insights", methods=["GET"])
def gerar_insights():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"erro": "Arquivo CSV não encontrado."})

        df = pd.read_csv(CSV_PATH)

        # insights_data = {"Vendas por Mês (Dados)": df.to_markdown()}
        # prompt = f"Analise os dados de vendas abaixo:\n\n{insights_data}\n\nForneça insights e recomendações."

        # Constrói o prompt com uma instrução para resumir em poucas frases
        insights_data = {"Dados de Vendas": df.to_markdown()}
        prompt = """
        Analise os dados de vendas abaixo e gere um resumo curto e conciso com até 3 frases. 
        Destaque os principais pontos, como variações significativas, outliers e tendências estratégicas.
        
        Dados para Análise:
        """
        for key, value in insights_data.items():
            prompt += f"\n\n## {key}:\n{value}"
        prompt += "\n\nResumo:"

        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)

        return jsonify({"insights": response.text})
    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route("/gerar_excel", methods=["GET"])
def gerar_excel():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"erro": "Arquivo CSV não encontrado."})

        df = pd.read_csv(CSV_PATH)
        df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")

        return send_file(EXCEL_PATH, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
