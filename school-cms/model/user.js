var getUsers = (criteria, cb) => {
  var query = 'SELECT * FROM `user`';
  // todo
  if (criteria) {
    var subs = [];
    if (criteria.id)    subs.push(` id='${criteria.id}'`);
    if (criteria.email) subs.push(` email='${criteria.email}'`);
    if (criteria.name)  subs.push(` name='${criteria.name}'`);

    if (subs.length > 0) query += ' WHERE ' + subs.join(' AND ');
  }

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
  // todo: use bcrypt
  return pwdCandidate === pwdHash;
}