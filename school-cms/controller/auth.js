var passport = require('passport');
var createError = require('http-errors');

exports.login = passport.authenticate('local', {
  successRedirect: '/',
  failureRedirect: '/auth/login',
  failureFlash: true
});

exports.signup = (req, res, next) => {
  next(createError.NotImplemented());
}

exports.signout = (req, res, next) => {
  req.logout();
  res.redirect('/');
}