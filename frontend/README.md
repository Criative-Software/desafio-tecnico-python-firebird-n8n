# Consulta de Vendas – Desafio Técnico

Interface web simples desenvolvida com Flask para consultar e exportar dados da tabela `csv_import` do banco Firebird.

## Funcionalidades

- Seleção de **mês** e **ano** por dropdown
- Filtro de dados diretamente da tabela `csv_import`
- Exibição em tabela responsiva
- Exportação dos dados filtrados em **.xlsx**
- Suporte a tema claro/escuro com alternância manual

## Requisitos

- Python 3.10+
- Firebird 2.5
- Dependências Python:
  - flask
  - pandas
  - fdb
  - openpyxl

## Como executar

1. Clone o repositório e entre no diretório `frontend`
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows


Instale as dependências:
pip install flask pandas fdb openpyxl

Execute o app:
python app.py

Acesse via navegador:
http://localhost:5000

Estrutura esperada do banco:
A tabela csv_import deve conter os campos:

| Campo | Tipo     |
| ----- | -------- |
| MES   | Inteiro  |
| ANO   | Inteiro  |
| TOTAL | Numérico |


Desenvolvido como parte do desafio técnico para vaga de Programador Júnior por Iago Freitas de Sousa.