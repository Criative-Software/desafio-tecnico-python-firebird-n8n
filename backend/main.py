import fdb
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Conectar ao banco Firebird
    con = fdb.connect(
        host='localhost',
        port=3050,
        database='/firebird/data/employee.fdb',
        user='sysdba',
        password='masterkey'
    )
    print("🔌 Conectado ao banco")

    cur = con.cursor()

    print("📊 Executando consulta: vendas por mês")
    cur.execute("""
        SELECT EXTRACT(MONTH FROM s.ORDER_DATE) AS mes,
               EXTRACT(YEAR FROM s.ORDER_DATE) AS ano,
               SUM(s.TOTAL_VALUE) AS total
        FROM SALES s
        GROUP BY ano, mes
        ORDER BY ano, mes;
    """)
    dados1 = cur.fetchall()
    df1 = pd.DataFrame(dados1, columns=['mes', 'ano', 'total'])
    df1.to_csv('vendas_por_mes.csv', index=False)
    print("📁 vendas_por_mes.csv gerado!")

    print("📊 Executando consulta: total por vendedor")
    cur.execute("""
        SELECT e.FULL_NAME AS nome_vendedor, SUM(s.TOTAL_VALUE) AS total
        FROM SALES s
        JOIN EMPLOYEE e ON s.SALES_REP = e.EMP_NO
        GROUP BY e.FULL_NAME
        ORDER BY total DESC;
    """)
    dados2 = cur.fetchall()
    df2 = pd.DataFrame(dados2, columns=['vendedor', 'total'])
    df2.to_csv('total_por_vendedor.csv', index=False)
    print("📁 total_por_vendedor.csv gerado!")

    print("📈 Gerando gráfico...")
    plt.figure(figsize=(10,6))
    plt.bar(df2['vendedor'], df2['total'])
    plt.xticks(rotation=45)
    plt.title('Total de Vendas por Vendedor')
    plt.tight_layout()
    plt.savefig('grafico.png')
    print("🖼️ grafico.png criado!")

if __name__ == "__main__":
    main()