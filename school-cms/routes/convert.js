var express = require('express');
var router = express.Router();

router.get('/', function (req, res, next) {
  res.render('convert', { title: 'Convert' });
});

module.exports = router;
