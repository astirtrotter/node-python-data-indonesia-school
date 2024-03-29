require('dotenv').config();

var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var flash = require('connect-flash');
var methodOverride = require('method-override');
var fileUpload = require('express-fileupload');
var session = require('express-session');
var MySQLStore = require('express-mysql-session')(session);
var cors = require('cors');
var mysql = require('mysql');

var app = express();
var passport = require('./middleware/passport');
var dbConfig = require('./config/db');

var db = mysql.createConnection(dbConfig);
db.connect(err => {
  if (err) {
    throw err;
  }
  console.log('Connected to database');
});
global.db = db;

var sessionStore = new MySQLStore(dbConfig);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(methodOverride('_method'));
app.use(flash());
app.use(fileUpload({
  createParentPath: true,
  limits: {
    fileSize: 50 * 1024 * 1024 // 50 MB
  }
}));
app.use(session({
  key: process.env.SESSION_KEY,
  secret: process.env.SESSION_SECRET,
  store: sessionStore,
  resave: false,
  saveUninitialized: false
}));
app.use(cors());
app.use(passport.initialize());
app.use(passport.session());

// routes
app.use(function (req, res, next) {
  let render = res.render;
  res.render = (view, locals, cb) => {
    if (typeof locals == 'object') {
      locals.user = req.user;
      locals.url = req.url;
      locals.messages = req.flash();
    }
    render.call(res, view, locals, cb);
  };

  next();
});
app.use('/', require('./routes/index'));
app.use('/convert', require('./routes/convert'));
app.use('/download', require('./routes/download'));
app.use('/auth', require('./routes/auth'));

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError.NotFound());
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
