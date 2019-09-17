var getUsers = (criteria, cb) => {
  var query = 'SELECT * from `user`';
  // todo


  db.query(query, cb);
}


exports.findUser = (criteria, cb) => {
  getUsers(criteria, (err, result) => {
    if (err) return cb(err, null);
    if (result.length == 0) return cb(null, null);
    if (result.length >= 2) return cb(new Error('Not only one'), null);
    cb(null, result[0]);
  });
}

exports.comparePassword = (pwdCandidate, pwdHash) => {
  return true;
}