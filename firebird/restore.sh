#!/bin/bash
set -e

BACKUP_FILE="/firebird/data/employee.fbk"
TARGET_DB="/firebird/data/employee.fdb"

if [ ! -f "$TARGET_DB" ] && [ -f "$BACKUP_FILE" ]; then
  echo "Restaurando banco de dados a partir de $BACKUP_FILE..."
  /usr/local/firebird/bin/gbak -c -user sysdba -password masterkey "$BACKUP_FILE" "$TARGET_DB"
else
  echo "Banco de dados já existe ou arquivo de backup não encontrado."
fi
