var express = require('express');
var router = express.Router();

router.get('/', function (req, res, next) {
  // get all directories under 'data'
  var directories = require('../util/fs').getDirectories('data');
  res.render('convert', { title: 'Convert', directories });
});

router.post('/', function (req, res, next) {
  res.json({ success: true });
});

module.exports = router;
