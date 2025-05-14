Claro! Aqui está o README atualizado **sem a seção "Clone este repositório"**:

---

# 🐦 Firebird Docker - Desafio Técnico

Este repositório contém um ambiente Docker configurado para rodar o **Firebird 2.5.9** usando a imagem `jacobalberty/firebird`. Ele é ideal para testes e desenvolvimento de sistemas que utilizam esse banco de dados.

## 🔧 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Como usar

1. **Suba o container:**

   ```bash
   docker-compose up -d
   ```

2. **Acesse o Firebird:**

   - **Host:** `localhost`
   - **Porta:** `3051`
   - **Usuário:** `seu usario`
   - **Senha:** `sua senha`

3. **Volume de dados:**

   Os dados do banco ficam persistidos na pasta `./data` do seu projeto.

## 🔄 Restaurando um backup `.fbk`

Se você possui um arquivo de backup do Firebird (`.fbk`), pode restaurá-lo dentro do container com o comando abaixo:

```bash
docker exec -it desafio_tecnico_firebird \
  /usr/local/firebird/bin/gbak -c \
  -user sysdba -password masterkey \
  /firebird/data/employee.fbk \
  /firebird/data/employee.fdb
```

> 💡 Certifique-se de que o arquivo `employee.fbk` está dentro da pasta `./data` do projeto antes de executar o comando acima.

## 📁 Estrutura

```yaml
services:
  firebird:
    image: jacobalberty/firebird:2.5.9-sc
    restart: always
    container_name: desafio_tecnico_firebird
    environment:
      FIREBIRD_USER: seu usario
      ISC_PASSWORD: sua senha
    ports:
      - "3051:3050"
    volumes:
      - ./data:/firebird/data

volumes:
  firebird-data:
```

## 🧼 Parar e remover o container

```bash
docker-compose down
```

Se quiser remover também os volumes persistentes:

```bash
docker-compose down -v
```

Com certeza! Aqui está uma versão **resumida e amigável** para adicionar ao seu `README.md`, explicando o uso do script Python com base no código fornecido:

---

## 📊 Análise de Vendas com Python

Este projeto também inclui um script Python que se conecta ao banco Firebird, executa consultas e gera relatórios visuais.

### Funcionalidades:

- Consulta de **vendas por mês** e **por vendedor**
- Exportação dos resultados para arquivos `.csv`
- Geração de gráficos de barras salvos como `.png`

### ▶️ Como usar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure um arquivo `.env` com as variáveis de conexão:

   ```
   DATABASE_URL=localhost:/firebird/data/employee.fdb
   USER=sysdba
   SECRET_KEY=masterkey
   ```

3. Execute o script principal:

   ```bash
   python nome_do_arquivo.py
   ```

Claro! Aqui está um README amigável e resumido para o seu projeto com a interface Streamlit:

---

# 📊 Sistema de Consulta de Vendas

Este projeto oferece uma **interface Streamlit** para consulta, visualização e exportação de dados de vendas armazenados em um banco Firebird. Ele permite que os usuários filtrem as vendas por mês e ano, visualizem as métricas principais e gerem gráficos e relatórios em formato Excel.

### Funcionalidades:

- **Consulta de vendas por mês**: Obtenha os dados de vendas agrupados por mês.
- **Exibição de métricas**: Mostra o total de vendas, pedidos e itens.
- **Gráfico de vendas**: Geração de um gráfico de barras das vendas por mês.
- **Exportação para Excel**: Exporte os dados para um arquivo Excel facilmente.
- **Filtros interativos**: Selecione ano e mês para filtrar os dados na interface.

### 📋 Requisitos

- [Python 3.7+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Firebird](https://firebirdsql.org/) (conectado via `fdb`)

### ⚙️ Como rodar o projeto

1. **Instale as dependências**:

   Execute o seguinte comando para instalar as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuração do Banco de Dados**:

   Crie um arquivo `.env` com as variáveis de configuração para o banco de dados Firebird:

   ```
   DATABASE_URL=localhost:/caminho/para/seu/banco.fdb
   USER=seu usario
   SECRET_KEY=sua senha
   ```

3. **Execute o aplicativo Streamlit**:

   Para rodar a interface, execute o comando:

   ```bash
   streamlit run app.py
   ```

4. **Interaja com a interface**:

   - Selecione o **ano** e **mês** na barra lateral para filtrar os dados.
   - Visualize as **métricas principais** (Total de Vendas, Total de Pedidos, Total de Itens).
   - Exporte os dados filtrados para um arquivo Excel.
   - Veja o **gráfico de vendas** gerado automaticamente.

### 🔧 Funcionalidades da Interface:

- **Filtros Interativos**: Selecione o ano e o mês para visualizar dados específicos.
- **Tabela**: Dados das vendas são exibidos em uma tabela interativa.
- **Gráfico**: Um gráfico de barras mostra o total de vendas por mês.
- **Exportação**: Baixe os dados filtrados em formato Excel.

### 📂 Estrutura de Arquivos

- `app.py`: Arquivo principal com a lógica do Streamlit.
- `requirements.txt`: Lista de dependências.
- `.env`: Arquivo para configurar o banco de dados.
