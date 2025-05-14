# import fdb
# import pandas as pd
# def conectar_firebird():
    
#     try:
#         # Firebird Client no Windows
#         # Necessario instalar em https://firebirdsql.org/en/firebird-3-0/
#         fdb.load_api("C:/Program Files/Firebird/Firebird_3_0/bin/fbclient.dll")
#         # Parâmetros de conexão para Firebird no Docker
#         host = 'localhost'  # Endereço do host onde o Docker está rodando
#         port = '3050'      # Porta padrão do Firebird
#         database = '/firebird/data/employee.fdb'  # Caminho dentro do container
#         user = 'sysdba'    # Usuário padrão do Firebird
#         password = 'masterkey'  # Senha padrão do Firebird
        
#         print(f'{host}:{database}')
#         # Estabelece a conexão
#         conexao = fdb.connect(         
#             dsn=f'{host}:{database}',
#             user=user,
#             password=password
#         )
        
#         print("Conexão estabelecida com sucesso!")
#         return conexao
        
#     except fdb.Error as erro:
#         print(f"Erro ao conectar ao banco de dados: {erro}")
#         return None

# def fechar_conexao(conexao):
#     if conexao:
#         conexao.close()
#         print("Conexão fechada com sucesso!")

# if __name__ == "__main__":
#     # Testa a conexão    
#     conexao = conectar_firebird()
#     if conexao:
#         # Aqui você pode executar suas consultas SQL
#         cursor = conexao.cursor()
        
#         print("######################################################")
#         print("################# VENDAS POR MES #################")
#         print("######################################################")
                
#         # consulta de vendas_por_mes
#         cursor.execute("""
#                         SELECT
#                             EXTRACT(YEAR FROM ORDER_DATE) || '-' || 
#                             LPAD(EXTRACT(MONTH FROM ORDER_DATE), 2, '0') AS MES,
#                             SUM(TOTAL_VALUE) AS TOTAL_VENDAS,
#                             COUNT(*) AS TOTAL_PEDIDOS,
#                             SUM(QTY_ORDERED) AS TOTAL_ITENS
#                         FROM
#                             SALES
#                         WHERE
#                             ORDER_STATUS = 'shipped'
#                         GROUP BY
#                             EXTRACT(YEAR FROM ORDER_DATE),
#                             EXTRACT(MONTH FROM ORDER_DATE)
#                         ORDER BY
#                             EXTRACT(YEAR FROM ORDER_DATE),
#                             EXTRACT(MONTH FROM ORDER_DATE);                  
#                        """)
#         vendas_por_mes = cursor.fetchall()
#         for linha in vendas_por_mes:
#             print(linha)
        
#         print("######################################################")
#         print("################# TOTAL POR VENDEDOR #################")
#         print("######################################################")
#         # consulta de total_por_vendedor
#         cursor.execute("""
#                 SELECT 
#                     SALES_REP AS COD_VENDEDOR,
#                     SUM(TOTAL_VALUE) AS TOTAL_VENDAS
#                 FROM 
#                 SALES
#                 WHERE 
#                     ORDER_STATUS = 'shipped'  
#                 GROUP BY 
#                     SALES_REP
#                 ORDER BY 
#                     TOTAL_VENDAS DESC;                                        
#                        """)
#         total_por_vendedor = cursor.fetchall()
#         for linha in total_por_vendedor:
#             print(linha)
              
#         df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8')

#         print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")                    
#         cursor.close()
#         fechar_conexao(conexao)

import fdb
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# Configurações de conexão com o banco de dados Firebird
conn_params = {
    'dsn': os.getenv("DATABASE_URL"),
    'user': os.getenv("USER"),
    'password': os.getenv("SECRET_KEY"),
    'charset': 'UTF8'
}

# Consulta SQL (usando a primeira versão do exemplo anterior)
sql_query = """
SELECT 
    SALES_REP AS COD_VENDEDOR,
    SUM(TOTAL_VALUE) AS TOTAL_VENDAS
FROM 
SALES
WHERE 
    ORDER_STATUS = 'shipped'  
GROUP BY 
    SALES_REP
ORDER BY 
    TOTAL_VENDAS DESC;   
"""

# Executar a consulta e carregar os dados diretamente em um DataFrame
try:
    # Estabelecer conexão e ler os dados para o DataFrame
    with fdb.connect(**conn_params) as conn:
        df = pd.read_sql(sql_query, conn)
    
    # Gerar nome do arquivo CSV com timestamp
    data_hora = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    nome_arquivo = f"vendas_por_vendedor_{data_hora}.csv"
    
    # Salvar o DataFrame em CSV
    df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8')
    
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
    print(f"\nResumo dos dados:\n{df.describe()}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")