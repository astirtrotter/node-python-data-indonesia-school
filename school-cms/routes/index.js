var express = require('express');
var router = express.Router();
var { spawn } = require('child_process');

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});


router.get('/convert', async function (req, res, next) {
  const logOutput = (name) => (message) => console.log(`[${name}] ${message}`);
  try {
    const output = await downloadJson();
    logOutput('main')(output.message);
    res.send('Success');
  } catch (e) {
    console.error('Error during download json script running ', e.stack);
    res.send('Failed');
  }
});

function downloadJson() {
  return new Promise((resolve, reject) => {
    const process = spawn('python', ['./dapo_spider.py']);

    const out = [];
    process.stdout.on('data', (data) => {
      out.push(data.toString());
      logOutput('stdout')(data);
    });

    const err = [];
    process.stderr.on('data', (data) => {
      err.push(data.toString());
      logOutput('stderr')(data);
    });

    process.on('exit', (code, signal) => {
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
