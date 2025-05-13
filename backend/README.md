# Análise de Vendas - Relatório Firebird
Ferramenta para análise de dados de vendas armazenados em banco de dados Firebird, com geração de relatórios CSV e visualizações em formato PNG.
## Funcionalidades

Conecta ao banco de dados Firebird

Extrai dados de vendas mensais e por vendedor

Gera arquivos CSV com os dados

Cria gráficos de barras para visualização

Exporta relatórios em formato PNG

## Requisitos

Python 3.6+

FDB (Firebird Database API)

Pandas

Matplotlib

Seaborn

## Instalação 

Clone o repositório:

```cmd
git clone https://github.com/ana-rabelo/desafio-tecnico-python-firebird-n8n
cd backend
```

Então,execute o seguinte comando para instalar as dependências:

```cmd
pip install -r requirements.txt
```

### Configuração do Firebird 2.5

#### Opção 1: Usando Docker (Recomendado)

1. Inicie o container Firebird usando Docker Compose:

```bashdocker-compose up -d```

O banco de dados estará disponível em:

```
Host: localhost
Porta: 3050
Banco de dados: employee
Usuário: sysdba
Senha: masterkey
```

#### Opção 2: Banco de Dados Existente
Se você já possui um servidor Firebird instalado,  configure os parâmetros de conexão no início da função `main()` ou através de variáveis de ambiente.

### Uso

1. Configure os parâmetros de conexão do banco de dados (se necessário)

2. Execute:

```bash
python main.py
```

3. Ao executar o script os arquivos serão criados:

- ```/backend/files/``` - Arquivos CSV 
- ```/backend/charts/``` - Gráficos PNG 

### Estrtura de diretórios

```
.
├── backend/
│   ├── README.md            # instruções do desafio back‑end
│   ├── requirements.txt     # dependências do desafio
│   └── main.py              # script Python
└── .gitignore
├── docker.compose.yml       # configuração Firebird
├── employee.fbk             # arquivo disponibilizado para a realização do teste
└── README.md                # este arquivo
```
