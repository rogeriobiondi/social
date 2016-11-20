CREATE KEYSPACE IF NOT EXISTS social
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

CREATE TABLE IF NOT EXISTS social.tweets (
	id text,
  datahora timestamp,
  tag text,
  autor text,
 	texto text,
  numero_followers int,
	lang text,
	PRIMARY KEY (id, datahora)
) WITH CLUSTERING ORDER BY (datahora DESC);

CREATE TABLE IF NOT EXISTS social.top5 (
	autor text,
  numero_followers int,
	PRIMARY KEY (autor, numero_followers)
) WITH CLUSTERING ORDER BY (numero_followers DESC);

CREATE TABLE IF NOT EXISTS social.tags (
	tag text,
  count int,
	PRIMARY KEY (tag, count)
) WITH CLUSTERING ORDER BY (count DESC);

CREATE TABLE IF NOT EXISTS social.dia (
	hora int,
  count int,
	PRIMARY KEY (count, hora)
) WITH CLUSTERING ORDER BY (hora ASC);
