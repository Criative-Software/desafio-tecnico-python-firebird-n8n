# Sistema de Consulta de Vendas

![Sistema de Consulta de Vendas](frontend/assets/images.jpeg)

## Sobre o Projeto

Sistema de Consulta de Vendas é uma aplicação web desenvolvida com Streamlit para visualizar e analisar dados de vendas armazenados em um banco de dados Firebird. Este projeto foi desenvolvido como parte de um desafio técnico que combina Python, Firebird e n8n.

## Funcionalidades

- ✅ Visualização de vendas por ano e mês
- 📊 Exibição de métricas como total de registros e valor total de vendas
- 📥 Exportação de dados para Excel
- 🔍 Filtragem dinâmica por período

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal
- **Streamlit**: Framework para criação de aplicações web
- **Firebird**: Sistema de gerenciamento de banco de dados relacional
- **FDB**: Biblioteca Python para conexão com Firebird
- **Pandas**: Biblioteca para manipulação e análise de dados
- **Pillow (PIL)**: Biblioteca para processamento de imagens
- **n8n**: Plataforma de automação de fluxo de trabalho

## Requisitos

Para executar este projeto, você precisa ter instalado:

- Python 3.7 ou superior
- Firebird SQL Server
- Pacotes Python listados em `requirements.txt`

## Instalação

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd [NOME_DO_DIRETÓRIO]
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados Firebird:
   - Certifique-se de que o servidor Firebird está em execução
   - Verifique se o arquivo de banco de dados `EMPLOYEE.FDB` está localizado no diretório correto
   - Ajuste os parâmetros de conexão em `get_connection()` se necessário

4. Prepare os arquivos de assets:
   - Certifique-se de que o diretório `frontend/assets` contém o arquivo `images.jpeg` para o logo

## Uso

1. Execute a aplicação Streamlit:
   ```bash
   streamlit run app.py
   ```

2. No navegador, acesse:
   ```
   http://localhost:8501
   ```

3. Use a interface para:
   - Selecionar o ano e mês desejados
   - Visualizar os dados de vendas correspondentes
   - Exportar os dados para Excel se necessário

## Modelo de Dados

A aplicação trabalha com a tabela `CSV_IMPORT` do banco de dados, que possui a seguinte estrutura:

| Campo           | Tipo    | Descrição                         |
|-----------------|---------|-----------------------------------|
| ID              | Integer | Identificador único do registro   |
| ANO             | Integer | Ano da venda                      |
| MES             | Integer | Mês da venda                      |
| TOTAL_VENDAS    | Numeric | Valor total das vendas no período |
| DATA_IMPORTACAO | Date    | Data e hora da importação         |

## Troubleshooting

- **Problema de conexão com o banco**: Verifique se o servidor Firebird está em execução e se o caminho para o arquivo `.FDB` está correto.
- **Logo não aparece**: Verifique se o arquivo de imagem está no diretório correto (`frontend/assets/images.jpeg`).
- **Erro ao exportar para Excel**: Certifique-se de que a biblioteca `openpyxl` está instalada corretamente.