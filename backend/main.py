import fdb
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import seaborn as sns
from pathlib import Path

def create_dir():
    """Cria diretórios para armazenar arquivos de saída se não existirem."""
    Path("backend/files").mkdir(parents=True, exist_ok=True)
    Path("backend/charts").mkdir(parents=True, exist_ok=True)


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

def execute_query(cursor, query):
    """
    Executa uma consulta SQL no banco de dados.
    
    Args:
        cursor: Cursor do banco de dados
        query: Consulta SQL a ser executada
        
    Returns:
        Lista de resultados da consulta
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except fdb.Error as e:
        raise RuntimeError(f"Erro ao executar consulta: {str(e)}")
    
def save_to_csv(file_path, results, headers):
    """
    Salva os resultados da consulta em um arquivo CSV.
    
    Args:
        file_path: Caminho do arquivo CSV a ser criado
        results: Resultados da consulta
        headers: Cabeçalhos para as colunas do CSV
    """
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(results)
    except IOError as e:
        raise IOError(f"Erro ao salvar arquivo CSV: {str(e)}")

def create_chart(csv_path, title):
    """
    Cria um gráfico de barras baseado nos dados do arquivo CSV.
    
    Args:
        csv_path: Caminho do arquivo CSV com os dados
        title: Título do gráfico
    """
    try:
        df = pd.read_csv(csv_path)
        col_x, col_y = df.columns.values

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x=col_x, y=col_y, palette="viridis", estimator=sum)
        
        plt.title(f'{title.replace("_", " ").title()}', fontsize=14)
        plt.xlabel(col_x.replace("_", " ").title(), fontsize=12)
        plt.ylabel(col_y.replace("_", " ").title(), fontsize=12)

        if 'TOTAL' in col_y:
            def currency_formatter(x, pos):
                return f'R$ {x:,.2f}'
            plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))

        plt.tight_layout()
        
        img_path = csv_path.replace('.csv', '.png').replace('files', 'charts')
        plt.savefig(img_path)
        plt.close()

        return img_path
    except Exception as e:
        raise RuntimeError(f"Erro ao criar gráfico: {str(e)}")
        
def main():
    """Função principal do programa."""
    create_dir()
    conn, cursor = db_connection()      
    try:

        query_sales = """
                SELECT 
                    EXTRACT(MONTH FROM ORDER_DATE) AS MES,
                    COUNT(*) AS QTD
                FROM SALES
                WHERE ORDER_DATE IS NOT NULL
                GROUP BY EXTRACT(MONTH FROM ORDER_DATE)
                ORDER BY QTD DESC
            """
            
        query_employees = """
                SELECT 
                    COALESCE(E.FIRST_NAME, 'Sem Vendedor') AS NOME_VENDEDOR,
                    SUM(S.TOTAL_VALUE) AS TOTAL
                FROM SALES S
                LEFT JOIN EMPLOYEE E ON E.EMP_NO = S.SALES_REP
                WHERE S.TOTAL_VALUE IS NOT NULL
                GROUP BY E.FIRST_NAME
                ORDER BY TOTAL DESC
            """

        results_sales = execute_query(cursor, query_sales)
        sales_file = 'backend/files/vendas_por_mes.csv'
        save_to_csv(sales_file, results_sales, ['MES', 'QTD'])
        create_chart(sales_file, 'Vendas Por Mês')
        print(f"Arquivo CSV e gráfico de vendas por mês gerados com sucesso.")
            
        results_employees = execute_query(cursor, query_employees)
        employees_file = 'backend/files/total_por_vendedor.csv'
        save_to_csv(employees_file, results_employees, ['NOME_VENDEDOR', 'TOTAL'])
        create_chart(employees_file, 'Total Por Vendedor')
        print(f"Arquivo CSV e gráfico de total por vendedor gerados com sucesso.")
            
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()