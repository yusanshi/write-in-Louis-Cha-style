var express = require('express')
var cors = require('cors')
var bodyParser = require('body-parser')
var urlencodedParser = bodyParser.urlencoded({
    extended: false
})
var https = require('https')
var app = express()
const nodejieba = require("nodejieba")
nodejieba.load()

const port = 8000
const fs = require('fs')
const html = fs.readFileSync('./get.html', 'utf-8')

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/privkey.pem'),
    cert: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/cert.pem'),
    ca: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/chain.pem')
}

app.use(cors())

app.get('/', function (req, res) {
    res.send(html)
})

app.post('/', urlencodedParser, function (req, res) {
    var result = nodejieba.cut(req.body.sentence, true)
    console.log(result)
    res.json(result)
})

var server = https.createServer(options, app)

server.listen(port, function () {
    console.log('CORS-enabled web server listening on port ' + port)
})