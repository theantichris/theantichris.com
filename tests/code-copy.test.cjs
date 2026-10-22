const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const test = require('node:test');
const vm = require('node:vm');

function setup(writeText) {
  let click;
  const button = {
    classList: { add() {} },
    addEventListener(event, callback) { click = callback; },
  };
  const code = {
    innerText: 'first line\n\n  indented line\n\n',
    dataset: { lang: 'go' },
    parentElement: { closest() { return { prepend() {} }; } },
  };
  vm.runInNewContext(readFileSync('assets/js/code.js', 'utf8'), {
    document: {
      querySelectorAll() { return [code]; },
      createElement(tag) {
        return tag === 'button' ? button : { classList: { add() {} }, append() {} };
      },
    },
    navigator: { clipboard: { writeText } },
    setTimeout() {},
  });
  return { button, click, code };
}

test('copy preserves blank lines, indentation, and trailing newline', async () => {
  let copied;
  const { button, click, code } = setup(async (text) => { copied = text; });
  await click();
  assert.equal(copied, code.innerText);
  assert.equal(button.innerText, 'Copied');
});

test('clipboard rejection does not report success', async () => {
  const { button, click } = setup(async () => { throw new Error('Permission denied'); });
  await click();
  assert.equal(button.innerText, 'Copy failed');
});
