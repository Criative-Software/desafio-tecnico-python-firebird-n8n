"""
Interface Streamlit para consulta e exportação de vendas por mês.
"""

import streamlit as st
import pandas as pd
import fdb
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

class VendasInterface:
    def __init__(self):
        """Inicializa a interface de vendas."""
        load_dotenv()
        self.conn_params = {
            'dsn': os.getenv("DATABASE_URL"),
            'user': os.getenv("USER"),
            'password': os.getenv("SECRET_KEY"),
            'charset': 'UTF8'
        }
        self.connection = None
        self.configurar_pagina()
        
    def configurar_pagina(self):
        """Configura as propriedades básicas da página Streamlit."""
        st.set_page_config(
            page_title="Sistema de Vendas",
            page_icon="📊",
            layout="wide"
        )
        st.title("📊 Sistema de Consulta de Vendas")
        st.markdown("---")

    def conectar(self) -> bool:
        """
        Estabelece conexão com o banco de dados.
        
        Returns:
            bool: True se a conexão foi bem sucedida, False caso contrário
        """
        try:
            self.connection = fdb.connect(**self.conn_params)
            return True
        except fdb.Error as erro:
            st.error(f"Erro ao conectar ao banco de dados: {erro}")
            return False

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()

    def consultar_vendas_por_mes(self) -> Optional[pd.DataFrame]:
        """
        Consulta as vendas agrupadas por mês.
        
        Returns:
            Optional[pd.DataFrame]: DataFrame com os dados ou None em caso de erro
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
            
            return pd.read_sql(sql_query, self.connection)
            
        except Exception as erro:
            st.error(f"Erro ao consultar vendas por mês: {erro}")
            return None

    def gerar_grafico_vendas(self, df: pd.DataFrame) -> str:
        """
        Gera um gráfico de barras para as vendas e salva como PNG.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            
        Returns:
            str: Nome do arquivo gerado
        """
        try:
            plt.figure(figsize=(12, 6))
            plt.bar(df['MES'], df['TOTAL_VENDAS'])
            plt.title('Vendas por Mês')
            plt.xlabel('Mês')
            plt.ylabel('Total de Vendas')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Gera nome do arquivo com timestamp
            data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"grafico_vendas_por_mes_{data_hora}.png"
            
            plt.savefig(nome_arquivo)
            plt.close()
            return nome_arquivo
            
        except Exception as erro:
            st.error(f"Erro ao gerar gráfico: {erro}")
            return None

    def processar_dados(self, df_vendas: pd.DataFrame) -> tuple:
        """
        Processa os dados do DataFrame para extrair anos e meses únicos.
        
        Args:
            df_vendas (pd.DataFrame): DataFrame com os dados de vendas
            
        Returns:
            tuple: (DataFrame processado, lista de anos, lista de meses)
        """
        df_processado = df_vendas.copy()
        df_processado['ANO'] = df_processado['MES'].str[:4]
        df_processado['MES_NUM'] = df_processado['MES'].str[5:7]
        
        anos = sorted(df_processado['ANO'].unique(), reverse=True)
        meses = sorted(df_processado['MES_NUM'].unique())
        
        return df_processado, anos, meses

    def criar_filtros(self, anos: list, meses: list) -> tuple:
        """
        Cria os filtros na sidebar.
        
        Args:
            anos (list): Lista de anos disponíveis
            meses (list): Lista de meses disponíveis
            
        Returns:
            tuple: (ano selecionado, mês selecionado)
        """
        st.sidebar.header("Filtros")
        
        ano_selecionado = st.sidebar.selectbox(
            "Selecione o Ano",
            anos,
            index=0
        )
        
        mes_selecionado = st.sidebar.selectbox(
            "Selecione o Mês",
            meses,
            index=0
        )
        
        return ano_selecionado, mes_selecionado

    def filtrar_dados(self, df: pd.DataFrame, ano: str, mes: str) -> pd.DataFrame:
        """
        Filtra os dados pelo ano e mês selecionados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            ano (str): Ano selecionado
            mes (str): Mês selecionado
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        return df[
            (df['ANO'] == ano) &
            (df['MES_NUM'] == mes)
        ]

    def formatar_dados_exibicao(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formata os dados para exibição na tabela.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            
        Returns:
            pd.DataFrame: DataFrame formatado
        """
        df_exibicao = df.copy()
        df_exibicao['TOTAL_VENDAS'] = df_exibicao['TOTAL_VENDAS'].map('R$ {:,.2f}'.format)
        df_exibicao['TOTAL_PEDIDOS'] = df_exibicao['TOTAL_PEDIDOS'].map('{:,.0f}'.format)
        df_exibicao['TOTAL_ITENS'] = df_exibicao['TOTAL_ITENS'].map('{:,.0f}'.format)
        
        return df_exibicao.drop(['ANO', 'MES_NUM'], axis=1)

    def exportar_excel(self, df: pd.DataFrame, mes: str, ano: str):
        """
        Exporta os dados para Excel e fornece botão de download.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            mes (str): Mês selecionado
            ano (str): Ano selecionado
        """
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"vendas_{mes}_{ano}_{data_hora}.xlsx"
        
        df.to_excel(nome_arquivo, index=False)
        
        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="⬇️ Baixar arquivo Excel",
                data=file,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    def exibir_metricas(self, df: pd.DataFrame):
        """
        Exibe as métricas principais.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total de Vendas",
                f"R$ {df['TOTAL_VENDAS'].sum():,.2f}"
            )
        
        with col2:
            st.metric(
                "Total de Pedidos",
                f"{df['TOTAL_PEDIDOS'].sum():,.0f}"
            )
        
        with col3:
            st.metric(
                "Total de Itens",
                f"{df['TOTAL_ITENS'].sum():,.0f}"
            )

    def executar(self):
        """Executa a interface principal."""
        if self.conectar():
            try:
                df_vendas = self.consultar_vendas_por_mes()
                
                if df_vendas is not None:
                    # Processa os dados
                    df_processado, anos, meses = self.processar_dados(df_vendas)
                    
                    # Cria filtros
                    ano_selecionado, mes_selecionado = self.criar_filtros(anos, meses)
                    
                    # Filtra os dados
                    df_filtrado = self.filtrar_dados(df_processado, ano_selecionado, mes_selecionado)
                    
                    # Exibe os dados
                    st.subheader(f"Vendas para {mes_selecionado}/{ano_selecionado}")
                    
                    # Formata e exibe a tabela
                    df_exibicao = self.formatar_dados_exibicao(df_filtrado)
                    st.dataframe(
                        df_exibicao,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Botão de exportação
                    if st.button("📥 Exportar para Excel"):
                        self.exportar_excel(df_filtrado, mes_selecionado, ano_selecionado)
                    
                    # Exibe métricas
                    self.exibir_metricas(df_filtrado)
                    
                    # Gera e exibe o gráfico
                    st.subheader("Gráfico de Vendas")
                    nome_arquivo = self.gerar_grafico_vendas(df_filtrado)
                    if nome_arquivo:
                        st.image(nome_arquivo)
                    
                else:
                    st.error("Não foi possível obter os dados do banco de dados.")
                    
            finally:
                self.fechar_conexao()
        else:
            st.error("Não foi possível conectar ao banco de dados.")


def main():
    """Função principal que inicializa e executa a interface."""
    interface = VendasInterface()
    interface.executar()


if __name__ == "__main__":
    main() 