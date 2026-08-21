#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const katex = require('katex');

function fail(message) {
  process.stderr.write(`STATIC KATEX FAIL: ${message}\n`);
  process.exit(1);
}

function decodeEntities(value) {
  return value
    .replaceAll('&amp;', '&')
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"')
    .replaceAll('&#39;', "'");
}

function embeddedCss() {
  const cssPath = require.resolve('katex/dist/katex.min.css');
  const cssRoot = path.dirname(cssPath);
  return fs.readFileSync(cssPath, 'utf8').replace(
    /url\((fonts\/[^)]+)\)/g,
    (_match, relative) => {
      const fontPath = path.join(cssRoot, relative);
      const extension = path.extname(fontPath).slice(1);
      const mime = extension === 'woff2' ? 'font/woff2' : extension === 'woff' ? 'font/woff' : 'application/octet-stream';
      const data = fs.readFileSync(fontPath).toString('base64');
      return `url(data:${mime};base64,${data})`;
    },
  );
}

const [input, output] = process.argv.slice(2);
if (!input || !output) fail('usage: render_static_katex.js <input.html> <output.html>');
if (path.resolve(input) === path.resolve(output)) fail('input and output must differ');

let html = fs.readFileSync(input, 'utf8');
let count = 0;
html = html.replace(
  /<span\s+class="math (display|inline)">([\s\S]*?)<\/span>/g,
  (_match, mode, encoded) => {
    count += 1;
    const tex = decodeEntities(encoded.trim());
    const rendered = katex.renderToString(tex, {
      displayMode: mode === 'display',
      throwOnError: true,
      strict: 'error',
      trust: false,
      output: 'htmlAndMathml',
    });
    return rendered.replace(/<annotation(?:\s[^>]*)?>[\s\S]*?<\/annotation>/g, '');
  },
);
if (count < 20) fail(`expected at least 20 equations, rendered ${count}`);
if (/<span\s+class="math (?:display|inline)">/.test(html)) fail('unrendered Pandoc math span remains');

html = html
  .replace(/\s*<script defer=""[\s\S]*?<\/script>/, '')
  .replace(/\s*<script>document\.addEventListener\("DOMContentLoaded"[\s\S]*?<\/script>/, '')
  .replace(/\s*<link rel="stylesheet"\s+href="https:\/\/cdn\.jsdelivr\.net\/npm\/katex@latest\/dist\/katex\.min\.css" \/>/, '')
  .replace('</head>', `<style id="katex-static">${embeddedCss()}</style>\n</head>`);

if (html.includes('application/x-tex') || html.includes('<annotation')) {
  fail('TeX annotation survived static rendering');
}
fs.writeFileSync(output, html);
process.stdout.write(JSON.stringify({ status: 'pass', equations: count, output }, null, 2) + '\n');
