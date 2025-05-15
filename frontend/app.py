from flask import Flask, render_template, request, send_file
import fdb
import pandas as pd
import io
from datetime import datetime
import calendar
import os

MESES_PT = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',
        4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro',
        10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

app = Flask(__name__)

def db_connection():
    """
    Estabelece conexão com o banco de dados Firebird.
    
    Args:
        host: Endereço do servidor do banco de dados
        database: Nome do banco de dados
        user: Nome de usuário para conexão
        password: Senha do usuário
        
    Returns:
        Tupla com a conexão e cursor do banco de dados
    """
    try:
        con = fdb.connect(host='localhost', 
                        database='employee',
                        user='sysdba', 
                        password='masterkey')
        cur = con.cursor()
        return con, cur
    except fdb.Error as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {str(e)}")

def get_available_years():
    con, cur = db_connection()
    try:
        cur.execute("""
            SELECT DISTINCT EXTRACT(YEAR FROM ORDER_DATE) AS ANO
            FROM SALES 
            ORDER BY ANO DESC
        """)
        results = cur.fetchall()
       
        years = [int(row[0]) for row in results]

        return years
    
    except Exception as e:
        print(f"Erro ao obter anos disponíveis: {str(e)}")
        
    finally:
        con.close()

def get_all_months():
    return [{'value': i, 'display': MESES_PT[i]} for i in range(1, 13)]

def get_sales_by_month_year(year, month):
    con, cur = db_connection()
    try:
        cur.execute("""
            SELECT
                S.PO_NUMBER,
                S.ORDER_DATE,
                C.CONTACT_FIRST AS CLIENT,
                S.QTY_ORDERED,
                S.TOTAL_VALUE
            FROM
                SALES S
            JOIN
                CUSTOMER C ON S.CUST_NO = C.CUST_NO
            WHERE
                EXTRACT(YEAR FROM S.ORDER_DATE) = ?
                AND EXTRACT(MONTH FROM S.ORDER_DATE) = ?
            ORDER BY
                S.ORDER_DATE
        """, (year, month))
        
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()

        sales_data = []
        for row in results:
            sale = {}
            for i, col in enumerate(columns):
                sale[col] = row[i]
            sales_data.append(sale)
            
        return sales_data, columns
    
    except Exception as e:
        app.logger.error(f"Erro ao buscar vendas: {str(e)}")
        return [], []
    finally:
        con.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    available_years = get_available_years()
    available_months = get_all_months()    
    selected_year = None
    selected_month = None
    sales_data = []
    columns = []
    
    if request.method == 'POST':
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        
        if selected_year and selected_month:
            selected_year = int(selected_year)
            selected_month = int(selected_month)
            sales_data, columns = get_sales_by_month_year(selected_year, selected_month)
    
    return render_template('index.html', 
                          available_years=available_years,
                          available_months=available_months,
                          selected_year=selected_year,
                          selected_month=selected_month,
                          sales_data=sales_data,
                          columns=columns)


@app.route('/export', methods=['POST'])
def export_excel():
    selected_year = request.form.get('year')
    selected_month = request.form.get('month')
    
    if not selected_year or not selected_month:
        return "Mês e ano não selecionados", 400
    
    selected_year = int(selected_year)
    selected_month = int(selected_month)
    sales_data, columns = get_sales_by_month_year(selected_year, selected_month)
    
    df = pd.DataFrame(sales_data)

    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Vendas', index=False)
        
        worksheet = writer.sheets['Vendas']
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)
    
    output.seek(0)
    
    month_name = MESES_PT[selected_month]
    filename = f"vendas_{month_name.lower()}_{selected_year}.xlsx"
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)