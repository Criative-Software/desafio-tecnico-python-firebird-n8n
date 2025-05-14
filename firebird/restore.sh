#!/bin/bash

CONTAINER_NAME="firebird25"
FBK_PATH="/firebird/employee.fbk"
FDB_PATH="/firebird/data/employee.fdb"
GBAK_PATH="/usr/local/firebird/bin/gbak"

echo "🔁 Restaurando backup Firebird..."

# Verifica se o container está rodando
if ! docker ps --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
  echo "❌ Container $CONTAINER_NAME não está rodando. Inicie com: docker compose up -d"
  exit 1
fi

# Executa o comando gbak dentro do container
docker exec -it $CONTAINER_NAME bash -c "$GBAK_PATH -c -v $FBK_PATH $FDB_PATH -user sysdba -password masterkey"

# Verifica se o .fdb foi criado
docker exec -it $CONTAINER_NAME bash -c "ls -lh $FDB_PATH && echo '✅ Restauração concluída com sucesso!'"
