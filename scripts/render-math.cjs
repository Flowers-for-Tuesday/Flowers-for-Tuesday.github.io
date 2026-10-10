// Render all equations in one process. Output includes MathML for screen readers.
const fs = require('node:fs');
const katex = require('../assets/vendor/katex/katex.min.js');
const equations = JSON.parse(fs.readFileSync(0, 'utf8'));
const results = equations.map(({tex, display}) => {
  try {
    return {html: katex.renderToString(tex, {
      displayMode: display,
      output: 'htmlAndMathml',
      throwOnError: true,
      strict: 'ignore',
      trust: false,
      maxExpand: 1000,
    })};
  } catch (error) {
    return {error: error.message};
  }
});
process.stdout.write(JSON.stringify(results));
