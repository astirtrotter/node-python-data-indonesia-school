var express = require('express');
var router = express.Router();
var authController = require('../controller/auth');

router.get('/login', function (req, res, next) {
  res.render('auth/login', { title: 'Login' });
});

router.get('/signup', function (req, res, next) {
  res.render('auth/signup', { title: 'Signup' });
});

router.post('/login', authController.login);
router.post('/signup', authController.signup);
router.post('/signout', authController.signout);

module.exports = router;
