#!/bin/bash
#
# pyspark --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 --conf spark.cassandra.connection.host=localhost
# spark-submit --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 --conf spark.cassandra.connection.host=localhost spark.py
#
from pyspark.sql.types import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import time

conf = SparkConf() \
    .setAppName("spark-twitter") \
    .set("spark.cassandra.connection.host", "localhost") \
    .set("spark.cassandra.connection.port", "9042")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

while True:

    # Realiza a varredura a cada 1 min.
    time.sleep(60)

    tweets = sqlContext.read.format("org.apache.spark.sql.cassandra") \
      .options(table="tweets", keyspace="social") \
      .load()

    rddTweets = tweets.rdd

    # Gerar Top5
    lista5 = tweets.select(["autor", "numero_followers"]) \
                 .distinct() \
                 .sort("numero_followers", ascending=False) \
                 .head(5)
    top5 = map(lambda u: (u["autor"], u["numero_followers"]), lista5)
    top5Schema = StructType([
        StructField("autor", StringType(), True),
        StructField("numero_followers", IntegerType(), True),
    ])
    dfTop5 = sqlContext.createDataFrame(top5, top5Schema)
    dfTop5.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode('overwrite') \
        .options(table="top5", keyspace="social") \
        .save()

    # Contagem Tweets lang='pt'
    contagemTags = tweets.filter("lang = 'pt'") \
                .groupBy("tag") \
                .count() \
                .collect()
    tags = map(lambda t: (t["tag"], t["count"]), contagemTags)
    tagsSchema = StructType([
        StructField("tag", StringType(), True),
        StructField("count", IntegerType(), True),
    ])
    dfTags = sqlContext.createDataFrame(tags, tagsSchema)
    dfTags.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode('overwrite') \
        .options(table="tags", keyspace="social") \
        .save()

    # Contagem Tweets/Hora
    tweetsHora = rddTweets.map(lambda linha: ( linha['datahora'].hour, 1 ) ) \
                .reduceByKey(lambda x, y: x+y) \
                .collect()
    tweetsSchema = StructType([
        StructField("hora", IntegerType(), True),
        StructField("count", IntegerType(), True),
    ])
    dfDia = sqlContext.createDataFrame(tweetsHora, tweetsSchema)
    dfDia.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode('overwrite') \
        .options(table="dia", keyspace="social") \
        .save()
