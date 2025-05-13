import fdb
import pandas as pd
import matplotlib.pyplot as plt

# 🔌 Conectar ao banco Firebird
con = fdb.connect(
    dsn='localhost:C:/Projects/Database/FIREBIRD.fdb',
    user='SYSDBA',
    password='masterkey'
)
cur = con.cursor()

# 📌 **Configurar API da IA**
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        api_configured = True
    else:
        st.error("Erro: Chave 'GOOGLE_API_KEY' não encontrada nos secrets do Streamlit.")
        api_configured = False
except Exception as e:
    st.error(f"Erro inesperado na configuração da API: {e}")
    api_configured = False

# 📌 Criar tabela `csv_import` caso ainda não exista
# Descomente esse trecho caso não tenha a tabela
# cur.execute("""
# CREATE TABLE csv_import (
#     ano INTEGER,
#     mes INTEGER,
#     total DECIMAL(15,2)
# );
# """)
# con.commit()

# 1️⃣ **Consulta: Vendas por Mês**
# Esta consulta extrai o ano e mês das vendas e soma o valor total para cada período
sql_vendas_mes = """
SELECT
    EXTRACT(YEAR FROM ORDER_DATE) AS "ano",
    EXTRACT(MONTH FROM ORDER_DATE) AS "mes",
    SUM(TOTAL_VALUE) AS "total"
FROM SALES
GROUP BY
    EXTRACT(YEAR FROM ORDER_DATE),
    EXTRACT(MONTH FROM ORDER_DATE)
ORDER BY
    EXTRACT(YEAR FROM ORDER_DATE),
    EXTRACT(MONTH FROM ORDER_DATE)
"""

# 2️⃣ **Consulta: Total por Vendedor**
# Obtém o nome dos vendedores e soma o total de vendas que cada um realizou
sql_total_vendedor = """
SELECT
    e.FULL_NAME,
    SUM(s.TOTAL_VALUE) AS total
FROM EMPLOYEE e
INNER JOIN SALES s ON s.SALES_REP = e.EMP_NO
GROUP BY e.FULL_NAME
ORDER BY total DESC
"""

# 📊 **Executar consultas e armazenar resultados em DataFrames**
df_vendas_mes = pd.read_sql(sql_vendas_mes, con)
df_total_vendedor = pd.read_sql(sql_total_vendedor, con)

# 📥 **Salvar resultados em CSV**
df_vendas_mes.to_csv('vendas_mes.csv', index=False)
df_total_vendedor.to_csv('total_por_vendedor.csv', index=False)

# 🔄 **Inserir os dados do CSV no banco Firebird**
for _, row in df_vendas_mes.iterrows():
    ano = int(row["ano"])  # Converte para inteiro
    mes = int(row["mes"])  # Converte para inteiro
    total = float(row["total"])  # Converte para número decimal
    
    cur.execute("INSERT INTO csv_import (ano, mes, total) VALUES (?, ?, ?)", (ano, mes, total))

con.commit()
print("✅ Dados do CSV inseridos no Firebird com sucesso!")

# 📈 **Gerar gráfico de vendas por mês**
df_vendas_mes['ano_mes'] = df_vendas_mes['ano'].astype(str) + '-' + df_vendas_mes['mes'].astype(str).str.zfill(2)

# 🎨 **Criar gráfico e salvar como imagem**
plt.figure(figsize=(10, 6))
plt.bar(df_vendas_mes['ano_mes'], df_vendas_mes['total'], color='green')
plt.title('Vendas por Mês')
plt.xlabel('Ano-Mês')
plt.ylabel('Total Vendido')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico.png')
plt.close()

print("📊 CSV e gráfico gerados com sucesso!")

# 🧠 **Gerar insights de negócios usando IA**
if st.button("Gerar Insights de Negócios por IA"):
    if api_configured and not df_vendas_mes.empty and not df_total_vendedor.empty and con is not None:
        
        insights_data = {
            "Vendas por Mês (Dados)": df_vendas_mes.to_markdown(),
            "Total por Vendedor (Dados)": df_total_vendedor.to_markdown(),
        }

        prompt = """
        Analise os dados de vendas de uma empresa abaixo.
        Forneça insights de negócios em formato de bullet points fáceis de entender.
        Identifique tendências nas vendas mensais e nos desempenhos individuais dos vendedores.
        Sugira possíveis áreas de melhoria para aumentar a receita ou otimizar a equipe de vendas.
        Organize tudo tópicos, indicando métricas de sucesso com base no passar dos anos.

        Dados para Análise:
        """
        for key, value in insights_data.items():
            prompt += f"\n\n## {key}:\n{value}"
        prompt += """

        Com base nesses dados, quais são os principais insights e recomendações de negócios?
        """

        try:
            model_name_to_try = 'models/gemini-2.0-flash'
            model = genai.GenerativeModel(model_name_to_try)

            with st.spinner(f"A IA ({model_name_to_try}) está analisando os dados e gerando insights..."):
                response = model.generate_content(prompt)

            st.subheader("Insights Gerados pela IA:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Erro ao chamar a API da IA: {e}")
            st.warning(f"Pode ser que o modelo '{model_name_to_try}' não esteja disponível para sua chave ou região.")
            st.info("Se o erro persistir, tente alterar o nome do modelo na linha `model_name_to_try`.")

    else:
        st.warning("Não é possível gerar insights: Verifique se a API está configurada corretamente e se os dados estão carregados.")

# 📌 **Fechar conexão com o banco**
con.close()
