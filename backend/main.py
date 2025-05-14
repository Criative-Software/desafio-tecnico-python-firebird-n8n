"""
Módulo para conexão e consultas ao banco de dados Firebird.
Este módulo fornece uma classe para conectar ao Firebird e realizar consultas no banco de dados:
- vendas_por_mes: obtém os dados das vendas agrupadas por mês
- total_por_vendedor: retorna o total de vendas realizadas por cada vendedor.
Os resultados de cada consulta são exportados para arquivos no formato .csv, permitindo que os dados sejam armazenados e reutilizados facilmente.
Por fim, com base nesses dados, é gerado um gráfico de barras — representando visualmente as informações — e ele é salvo como uma imagem no arquivo grafico.png.
"""

import fdb
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, List, Tuple


class FirebirdDatabase:
    def __init__(self):
        """Inicializa a classe com os parâmetros de conexão."""
        load_dotenv()
        self.conn_params = {
            'dsn': os.getenv("DATABASE_URL"),
            'user': os.getenv("USER"),
            'password': os.getenv("SECRET_KEY"),
            'charset': 'UTF8'
        }
        self.connection = None

    def conectar(self) -> Optional[fdb.Connection]:
        """
        Estabelece conexão com o banco de dados Firebird.

        Returns:
            Optional[fdb.Connection]: Objeto de conexão se bem sucedido, None caso contrário.
        """
        try:
            self.connection = fdb.connect(**self.conn_params)
            print("Conexão estabelecida com sucesso!")
            return self.connection
        except fdb.Error as erro:
            print(f"Erro ao conectar ao banco de dados: {erro}")
            return None

    def fechar_conexao(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            print("Conexão fechada com sucesso!")

    def consultar_vendas_por_mes(self) -> Optional[pd.DataFrame]:
        """
        Consulta as vendas agrupadas por mês.

        Returns:
            Optional[pd.DataFrame]: DataFrame contendo dados das vendas ou None em caso de erro.
        """
        try:
            sql_query = """
                SELECT
                    EXTRACT(YEAR FROM ORDER_DATE) || '-' || 
                    LPAD(EXTRACT(MONTH FROM ORDER_DATE), 2, '0') AS MES,
                    SUM(TOTAL_VALUE) AS TOTAL_VENDAS,
                    COUNT(*) AS TOTAL_PEDIDOS,
                    SUM(QTY_ORDERED) AS TOTAL_ITENS
                FROM
                    SALES
                WHERE
                    ORDER_STATUS = 'shipped'
                GROUP BY
                    EXTRACT(YEAR FROM ORDER_DATE),
                    EXTRACT(MONTH FROM ORDER_DATE)
                ORDER BY
                    EXTRACT(YEAR FROM ORDER_DATE),
                    EXTRACT(MONTH FROM ORDER_DATE);    
            """
            
            df = pd.read_sql(sql_query, self.connection)
            
            # Gerar nome do arquivo CSV com timestamp
            data_hora = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            nome_arquivo = f"vendas_por_mes_{data_hora}.csv"
            
            # Salvar o DataFrame em CSV
            df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8')
            
            print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
            return df
            
        except fdb.Error as erro:
            print(f"Erro ao consultar vendas por mês: {erro}")
            return None

    def consultar_vendas_por_vendedor(self) -> Optional[pd.DataFrame]:
        """
        Consulta as vendas agrupadas por vendedor.

        Returns:
            Optional[pd.DataFrame]: DataFrame contendo dados das vendas por vendedor ou None em caso de erro.
        """
        try:
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
            
            df = pd.read_sql(sql_query, self.connection)
            
            # Gerar nome do arquivo CSV com timestamp
            data_hora = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            nome_arquivo = f"vendas_por_vendedor_{data_hora}.csv"
            
            # Salvar o DataFrame em CSV
            df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8')
            
            print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
            return df
            
        except fdb.Error as erro:
            print(f"Erro ao consultar vendas por vendedor: {erro}")
            return None

    def gerar_grafico_vendas_por_mes(self, df: pd.DataFrame) -> None:
        """
        Gera um gráfico de barras para as vendas por mês e salva como PNG.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados de vendas por mês.
        """
        try:
            plt.figure(figsize=(12, 6))
            plt.bar(df['MES'], df['TOTAL_VENDAS'])
            plt.title('Vendas por Mês')
            plt.xlabel('Mês')
            plt.ylabel('Total de Vendas')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Gerar nome do arquivo com timestamp
            data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"grafico_vendas_por_mes_{data_hora}.png"
            
            plt.savefig(nome_arquivo)
            plt.close()
            print(f"Gráfico salvo como '{nome_arquivo}'")
        except Exception as erro:
            print(f"Erro ao gerar gráfico de vendas por mês: {erro}")

    def gerar_grafico_vendas_por_vendedor(self, df: pd.DataFrame) -> None:
        """
        Gera um gráfico de barras para as vendas por vendedor e salva como PNG.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados de vendas por vendedor.
        """
        try:
            plt.figure(figsize=(12, 6))
            plt.bar(df['COD_VENDEDOR'], df['TOTAL_VENDAS'])
            plt.title('Vendas por Vendedor')
            plt.xlabel('Código do Vendedor')
            plt.ylabel('Total de Vendas')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Gerar nome do arquivo com timestamp
            data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"grafico_vendas_por_vendedor_{data_hora}.png"
            
            plt.savefig(nome_arquivo)
            plt.close()
            print(f"Gráfico salvo como '{nome_arquivo}'")
        except Exception as erro:
            print(f"Erro ao gerar gráfico de vendas por vendedor: {erro}")


def main() -> None:
    """Função principal que executa as operações do módulo."""
    db = FirebirdDatabase()
    
    if db.conectar():
        try:
            # Consultar e gerar gráfico de vendas por mês
            df_vendas_mes = db.consultar_vendas_por_mes()
            if df_vendas_mes is not None:
                db.gerar_grafico_vendas_por_mes(df_vendas_mes)

            # Consultar e gerar gráfico de vendas por vendedor
            df_vendas_vendedor = db.consultar_vendas_por_vendedor()
            if df_vendas_vendedor is not None:
                db.gerar_grafico_vendas_por_vendedor(df_vendas_vendedor)
        finally:
            db.fechar_conexao()


if __name__ == "__main__":
    main()
