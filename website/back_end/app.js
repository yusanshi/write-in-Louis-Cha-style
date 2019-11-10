var express = require('express')
var cors = require('cors')
var bodyParser = require('body-parser')
var urlencodedParser = bodyParser.urlencoded({
    extended: false
})
var http = require('http')
var app = express()
const nodejieba = require("nodejieba")
nodejieba.load()

const port = 8081
const fs = require('fs')
const html = fs.readFileSync('./get.html', 'utf-8')

app.use(cors())

app.get('/', function (req, res) {
    res.send(html)
})

app.post('/', urlencodedParser, function (req, res) {
    var result = nodejieba.cut(req.body.sentence, true)
    console.log(result)
    res.json(result)
})

var server = http.createServer(app)

server.listen(port, function () {
    console.log('CORS-enabled web server listening on port ' + port)
})
