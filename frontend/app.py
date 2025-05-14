from flask import Flask, render_template, request, send_file
import fdb
import pandas as pd
import io
from datetime import datetime
import calendar
import os

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

def get_available_months():
    con, cur = db_connection()
    try:
        cur.execute("""
            SELECT DISTINCT EXTRACT(YEAR FROM ORDER_DATE) AS ANO, 
                           EXTRACT(MONTH FROM ORDER_DATE) AS MES 
            FROM SALES 
            ORDER BY ANO DESC, MES DESC
        """)
        results = cur.fetchall()
       
        months_years = []
        for row in results:
            year, month = int(row[0]), int(row[1])
            month_name = calendar.month_name[month]
            months_years.append({
                'value': f"{year}-{month:02d}",
                'display': f"{month_name} {year}"
            })
        return months_years
    except Exception as e:
        print(f"Erro ao obter meses disponíveis: {str(e)}")
        current_date = datetime.now()
        months_years = []
        for i in range(12):
            year = current_date.year
            month = current_date.month - i
            if month <= 0:
                month += 12
                year -= 1
            month_name = calendar.month_name[month]
            months_years.append({
                'value': f"{year}-{month:02d}",
                'display': f"{month_name} {year}"
            })
        return months_years
    finally:
        con.close()

def sales_by_month(year_month):
    year, month = map(int, year_month.split('-'))
    con, cur = db_connection()
    try:
        cur.execute("""
            SELECT
                S.PO_NUMBER
                S.ORDER_DATE,
                C.CONTACT_FIRST AS CLIENT,
                S.QTY_ORDERED,
                S.TOTAL_VALUE,
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
    finally:
        con.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    available_months = get_available_months()
    selected_month = request.form.get('month') if request.method == 'POST' else None
    
    if selected_month:
        sales_data, columns = sales_by_month(selected_month)
    else:
        sales_data, columns = [], []
    
    return render_template('./index.html', 
                          available_months=available_months,
                          selected_month=selected_month,
                          sales_data=sales_data,
                          columns=columns)

@app.route('/export', methods=['POST'])
def export_excel():
    selected_month = request.form.get('month')
    if not selected_month:
        return "Mês não selecionado", 400
    
    sales_data, columns = sales_by_month(selected_month)
    
    df = pd.DataFrame(sales_data)
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Vendas', index=False)
        
        worksheet = writer.sheets['Vendas']
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)
    
    output.seek(0)
    
    year, month = selected_month.split('-')
    month_name = calendar.month_name[int(month)]
    filename = f"vendas_{month_name}_{year}.xlsx"
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)