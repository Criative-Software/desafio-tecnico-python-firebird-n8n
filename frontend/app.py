from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from datetime import datetime
import os
import sys
import json

# Adiciona o diretório do backend ao path
sys.path.append('../backend')
from main import consultar_vendas_por_mes, gerar_grafico

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_vendas', methods=['POST'])
def buscar_vendas():
    try:
        mes_ano = request.json.get('mes_ano')
        if not mes_ano:
            return jsonify({'erro': 'Mês/ano não fornecido'}), 400

        # Consulta vendas usando o backend
        df = consultar_vendas_por_mes(mes_ano)
        
        # Converte DataFrame para lista de dicionários
        dados = df.to_dict('records')
        return jsonify(dados)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/exportar_excel', methods=['POST'])
def exportar_excel():
    try:
        mes_ano = request.json.get('mes_ano')
        if not mes_ano:
            return jsonify({'erro': 'Mês/ano não fornecido'}), 400

        # Consulta vendas usando o backend
        df = consultar_vendas_por_mes(mes_ano)
        
        # Criar diretório para arquivos temporários se não existir
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        # Salvar arquivo Excel
        filename = f'temp/vendas_{mes_ano}.xlsx'
        df.to_excel(filename, index=False)
        
        return send_file(filename, as_attachment=True, download_name='vendas_mes.xlsx')
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/grafico_vendas')
def grafico_vendas():
    mes_ano = request.args.get('mes_ano')
    if not mes_ano:
        return 'Mês/ano não fornecido', 400
    # Caminho absoluto para o gráfico
    caminho = os.path.abspath(os.path.join('../backend/imagens', f'vendas_{mes_ano}.png'))
    if not os.path.exists(caminho):
        # Tenta gerar o gráfico sob demanda
        try:
            df = consultar_vendas_por_mes(mes_ano)
            if not df.empty:
                gerar_grafico(df, mes_ano)
        except Exception as e:
            return f'Erro ao gerar gráfico: {str(e)}', 500
    if not os.path.exists(caminho):
        return 'Gráfico não encontrado', 404
    return send_file(caminho, mimetype='image/png')

@app.route('/baixar_csv')
def baixar_csv():
    mes_ano = request.args.get('mes_ano')
    if not mes_ano:
        return 'Mês/ano não fornecido', 400
    
    # Criar diretório para relatórios se não existir
    relatorios_dir = os.path.abspath(os.path.join('../backend/relatorios'))
    if not os.path.exists(relatorios_dir):
        os.makedirs(relatorios_dir)
    
    # Nome fixo para o arquivo
    caminho = os.path.abspath(os.path.join(relatorios_dir, 'vendas_mes.csv'))
    
    # Tenta gerar o CSV
    try:
        df = consultar_vendas_por_mes(mes_ano)
        if not df.empty:
            df.to_csv(caminho, index=False, encoding='utf-8')
    except Exception as e:
        return f'Erro ao gerar CSV: {str(e)}', 500
        
    if not os.path.exists(caminho):
        return 'CSV não encontrado', 404
    return send_file(caminho, as_attachment=True, download_name='vendas_mes.csv')

if __name__ == '__main__':
    app.run(debug=True) 