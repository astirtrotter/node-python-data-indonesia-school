const fs = require('fs');
const { join } = require('path');

exports.makeDirectoryIfNotExist = (directoryName) => {
  if (!fs.existsSync(directoryName)) fs.mkdirSync(directoryName);
}

exports.getDirectories = source => {
  this.makeDirectoryIfNotExist('data');

  return fs.readdirSync(source, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
}