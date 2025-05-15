# Análise de Vendas - Relatório Firebird

1. Inicie o container Firebird usando Docker Compose:

```bash
docker-compose up -d
```
O banco de dados será iniciado em um container Docker. O banco de dados padrão é o `employee` e o usuário e senha são `sysdba` e `masterkey`, respectivamente. O banco de dados estará disponível na porta 3050.

2. Execute:

```bash
python main.py
```

3. Ao executar o script os arquivos serão criados:

- ```/backend/files/``` - Arquivos CSV 
- ```/backend/charts/``` - Gráficos PNG 