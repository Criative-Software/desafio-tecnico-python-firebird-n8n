docker exec -it desafio_tecnico_firebird bash

/usr/local/firebird/bin/gbak -c -user sysdba -password masterkey /firebird/data/employee.fbk /firebird/data/employee.fdb
