# Sistema de Consulta de Vendas

Um sistema simples para consulta e exportação de vendas mensais utilizando Flask e banco de dados Firebird.

## 🗄️ Estrutura do banco de dados

O sistema assume que você já possui um banco de dados Firebird (`employee`) com a seguinte estrutura, no mínimo:

- TABELA `SALES` com os campos:
    - PO_NUMBER
    - CUST_NO
    - ORDER_DATE
    - QTY_ORDERED
    - TOTAL_VALUE

- TABELA `CUSTOMER` com campos:
    - CUST_NO
    - CONTACT_FIRST

## ⬇️ Instalação

1. Clone este repositório (`git clone https://github.com/ana-rabelo/desafio-tecnico-python-firebird-n8n.git`)

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Rode a aplicação:
   ```bash
   python app.py
   ```
O sistema estará disponível em `http://localhost:5000`.

## 🗂️ Estrutura do projeto

```
/ frontend
├── static/                   # Arquivos estáticos
│   ├── icon/                 # Ícones
│   │   └── analise-de-dados.png          # Ícone da aplicação
│   └── style/                # Estilos CSS
│       └── index.style.css   # Arquivo de estilo
├── templates/                # Templates HTML
│   └── index.html            # Template principal
├── app.py                    # Código principal da aplicação
├── README.md                 # Este arquivo
└── requirements.txt          # Dependências
```

## ⚙️ Configuração

Edite o arquivo `app.py` se necessário para alterar as configurações de conexão com o banco de dados:

```python
def db_connection():
    ...
    con = fdb.connect(host='localhost', 
                        database='employee',
                        user='sysdba', 
                        password='masterkey')
    ...
```

## 💡 Funcionalidades

- Seleção de mês e ano para consulta de vendas
- Exibição de resultados em tabela
- Exportação dos dados para Excel