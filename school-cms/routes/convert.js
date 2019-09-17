var express = require('express');
var router = express.Router();

var { spawn } = require('child_process');
const logOutput = (name) => (message) => console.log(`[${name}] ${message}`);

router.get('/', async function (req, res, next) {
  res.render('convert');
  // try {
  //   const output = await downloadJson();
  //   logOutput('main')(output.message);
  //   res.send('Success');
  // } catch (e) {
  //   console.error('Error during download json script running ', e.stack);
  //   res.send('Failed');
  // }
});

async function downloadJson() {
  return new Promise((resolve, reject) => {
    const processDownload = spawn('python', ['./dapo_spider.py']);

    const out = [];
    processDownload.stdout.on('data', (data) => {
      out.push(data.toString());
      logOutput('stdout')(data);
    });

    const err = [];
    processDownload.stderr.on('data', (data) => {
      err.push(data.toString());
      logOutput('stderr')(data);
    });

    processDownload.on('exit', (code, signal) => {
      logOutput('exit')(`${code} (${signal})`);
      if (code !== 0) {
        reject(new Error(err.join('\n')));
        return;
      }
      try {
        resolve(JSON.parse(out[0]));
      } catch (e) {
        reject(e);
      }
    });
  });
}

module.exports = router;
