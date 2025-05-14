FROM ubuntu:20.04

# Instalar pacotes necessários
RUN apt-get update && apt-get install -y \
    firebird2.5-server \
    firebird2.5-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de backup para dentro do container
COPY ./employee.fbk /var/lib/firebird/data/employee.fbk

# Configurar o Firebird
RUN echo "Starting Firebird..."
RUN /etc/init.d/firebird2.5-server start

# Expor a porta 3050
EXPOSE 3050

CMD ["/usr/sbin/fbguard", "/etc/firebird/firebird.conf"]
