# Backend - Sistema de Relatórios

Backend para consulta de vendas no banco de dados Firebird e geração de relatórios.

## Requisitos

- Python 3.8 ou superior
- Firebird 2.5
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

## Configuração do Banco de Dados

1. Certifique-se de que o Firebird 2.5 está instalado e rodando
2. Restaure o backup do banco de dados:
```bash
gbak -c -v employee.fbk employee.fdb
```

## Execução

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o script:
```bash
python main.py
```

## Funcionalidades

- Conexão com banco de dados Firebird
- Consulta de vendas por mês/ano
- Geração de relatórios em CSV
- Geração de gráficos em PNG
- Tratamento de erros e exceções

## Estrutura de Arquivos

- `main.py`: Script principal
- `requirements.txt`: Dependências do projeto
- `relatorios/`: Diretório para arquivos CSV gerados
- `imagens/`: Diretório para gráficos gerados 