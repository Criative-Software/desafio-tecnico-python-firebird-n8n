# IMPOTAÇÕES DE BIBLIOTECAS
from typing import List, Tuple, Dict, Any
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import fdb
import os
import sys
import json

# CONFIGURAÇÕES DO BANCO DE DADOS
DB_CONFIG = {
    'host': 'localhost/3050',
    'database': 'C:\\Users\\Lucas\\Documents\\Equipar\\desafio-tecnico-python-firebird-n8n\\backend\\EMPLOYEE.FDB',
    'user': 'sysdba',
    'password': 'masterkey',
    'charset': 'UTF8'
}

# TRATAMENTO DE EXCEÇÕES
class DatabaseConnectionError(Exception):
    pass

class DatabaseManager:
    @staticmethod
    def get_connection() -> fdb.Connection:
        try:
            dsn = f"{DB_CONFIG['host']}:{DB_CONFIG['database']}"
            return fdb.connect(
                dsn=dsn,
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                charset=DB_CONFIG['charset']
            )
        except fdb.Error as e:
            raise DatabaseConnectionError(f"Erro na conexão com o banco: {e}") from e

# CONSULTAS SQL
def execute_query(query: str, params: Tuple = None) -> List[Dict[str, Any]]:
    try:
        with DatabaseManager.get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(query, params or ())
                cols = [d[0].lower() for d in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
            finally:
                cur.close()
    except fdb.Error as e:
        raise DatabaseConnectionError(f"Erro na execução da query: {e}") from e

def get_vendas_por_mes() -> List[Dict[str, Any]]:
    q = """
        SELECT
            EXTRACT(YEAR FROM ORDER_DATE) AS ano,
            EXTRACT(MONTH FROM ORDER_DATE) AS mes,
            SUM(TOTAL_VALUE) AS total_vendas
        FROM SALES
        GROUP BY EXTRACT(YEAR FROM ORDER_DATE), EXTRACT(MONTH FROM ORDER_DATE)
        ORDER BY ano, mes
    """
    return execute_query(q)

def get_total_por_vendedor() -> List[Dict[str, Any]]:
    q = """
        SELECT
            E.FIRST_NAME || ' ' || E.LAST_NAME AS vendedor,
            SUM(S.TOTAL_VALUE) AS total_vendas
        FROM SALES S
        JOIN EMPLOYEE E ON S.SALES_REP = E.EMP_NO
        GROUP BY E.FIRST_NAME, E.LAST_NAME
        ORDER BY total_vendas DESC
    """
    return execute_query(q)

# FUNÇOES AUXILIARES
def formatar_mes(mes: int) -> str:
    return datetime(1900, mes, 1).strftime('%b')

def parse_valor_brasileiro(valor_str: str) -> float:
    s = str(valor_str).strip()
    if '.' in s and ',' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    return float(s)

def formatar_moeda(valor) -> str:
    try:
        f = float(valor)
        return f"R$ {f:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"

def mostrar_resultados(resultados: List[Dict[str, Any]], titulo: str):
    if not resultados:
        print(f"\n{titulo}: Nenhum dado disponível.")
        return

    primeiro = resultados[0]
    if 'mes' in primeiro and 'ano' in primeiro:
        ords = sorted(resultados, key=lambda x: (x['ano'], x['mes']))
        cab = ['Período', 'Total Vendas']
        linhas = [
            [
                f"{formatar_mes(item['mes'])}/{item['ano']}",
                item['total_vendas'] if isinstance(item['total_vendas'], str)
                    else formatar_moeda(item['total_vendas'])
            ] for item in ords
        ]
    else:
        ords = sorted(resultados, key=lambda x: x['total_vendas'], reverse=True)
        cab = ['Vendedor', 'Total Vendas']
        linhas = [
            [
                item['vendedor'],
                item['total_vendas'] if isinstance(item['total_vendas'], str)
                    else formatar_moeda(item['total_vendas'])
            ] for item in ords
        ]

    largura1 = max(len(cab[0]), max(len(l[0]) for l in linhas))
    largura2 = max(len(cab[1]), max(len(l[1]) for l in linhas))
    sep = "-" * (largura1 + largura2 + 3)

    print(f"\n{titulo}:")
    print(sep)
    print(f"{cab[0]:<{largura1}}  {cab[1]:>{largura2}}")
    print(sep)
    for l in linhas:
        print(f"{l[0]:<{largura1}}  {l[1]:>{largura2}}")
    print(sep)

# GERAÇÃO E SALVAMENTO DE GRÁFICOS
def salvar_grafico(fig, caminho: str):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    fig.savefig(caminho, dpi=300)
    print(f"Resultados salvos em: {caminho}")
    plt.close(fig)

def plot_total_por_vendedor(vendas: List[Dict[str, Any]]):
    df = pd.DataFrame(vendas)

    fig, ax = plt.subplots(figsize=(14, 8), constrained_layout=True)
    sns.barplot(x='vendedor', y='total_vendas', data=df, color='seagreen', ax=ax)
    ax.set_title("Total de Vendas por Vendedor", fontsize=16, fontweight='bold')
    ax.set_xlabel("Vendedor", fontsize=12)
    ax.set_ylabel("Total (R$)", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('R$ {x:,.0f}'))

    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                f"R$ {h:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                (p.get_x() + p.get_width() / 2, h),
                ha='center', va='bottom', fontsize=9
            )

    salvar_grafico(fig, "graficos/total de vendas por vendedor.png")

def plot_vendas_por_mes(vendas_mes: List[Dict[str, Any]]):
    df = pd.DataFrame(vendas_mes)
    df['mes_nome'] = df['mes'].apply(formatar_mes)
    df['periodo'] = df['mes_nome'] + '/' + df['ano'].astype(str)

    fig, ax = plt.subplots(figsize=(14, 8), constrained_layout=True)
    sns.barplot(x='periodo', y='total_vendas', data=df, color='steelblue', ax=ax)
    ax.set_title("Total de Vendas por Mês", fontsize=16, fontweight='bold')
    ax.set_xlabel("Período", fontsize=12)
    ax.set_ylabel("Total (R$)", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('R$ {x:,.0f}'))

    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                f"R$ {h:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                (p.get_x() + p.get_width() / 2, h),
                ha='center', va='bottom', fontsize=9
            )

    salvar_grafico(fig, "graficos/total de vendas por mês.png")

# GERAÇÃO E SALVAMENTO DE CSV
def salvar_resultados_csv(resultados: List[Dict[str, Any]], nome_arquivo: str, formatar_valores=False):
    if not resultados:
        print(f"Nenhum dado disponível para salvar em {nome_arquivo}.")
        return

    os.makedirs("arquivos_csv", exist_ok=True)
    if formatar_valores:
        for linha in resultados:
            if 'total_vendas' in linha:
                linha['total_vendas'] = formatar_moeda(linha['total_vendas'])

    caminho = os.path.join("arquivos_csv", nome_arquivo)
    pd.DataFrame(resultados).to_csv(caminho, index=False, encoding='utf-8-sig')
    print(f"Resultados salvos em: {caminho}")

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    try:
        vendas_mes = get_vendas_por_mes()
        total_vendedor = get_total_por_vendedor()

        for v in vendas_mes:
            v['ano'] = int(float(v['ano']))
            v['mes'] = int(float(v['mes']))
            v['total_vendas'] = float(str(v['total_vendas']).replace(',', '.'))
        for v in total_vendedor:
            v['total_vendas'] = parse_valor_brasileiro(v['total_vendas'])

        if "--json" in sys.argv:
            print(json.dumps({
                "vendas_por_mes": vendas_mes,
                "vendas_por_vendedor": total_vendedor
            }, ensure_ascii=False))
            sys.exit(0)

        # Gera gráficos primeiro (com dados numéricos puros)
        plot_vendas_por_mes(vendas_mes)
        plot_total_por_vendedor(total_vendedor)

        # Depois CSV formatado e saída no terminal
        salvar_resultados_csv(vendas_mes, "vendas_por_mes.csv", formatar_valores=True)
        salvar_resultados_csv(total_vendedor, "total_por_vendedor.csv", formatar_valores=True)
        mostrar_resultados(vendas_mes, "Vendas por Mês")
        mostrar_resultados(total_vendedor, "Total por Vendedor")

    except DatabaseConnectionError as e:
        print(f"Erro crítico: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
