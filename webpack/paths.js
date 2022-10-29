const path = require('path');

module.exports = {
  root: path.resolve(__dirname, '../'),
  outputPath: path.resolve(__dirname, '../', 'app/static/'),
  entryPath: {
    styles: path.resolve(__dirname, '../', 'client/styles/styles.scss'),
    main: path.resolve(__dirname, '../', 'client/index.jsx'),
  },
  templatePath: path.resolve(__dirname, '../', 'client/template.html'),
  imagesFolder: 'images',
  fontsFolder: 'fonts',
  cssFolder: 'styles',
  jsFolder: 'js',
};
