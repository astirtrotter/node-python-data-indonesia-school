var express = require('express');
var router = express.Router();

router.get('/login', function (req, res, next) {
  res.render('auth/login', { title: 'Login' });
});

router.get('/signup', function (req, res, next) {
  res.render('auth/signup', { title: 'Signup' });
});

module.exports = router;
