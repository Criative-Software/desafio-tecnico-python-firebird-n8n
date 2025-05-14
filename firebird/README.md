# Firebird – Banco de Dados do Desafio Técnico

Este diretório contém o ambiente e dados necessários para execução do banco Firebird 2.5 utilizado no desafio técnico.

## 📦 Conteúdo

- `employee.fbk`: backup original da base de dados (`.fbk`)
- `data/`: diretório usado pelo Docker para persistência
- `docker-compose.yml`: arquivo de configuração do container Firebird
- `restore.sh`: script para restaurar o `.fbk` dentro do container (opcional)

## ▶️ Como subir o banco

```bash
docker-compose up -d
O banco estará acessível em localhost:3050.

🗃️ Estrutura esperada da tabela usada no sistema
Tabela csv_import:
| Campo | Tipo    |
| ----- | ------- |
| MES   | INTEGER |
| ANO   | INTEGER |
| TOTAL | NUMERIC |

🔁 Como restaurar o banco (opcional)
Se necessário, use:
bash restore.sh
