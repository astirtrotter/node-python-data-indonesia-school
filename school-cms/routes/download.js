var express = require('express');
var router = express.Router();
var fsUtil = require('../util/fs');

var { spawn } = require('child_process');
const logOutput = (name) => (message) => console.log(`[${name}] ${message}`);

router.get('/', async function (req, res, next) {
  res.render('download', { title: 'Download' });
});

router.post('/', async function (req, res, next) {
  fsUtil.writeUrls(req.body.destination, req.body.url + '\n');
  try {
    const subprocess = runScript(req.body.destination);
    res.set('Content-Type', 'text/plain');
    subprocess.stdout.pipe(res);
    subprocess.stderr.pipe(res);
  } catch (e) {
    console.error('Error during download json script running ', e.stack);
    res.send('Failed');
  }
});

function runScript(dest) {
  const processDownload = spawn('python3', ['-u', 'dapo_spider.py', dest]);

  processDownload.stdout.on('data', (data) => {
    logOutput('download-stdout')(data);
  });

  processDownload.stderr.on('data', (data) => {
    logOutput('download-stderr')(data);
  });

  processDownload.on('exit', (code, signal) => {
    logOutput('download-exit')(`${code} (${signal})`);
  });

  processDownload.on('close', () => {
    logOutput('download-close')(``);
  });

  return processDownload;
}

module.exports = router;
