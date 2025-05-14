import streamlit as st
import pandas as pd
import fdb
from datetime import datetime
import os
from PIL import Image 
import pathlib

# Configuração da página (deve ser a primeira instrução Streamlit)
st.set_page_config(
    page_title="Sistema de Consulta de Vendas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistema de Consulta de Vendas")
st.markdown("---")

def get_connection():
    """
    Abre uma nova conexão com o Firebird.
    Tenta encontrar o arquivo de banco de dados em diferentes locais.
    """
    try:
        db_locations = [
            r'C:\Users\Lucas\Documents\Equipar\desafio-tecnico-python-firebird-n8n\n8n\backend\EMPLOYEE.FDB',
            os.path.join(os.getcwd(), 'backend', 'EMPLOYEE.FDB'),
            os.path.join(os.path.dirname(os.getcwd()), 'backend', 'EMPLOYEE.FDB')
        ]
        
        for db_path in db_locations:
            if os.path.exists(db_path):
                return fdb.connect(
                    host='localhost',
                    database=db_path,
                    user='SYSDBA',
                    password='masterkey',
                    charset='UTF8'
                )
        
        return fdb.connect(
            host='localhost',
            database=r'C:\Users\Lucas\Documents\Equipar\desafio-tecnico-python-firebird-n8n\n8n\backend\EMPLOYEE.FDB',
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        st.stop()

@st.cache_data
def get_available_years():
    """Retorna os anos disponíveis na tabela CSV_IMPORT."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT ANO FROM CSV_IMPORT ORDER BY ANO DESC")
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        st.error(f"Erro ao buscar anos disponíveis: {str(e)}")
        return []

@st.cache_data
def get_available_months(year: int):
    """Retorna os meses disponíveis para um dado ano."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT DISTINCT MES FROM CSV_IMPORT WHERE ANO = ? ORDER BY MES",
                (year,)
            )
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        st.error(f"Erro ao buscar meses disponíveis: {str(e)}")
        return []

def fetch_sales_data(year: int, month: int) -> pd.DataFrame:
    """Busca registros de vendas para o ano e mês selecionados."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT ID, ANO, MES, TOTAL_VENDAS, DATA_IMPORTACAO
                  FROM CSV_IMPORT
                 WHERE ANO = ? AND MES = ?
                 ORDER BY ID
                """,
                (year, month)
            )
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=cols)
        if not df.empty:
            
            df['DATA_IMPORTACAO'] = pd.to_datetime(df['DATA_IMPORTACAO'])\
                .dt.strftime('%d/%m/%Y %H:%M:%S')
            
            df['TOTAL_VENDAS'] = df['TOTAL_VENDAS']\
                .apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados de vendas: {str(e)}")
        return pd.DataFrame()

def parse_currency(s: str) -> float:
    """
    Converte string de moeda para float:
    - 'R$ 3.000,50' → 3000.50
    - 'R$ 3000.50'  → 3000.50
    """
    try:
        s = s.replace('R$', '').strip()
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        return float(s)
    except:
        return 0.0

def export_to_excel(df: pd.DataFrame, year: int, month: int):
    """Gera arquivo .xlsx e retorna (bytes, nome_arquivo)."""
    if df.empty:
        st.warning("Não há dados para exportar.")
        return None, None

    try:
        export_df = df.copy()
        export_df['TOTAL_VENDAS'] = export_df['TOTAL_VENDAS'].apply(parse_currency)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vendas_{year}_{month:02d}_{ts}.xlsx"
        export_df.to_excel(filename, index=False, engine='openpyxl')

        with open(filename, 'rb') as f:
            data = f.read()
        os.remove(filename)
        return data, filename
    except Exception as e:
        st.error(f"Erro ao exportar para Excel: {str(e)}")
        return None, None

# --- Interface ---


st.sidebar.header("Sistema de Consulta")


try:
    current_dir = pathlib.Path(__file__).parent.absolute()
    logo_path = current_dir / "assets" / "images.jpeg"
    
    if logo_path.exists():
        logo = Image.open(logo_path)
        st.sidebar.image(logo, width=200)
    else:
        alt_path = pathlib.Path("frontend") / "assets" / "images.jpeg"
        if alt_path.exists():
            logo = Image.open(alt_path)
            st.sidebar.image(logo, width=200)
        else:
            st.sidebar.warning("Logo não encontrada. Verifique o diretório de assets.")
except Exception as e:
    st.sidebar.warning(f"Não foi possível carregar a logo: {str(e)}")

st.sidebar.header("Filtros")

years = get_available_years()
if not years:
    st.warning("Nenhum registro encontrado no banco.")
    st.stop()

selected_year = st.sidebar.selectbox("Ano", years)

months = get_available_months(selected_year)
if not months:
    st.sidebar.warning(f"Sem dados para o ano {selected_year}.")
    st.stop()

month_names = {
    1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril",
    5:"Maio", 6:"Junho", 7:"Julho", 8:"Agosto",
    9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"
}
opts = [f"{m} — {month_names[m]}" for m in months]
sel = st.sidebar.selectbox("Mês", opts)
selected_month = int(sel.split(" — ")[0])

btn = st.sidebar.button("🔍 Buscar")

results = st.container()

if btn:
    with results:
        with st.spinner("Buscando dados..."):
            df = fetch_sales_data(selected_year, selected_month)
            if df.empty:
                st.info(f"Sem vendas para {month_names[selected_month]} de {selected_year}.")
            else:
                st.subheader(f"Vendas de {month_names[selected_month]} de {selected_year}")
                total_records = len(df)
                total_sales = df['TOTAL_VENDAS'].apply(parse_currency).sum()
                c1, c2 = st.columns(2)
                c1.metric("Total de Registros", total_records)
                c2.metric("Total de Vendas", f"R$ {total_sales:,.2f}".replace(',', 'X').replace('.', ',').replace('X','.'))

                excel_data, fname = export_to_excel(df, selected_year, selected_month)
                if excel_data:
                    st.download_button(
                        label="📥 Exportar para Excel",
                        data=excel_data,
                        file_name=fname,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )

st.markdown("---")
st.caption("Desenvolvido para o desafio técnico Python + Firebird + n8n")