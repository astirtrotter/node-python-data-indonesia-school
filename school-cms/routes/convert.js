var express = require('express');
var router = express.Router();

router.get('/', function (req, res, next) {
  res.render('convert', { title: 'Convert' });
});

router.post('/', function (req, res, next) {
  res.json({ success: true });
});

module.exports = router;
