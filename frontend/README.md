# Frontend - Consulta de Vendas

Interface web para consulta e exportação de vendas por mês.

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

2. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o servidor:
```bash
python app.py
```
3. Acesse a aplicação em: http://localhost:5000

## Funcionalidades

- Seleção de mês/ano
- Visualização dos dados em tabela
- Exportação para Excel
- Interface responsiva
- Indicador de carregamento
- Envio de CSV via webhook para o n8n 