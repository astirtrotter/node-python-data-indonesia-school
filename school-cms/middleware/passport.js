const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const User = require('../model/user');

passport.use(new LocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
},
  (email, password, done) => {
    User.findUser({ email: email }, (err, user) => {
      console.log(err, user);
      if (err) return done(err);
      if (!user) return done(null, false, { message: 'Incorrect email' });
      if (!User.comparePassword(password, user.password_hash)) {
        return done(null, false, { message: 'Incorrect password' });
      }
      done(null, user);
    });
  }
));

passport.serializeUser((user, done) => {
  done(null, user.id);
});

passport.deserializeUser((id, done) => {
  User.findUser({id: id}, done);
});

module.exports = passport;