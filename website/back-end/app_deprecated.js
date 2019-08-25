const https = require('https');
const fs = require('fs');
const qs = require('querystring');
const nodejieba = require("nodejieba");

const html = fs.readFileSync('./get.html');

nodejieba.load();

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/privkey.pem'),
    cert: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/cert.pem'),
    ca: fs.readFileSync('/etc/letsencrypt/live/jieba.yusanshi.com/chain.pem')
};

const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS, POST, GET',
    'Access-Control-Max-Age': 2592000, // 30 days
    /** add other headers as per requirement */
};

const server = https.createServer(options, function (req, res) {
    if (req.method === 'OPTIONS') {
        res.writeHead(204, headers);
        res.end();
    } else if (req.method == 'POST') {
        var requestBody = '';
        req.on('data', function (chunk) {
            requestBody += chunk;
        });
        req.on('end', function () {
            var formData = qs.parse(requestBody);
            var result = nodejieba.cut(formData.sentence, true);
            console.log(result);
            res.writeHead(200);
            res.end(JSON.stringify(result));
        });
    } else if (req.method == 'GET') {
        res.writeHead(200);
        res.end(html);
    } else {
        res.writeHead(405, headers);
        res.end(`${req.method} is not allowed for the request.`);
    }
});

server.listen(8000);