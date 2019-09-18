const { readdirSync } = require('fs');
const { join } = require('path');

exports.getDirectories = source => {
  return readdirSync(source, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
}