import fdb
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Configurações de conexão com o Firebird
CONFIG = {
    'host': 'localhost',
    'database': os.path.abspath(os.path.join(os.path.dirname(__file__), 'employee.fdb')),
    'user': 'sysdba',
    'password': 'masterkey'
}

def conectar_banco():
    """Estabelece conexão com o banco de dados Firebird"""
    try:
        return fdb.connect(**CONFIG)
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

def consultar_vendas_por_mes(mes_ano):
    """
    Consulta vendas por mês/ano
    Retorna um DataFrame com os resultados
    """
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Extrai mês e ano do formato YYYY-MM
        ano, mes = mes_ano.split('-')
        
        # Consulta SQL para vendas por vendedor no mês/ano especificado
        query = """
        SELECT 
            e.FIRST_NAME || ' ' || e.LAST_NAME as vendedor,
            SUM(s.TOTAL_VALUE) as total
        FROM SALES s
        JOIN EMPLOYEE e ON s.SALES_REP = e.EMP_NO
        WHERE EXTRACT(YEAR FROM s.ORDER_DATE) = ? 
        AND EXTRACT(MONTH FROM s.ORDER_DATE) = ?
        GROUP BY e.FIRST_NAME, e.LAST_NAME
        ORDER BY total DESC
        """
        
        cursor.execute(query, (ano, mes))
        resultados = cursor.fetchall()
        print(f"Resultados brutos da consulta para {mes_ano}: {resultados}")
        
        # Cria DataFrame com os resultados
        df = pd.DataFrame(resultados, columns=['vendedor', 'total'])
        df['total'] = df['total'].fillna(0)
        
        return df
        
    except Exception as e:
        print(f"Erro na consulta: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def consultar_total_por_vendedor():
    """
    Consulta o total de vendas por vendedor
    Retorna um DataFrame com os resultados
    """
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Consulta SQL para total de vendas por vendedor
        query = """
        SELECT 
            e.FIRST_NAME || ' ' || e.LAST_NAME as vendedor,
            SUM(s.TOTAL_VALUE) as total
        FROM SALES s
        JOIN EMPLOYEE e ON s.SALES_REP = e.EMP_NO
        GROUP BY e.FIRST_NAME, e.LAST_NAME
        ORDER BY total DESC
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        print(f"Resultados brutos da consulta total por vendedor: {resultados}")
        
        # Cria DataFrame com os resultados
        df = pd.DataFrame(resultados, columns=['vendedor', 'total'])
        df['total'] = df['total'].fillna(0)
        
        return df
        
    except Exception as e:
        print(f"Erro na consulta: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def gerar_grafico(df, mes_ano):
    """Gera gráfico de barras com os dados de vendas"""
    print(f"Gerando gráfico para {mes_ano} com {len(df)} linhas")
    if df.empty:
        print("DataFrame vazio, não será gerado gráfico.")
        return
    plt.figure(figsize=(10, 6))
    plt.bar(df['vendedor'], df['total'])
    plt.title(f'Vendas por Vendedor - {mes_ano}')
    plt.xlabel('Vendedor')
    plt.ylabel('Total de Vendas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Caminho absoluto para a pasta de imagens
    imagens_dir = os.path.join(os.path.dirname(__file__), 'imagens')
    if not os.path.exists(imagens_dir):
        os.makedirs(imagens_dir)
    caminho_arquivo = os.path.join(imagens_dir, f'vendas_{mes_ano}.png')
    plt.savefig(caminho_arquivo)
    plt.close()
    print(f"Gráfico salvo em {caminho_arquivo}")

def main():
    """Função principal que executa as consultas e gera os relatórios"""
    try:
        # Obtém o mês/ano atual
        mes_ano_atual = datetime.now().strftime('%Y-%m')
        
        # Consulta vendas por mês
        df_vendas = consultar_vendas_por_mes(mes_ano_atual)
        
        # Consulta total por vendedor
        df_total = consultar_total_por_vendedor()
        
        # Salva resultados em CSV
        if not os.path.exists('relatorios'):
            os.makedirs('relatorios')
        df_vendas.to_csv(f'relatorios/vendas_{mes_ano_atual}.csv', index=False)
        df_total.to_csv(f'relatorios/total_por_vendedor.csv', index=False)
        
        # Gera gráfico
        gerar_grafico(df_vendas, mes_ano_atual)
        
        print(f"Relatórios gerados com sucesso para {mes_ano_atual}")
        
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == '__main__':
    main() 