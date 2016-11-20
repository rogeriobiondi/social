#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import twitter
import json
import re
from cassandra.cluster import Cluster

# Constantes
# TODO Passar esses parâmetros na inicialização do container, como variáveis de ambiente
CONSUMER_KEY = 'iKD5x72adTtj6ZmFVgHbCDMfM'
CONSUMER_SECRET = 'eRNG2FOCOEtHr0JrNIAARkmg4Rh9yiZcQE4pOb4i1WefWaOjmG'
OAUTH_TOKEN = '728894222724640769-KGUk7K7R1XzNXYwjGBQtbDNeNvAthmF'
OAUTH_TOKEN_SECRET = 'z3eyPkwWeIxd3fSXiZDz62GImSueUjMKqpISTQ9Ux6rLg'

# Conexão ao twitter
api = twitter.Api(consumer_key=CONSUMER_KEY,
          consumer_secret=CONSUMER_SECRET,
          access_token_key=OAUTH_TOKEN,
          access_token_secret=OAUTH_TOKEN_SECRET,
          debugHTTP=True)

# Conexão ao Cassandra
cluster = Cluster()
session = cluster.connect('social')

# {u'contributors': None, u'truncated': False, u'text': u'Economy|Populist Policies Let #Brazil\u2019s Tomorrow Slip Away... https://t.co/UU0PiSIcRq', u'is_quote_status': False, u'in_reply_to_status_id': None, u'id': 799640088808275968, u'favorite_count': 0, u'source': u'<a href="http://dlvr.it" rel="nofollow">dlvr.it</a>', u'retweeted': False, u'coordinates': None, u'timestamp_ms': u'1479484028423', u'entities': {u'user_mentions': [], u'symbols': [], u'hashtags': [{u'indices': [30, 37], u'text': u'Brazil'}], u'urls': [{u'url': u'https://t.co/UU0PiSIcRq', u'indices': [62, 85], u'expanded_url': u'http://dlvr.it/MhXXjm', u'display_url': u'dlvr.it/MhXXjm'}]}, u'in_reply_to_screen_name': None, u'in_reply_to_user_id': None, u'retweet_count': 0, u'id_str': u'799640088808275968', u'favorited': False, u'user': {u'follow_request_sent': None, u'profile_use_background_image': True, u'id': 2782404078, u'verified': False, u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/506095748379705344/SOptiXPG_normal.jpeg', u'profile_sidebar_fill_color': u'DDEEF6', u'is_translator': False, u'geo_enabled': False, u'profile_text_color': u'333333', u'followers_count': 24646, u'protected': False, u'location': u'Florida', u'default_profile_image': False, u'id_str': u'2782404078', u'utc_offset': -28800, u'statuses_count': 613900, u'description': u"I think it's fine for girls to ask boys out. I actually prefer it.", u'friends_count': 23236, u'profile_link_color': u'1DA1F2', u'profile_image_url': u'http://pbs.twimg.com/profile_images/506095748379705344/SOptiXPG_normal.jpeg', u'notifications': None, u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme1/bg.png', u'profile_background_color': u'C0DEED', u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/2782404078/1409497625', u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'chloeesu', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 16922, u'name': u'Chloe', u'url': None, u'created_at': u'Sun Aug 31 15:05:59 +0000 2014', u'contributors_enabled': False, u'time_zone': u'Pacific Time (US & Canada)', u'profile_sidebar_border_color': u'C0DEED', u'default_profile': True, u'following': None, u'listed_count': 351}, u'geo': None, u'in_reply_to_user_id_str': None, u'possibly_sensitive': False, u'lang': u'en', u'created_at': u'Fri Nov 18 15:47:08 +0000 2016', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': None}
# TODO passar a lista de tags como uma variável de ambiente ou em arquivo de configuração.
tags = ['#brasil', '#brazil', '#brasil2016', '#brazil2016', '#jogosolimpicos', \
        '#olimpiadas', '#olimpiadas2016', '#olympics', '#rio2016', '#riojaneiro']

# Le os tweets e grava no Cassandra
for tweet in api.GetStreamFilter(track = tags):
    t = json.dumps(tweet).encode('utf-8')
    tw = json.loads(t)
    # TODO coluna do tipo SET no Cassandra é capaz de armazenar vários hashtags
    tagTweet = '#unknown'
    for tag in tags:
        if tag in tw['text'].lower():
            tagTweet = tag
    # A API do Twitter tem bug e raras vezes traz tweets sem as palavras/tags especificadas. Ignorar
    if tagTweet == '#unknown':
        continue;
    # Retirar do tweet caracteres indesejados
    texto = tw['text']
    texto = texto.replace("'", "")
    texto = texto.replace('"', '')
    texto = texto.replace('\n', '')
    texto = texto.replace('\r', '')
    texto = texto.replace('\t', '')
    # Ajusta timezone/data
    hora = long(tw['timestamp_ms']) - (2 * 60 * 60 * 1000)
    # Criar o comando CQL
    cql = u"INSERT INTO social.tweets (id, datahora, tag, autor, texto, numero_followers, lang) VALUES ('"
    cql = cql + str(tw['id']) + "', " + str(hora) + ",  '" + tagTweet + "' , '"
    cql = cql + tw['user']['screen_name'] + "', '" + texto + "', "
    cql = cql + str(tw['user']['followers_count']) + ", '" + tw['lang'] + "')"
    try:
        print cql.encode('utf-8')
        session.execute(cql.encode('utf-8'));
    except Exception, e:
        # Mesmo com todas as consistências, se ocorrer um erro de alguma natureza,
        # tratar e enviar para o log
        print "### Erro parsing tweet: " + str(e)
        print cql.encode('utf-8')
        pass
    print "\n"
