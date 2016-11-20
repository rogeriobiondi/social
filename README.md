# social
Twitter data mining with Spark and Cassandra.

## Pré-requisitos

- Docker instalado (versão 1.10.3+)
- 32 GB de disco
- 8GB de RAM
- git instalado

## Como construir o container
```
  git clone https://github.com/rogeriobiondi/social.git
  cd social
  ./build.sh
```

## Como executar o container
```
  ./run.sh
```
Aguarde alguns minutos para realizar a inicialização.
Para coletar dados do tweeter, pode ser necessário aguardar alguns minutos ou horas.

## Como ver o relatório de tweets processados

http://ip_container:9000
