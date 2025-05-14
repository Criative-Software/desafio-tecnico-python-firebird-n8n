import fdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Força uso de backend sem interface gráfica


def conectar():
    return fdb.connect(
        host='localhost',
        database=r'C:\Users\flavi\Workspace\desafio-tecnico-python-firebird-n8n-flaviomartins\employee.fdb',
        user='sysdba',
        password='masterkey'
    )

def vendas_por_mes():
    try:
        conn = conectar()
        query = """
            SELECT
              EXTRACT(MONTH FROM ORDER_DATE) AS MES,
              SUM(TOTAL_VALUE) AS TOTAL_VENDAS
            FROM SALES
            GROUP BY EXTRACT(MONTH FROM ORDER_DATE)
            ORDER BY MES
        """
        df = pd.read_sql(query, conn)
        df.columns = [col.strip().lower() for col in df.columns]  # padroniza nomes
        df.to_csv('vendas_mes.csv', index=False)
        print("✅ CSV de vendas por mês gerado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao consultar vendas por mês: {e}")
        return pd.DataFrame()

def total_por_vendedor():
    try:
        conn = conectar()
        query = """
            SELECT
              E.FULL_NAME AS VENDEDOR,
              SUM(S.TOTAL_VALUE) AS TOTAL_VENDAS
            FROM SALES S
            JOIN EMPLOYEE E ON S.SALES_REP = E.EMP_NO
            GROUP BY E.FULL_NAME
            ORDER BY TOTAL_VENDAS DESC
        """
        df = pd.read_sql(query, conn)
        df.columns = [col.strip().lower() for col in df.columns]  # padroniza nomes
        df.to_csv('total_por_vendedor.csv', index=False)
        print("✅ CSV de total por vendedor gerado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao consultar total por vendedor: {e}")
        return pd.DataFrame()

def gerar_grafico():
    df = vendas_por_mes()
    if df.empty:
        print("Não foi possível gerar o gráfico. DataFrame vazio.")
        return
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(df['mes'], df['total_vendas'], color='skyblue')
        plt.xlabel('Mês')
        plt.ylabel('Total de Vendas')
        plt.title('Vendas por Mês')
        plt.xticks(range(1, 13))
        plt.savefig('grafico.png')
        plt.close()
        print("✅ Gráfico gerado como 'grafico.png'.")
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")

if __name__ == '__main__':
    vendas_por_mes()
    total_por_vendedor()
    gerar_grafico()
