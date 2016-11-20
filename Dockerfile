FROM ubuntu:16.04
MAINTAINER Rogerio Biondi

# Instalar Utils e Python
RUN echo "*** Atualizando Container..." && \
    apt-get update && \
    echo "*** Instalando Utils e Python..." && \
    apt-get -y install wget git make curl software-properties-common python-software-properties python-setuptools python-dev build-essential python-pip netcat && \
    pip install --upgrade pip && \
    pip install cassandra-driver && \
    pip install python-twitter

# Instalar Java
RUN add-apt-repository ppa:webupd8team/java
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN apt-get update -y --force-yes
RUN apt-get install -y --force-yes oracle-java8-installer
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Instalar NodeJs
RUN echo "*** Instalando NodeJS" && \
    curl -sL https://deb.nodesource.com/setup_6.x | bash && \
    apt-get -y install nodejs

# Instalar Scala
RUN echo "*** Instalando Scala" && \
    wget http://www.scala-lang.org/files/archive/scala-2.10.4.tgz && \
    mkdir /usr/local/src/scala && \
    tar xvf scala-2.10.4.tgz -C /usr/local/src/scala/ && \
    rm /scala-2.10.4.tgz
ENV SCALA_HOME /usr/local/src/scala/scala-2.10.4
ENV PATH $SCALA_HOME/bin:$PATH

# Instalar Spark (Standalone Mode)
RUN echo "*** Instalando Spark (Single Node)" && \
    wget http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz && \
    tar xvf spark-2.0.2-bin-hadoop2.7.tgz && \
    rm spark-2.0.2-bin-hadoop2.7.tgz
ENV SPARK_HOME /spark-2.0.2-bin-hadoop2.7
ENV PATH $SPARK_HOME/bin:$PATH

# Instalar Cassandra (Single Node)
RUN wget http://ftp.unicamp.br/pub/apache/cassandra/3.9/apache-cassandra-3.9-bin.tar.gz && \
    mkdir /cassandra-3.9 && \
    tar -xvf apache-cassandra-3.9-bin.tar.gz -C /cassandra-3.9 --strip-components=1 && \
    rm /apache-cassandra-3.9-bin.tar.gz
ENV CASSANDRA_HOME /cassandra-3.9
ENV PATH $CASSANDRA_HOME/bin:$PATH

# Script de inicializacao do container
ADD start.sh /
RUN chmod a+x /start.sh

EXPOSE 9000 8000

# Define default command.
CMD ["bash", "./start.sh"]

# ADD app.js /var/www/app.js
# CMD ["/usr/bin/node", "/var/www/app.js"]
# CMD ["/bin/bash"]
