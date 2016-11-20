#/bin/bash
echo "### Starting Cassandra..."
nohup $CASSANDRA_HOME/bin/cassandra -R &

echo "### Starting Spark..."
nohup $SPARK_HOME/sbin/start-master.sh &

echo "### Aguardando Cassandra Iniciar..."
opened=0
while ! nc -vz localhost 9042; do
  echo "Aguardando cassandra iniciar na porta 9042..."
  sleep 10
done
echo "   Cassandra iniciado."
echo "### Criando Keyspace e Tabelas no Cassandra..."
cqlsh -f /app/cassandra/model.cql

echo "### Iniciando captura twitter..."
nohup /app/code/python/twitter-connector.py &

echo "### Iniciando processo spark de agregação..."
nohup spark-submit --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 --conf spark.cassandra.connection.host=localhost /app/code/spark/spark.py &

echo "### Iniciando microserviço REST/JSON..."
cd /app/code/node/microservice
npm install
nohup npm start &

echo "### Iniciando dashboard web..."
cd /app/code/node/web
npm install
npm -g install bower
bower install --allow-root
nohup npm start &

echo "### Processo de inicialização do container concluído!"
echo "Acesse o dashboard no endereço http://<ip_container>:9000"
echo "Para fechar o container, digite exit."
/bin/bash
