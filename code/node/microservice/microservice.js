"use strict";

var express    = require('express');
var cors = require('cors');
var app        = express();
var bodyParser = require('body-parser');

var cassandra = require('cassandra-driver');
var async = require('async');
var _ = require('lodash');

//Connect to the cluster
var client = new cassandra.Client({contactPoints: ['127.0.0.1'], keyspace: 'social'});

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, Content-Type, X-Requested-With, X-Auth-Token, Accept');
  next();
});

var port = process.env.PORT || 8000;
var address = process.env.ADDRESS || '0.0.0.0';

var router = express.Router();

router.get('/', function(req, res) {
  var payload = {
    top5 : {},
    tags : {},
    dia  : {},
    ultimos10 : []
  }
  async.series([
    function selectTop5(next) {
      var query = 'select autor, numero_followers from social.top5';
      client.execute(query, { prepare: true }, function (err, result) {
        if (err) return next(err);
        var top5 = { labels: [], data: [] };
        var lines = _.sortBy(result.rows, "numero_followers").reverse();
        for(let row of lines) {
          // console.log(row);
          top5.labels.push(row.autor);
          top5.data.push(row.numero_followers);
        }
        payload.top5 = top5;
        next();
      });
    },
    function selectTags(next) {
      var query = 'select tag, count from social.tags;';
      client.execute(query, { prepare: true }, function (err, result) {
        if (err) return next(err);
        var tags = { labels: [], data: [] };
        var lines = _.sortBy(result.rows, "count").reverse();
        for(let row of lines) {
          // console.log(row);
          tags.labels.push(row.tag);
          tags.data.push(row.count);
        }
        payload.tags = tags;
        next();
      });
    },
    function selectDia(next) {
      var query = 'select hora,count from social.dia';
      client.execute(query, { prepare: true }, function (err, result) {
        if (err) return next(err);
        var dia = { labels: [], data: [] };
        var lines = _.sortBy(result.rows, "hora").reverse();
        for(let row of lines) {
          // console.log(row);
          dia.labels.push(row.hora);
          dia.data.push(row.count);
        }
        payload.dia = dia;
        next();
      });
    },
    function selectUltimos10(next) {
      var query = 'select * from social.tweets';
      client.execute(query, { prepare: true }, function (err, result) {
        if (err) return next(err);
        var lines = _.sortBy(result.rows, "datahora").reverse();
        lines = _.take(lines, 10);
        payload.ultimos10 = lines;
        next();
      });
    },
    function ok(next) {
        res.status(200).json(payload);
        next();
    },
  ],
  function (err) {
    if (err) {
      console.error('Erro', err.message, err.stack);
    }
  });
});

app.use('/api', router);
app.listen(port, address);
console.log('Iniciando serviço REST na porta ' + port);
