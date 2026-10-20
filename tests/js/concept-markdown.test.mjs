import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { resolveConceptPath } from '../../website/graph-contract.mjs';

import * as parser from '../../website/concept-markdown.mjs';
const { splitSections, parseFrontMatter, inlineMarkdown, renderSectionContent } = parser;
const base = 'https://example.test/published/Linear%20Regression/concept.md';

test('section split retains pre-section prose and title-less documents', () => {
  const doc = splitSections('# Model\nIntro **evidence**.\n\n## Definition\nBody');
  assert.equal(doc.title, 'Model');
  assert.equal(doc.preamble.join('\n'), 'Intro **evidence**.\n');
  assert.match(renderSectionContent(splitSections('Only prose.').preamble, base), /<p>Only prose\.<\/p>/);
});

for (const fence of ['```', '~~~~']) {
  test(`section split ignores headings within ${fence} fences`, () => {
    const doc = splitSections(`# Real\n## Definition\n${fence}text\n# Fake\n## Fake section\n${fence}\n## Provenance\nSource`);
    assert.equal(doc.sections.length, 2);
    assert.equal(doc.sections[0].title, 'Definition');
    assert.match(renderSectionContent(doc.sections[0].lines, base), /<pre><code># Fake\n## Fake section<\/code><\/pre>/);
  });
}

test('short or mismatched fence cannot close code block', () => {
  const doc = splitSections('# Real\n## Definition\n````md\n```\n## Still code\n~~~\n````\n## Provenance\nSource');
  assert.equal(doc.sections.length, 2);
  assert.match(renderSectionContent(doc.sections[0].lines, base), /```\n## Still code\n~~~/);
});

test('section parsing preserves literal hashes in concept names', () => {
  const doc = splitSections('# C#\n## Formula x#\nExact source.');
  assert.equal(doc.title, 'C#');
  assert.equal(doc.sections[0].title, 'Formula x#');
});

test('display math keeps heading-like lines and fence markers literal', () => {
  const doc = splitSections('# Real\n## Definition\n$$\n## x\n```\nx_1 = 2\n$$\n## Provenance\nSource');
  assert.equal(doc.sections.length, 2);
  const html = renderSectionContent(doc.sections[0].lines, base);
  assert.match(html, /class="math-block"/);
  assert.match(html, /## x\n```\nx_1 = 2/);
});

test('unterminated front matter never discards source text', () => {
  const input = '---\nUnknown: value\nSource prose';
  assert.equal(parseFrontMatter(input).body, input);
});

test('front matter preserves existing metadata contract', () => {
  const doc = parseFrontMatter('---\nconcept_name: "Model"\nversion_number: 2\n---\n# Model');
  assert.equal(doc.meta.concept_name, 'Model');
  assert.equal(doc.meta.version_number, '2');
  assert.equal(doc.body, '# Model');
});

test('balanced parentheses and titles do not truncate destinations', () => {
  const html = inlineMarkdown('[paper](../papers/Model_(v2).pdf#page=3 "Original source")', base);
  assert.match(html, /href="https:\/\/example.test\/published\/papers\/Model_\(v2\)\.pdf#page=3"/);
  assert.match(html, /title="Original source"/);
  assert.match(html, />paper<\/a>$/);
});

test('legacy evidence filenames containing spaces still resolve exactly', () => {
  const html = inlineMarkdown('[lecture](../data/raw/BT2101 Midterms (L1-6).pdf#page=1)', base);
  assert.match(html, /href="https:\/\/example.test\/published\/data\/raw\/BT2101%20Midterms%20\(L1-6\)\.pdf#page=1"/);
});

test('explicit legacy source root preserves shipped provenance targets without rebasing ordinary assets', () => {
  const html = renderSectionContent([
    '**[BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=1)**',
    '![plot](./figures/fit.png) [notes](./notes.md) [other](../data/raw-other/file.pdf)',
  ], base, { legacySourceRootUrl: 'https://example.test/repo/data/raw/' });
  assert.match(html, /href="https:\/\/example.test\/repo\/data\/raw\/BT2101\/BT2101%20Midterms%20\(L1-6\)\.pdf#page=1"/);
  assert.match(html, /src="https:\/\/example.test\/published\/Linear%20Regression\/figures\/fit.png"/);
  assert.match(html, /href="https:\/\/example.test\/published\/Linear%20Regression\/notes.md"/);
  assert.match(html, /href="https:\/\/example.test\/published\/data\/raw-other\/file.pdf"/);
});

test('images render as images with rebased paths and safe attributes', () => {
  const html = inlineMarkdown('![Plot & result](<figures/fit (final).png> "Fit & residuals")', base);
  assert.equal(html, '<img src="https://example.test/published/Linear%20Regression/figures/fit%20(final).png" alt="Plot &amp; result" title="Fit &amp; residuals">');
});

test('linked image renders figure inside one anchor with legacy source mapping', () => {
  const html = inlineMarkdown('[![Evidence](figure.png)](../data/raw/COURSE/source.pdf#page=2)', base,
    { legacySourceRootUrl: 'https://example.test/repo/data/raw/' });
  assert.equal(html, '<a href="https://example.test/repo/data/raw/COURSE/source.pdf#page=2" target="_blank" rel="noreferrer"><img src="https://example.test/published/Linear%20Regression/figure.png" alt="Evidence"></a>');
});

test('link labels allow images but never nested anchors', () => {
  const html = inlineMarkdown('[[inner](inner.pdf) ![Evidence](figure.png)](source.pdf)', base);
  assert.equal((html.match(/<a\b/g) || []).length, 1);
  assert.match(html, /<img src="https:\/\/example.test\/published\/Linear%20Regression\/figure.png" alt="Evidence">/);
  assert.doesNotMatch(html, /href="[^"]*inner.pdf"/);
});

test('linked images retain unsafe URL rejection for image and anchor destinations', () => {
  for (const url of ['javascript:alert(1)', 'data:text/html,boom', 'file:///etc/passwd', 'jav&#x61;script:alert(1)']) {
    const unsafeImage = inlineMarkdown(`[![Evidence](${url})](source.pdf)`, base);
    assert.equal(unsafeImage, '<a href="https://example.test/published/Linear%20Regression/source.pdf" target="_blank" rel="noreferrer">Evidence</a>');
    const unsafeAnchor = inlineMarkdown(`[![Evidence](figure.png)](${url})`, base);
    assert.equal(unsafeAnchor, '<img src="https://example.test/published/Linear%20Regression/figure.png" alt="Evidence">');
  }
});

test('relative links, query and fragment use Markdown URL rather than viewer URL', () => {
  const html = inlineMarkdown('[source](./evidence.md?view=raw&v=2#page=4) [anchor](#proof)', base);
  assert.match(html, /href="https:\/\/example.test\/published\/Linear%20Regression\/evidence.md\?view=raw&amp;v=2#page=4"/);
  assert.match(html, /href="https:\/\/example.test\/published\/Linear%20Regression\/concept.md#proof"/);
});

for (const url of ['javascript:alert(1)', 'data:text/html,boom', 'file:///etc/passwd', 'jav&#x61;script:alert(1)', 'java\nscript:alert(1)']) {
  test(`unsafe destination remains inert: ${JSON.stringify(url)}`, () => {
    const html = inlineMarkdown(`[label](${url}) ![plot](${url})`, base);
    assert.doesNotMatch(html, /<(?:a|img)\b/);
    assert.match(html, /label/);
    assert.match(html, /plot/);
  });
}

test('raw HTML and quoted titles cannot inject markup', () => {
  const html = inlineMarkdown('<img src=x onerror=alert(1)> [safe](https://example.test "&quot; onmouseover=boom")', base);
  assert.match(html, /^&lt;img/);
  assert.doesNotMatch(html, /<img/);
  assert.match(html, /title="&quot; onmouseover=boom"/);
});

test('code spans isolate Markdown and escape HTML exactly once', () => {
  assert.equal(inlineMarkdown('`<tag>&`', base), '<code>&lt;tag&gt;&amp;</code>');
  assert.equal(inlineMarkdown('`**literal**`', base), '<span class="inline-math">\\(**literal**\\)</span>');
  assert.doesNotMatch(inlineMarkdown('`[label](https://example.test)`', base), /<a\b/);
});

test('equations retain existing inline and display MathJax hooks', () => {
  assert.equal(inlineMarkdown('`x_i = 2`', base), '<span class="inline-math">\\(x_i = 2\\)</span>');
  assert.equal(inlineMarkdown('$x_i ** y$ and \\(a_b\\)', base), '$x_i ** y$ and \\(a_b\\)');
  const html = renderSectionContent(['$$', '\\theta_{t+1} = \\theta_t - \\alpha', '$$', '$$x = 1$$'], base);
  assert.match(html, /\\theta_\{t\+1\} = \\theta_t - \\alpha/);
  assert.equal((html.match(/class="math-block"/g) || []).length, 2);
});

test('code blocks escape literally without interpreting markup', () => {
  const html = renderSectionContent(['```html', '<b>& **literal**</b>', '```'], base);
  assert.equal(html, '<pre><code>&lt;b&gt;&amp; **literal**&lt;/b&gt;</code></pre>');
});

test('tables preserve header, cells, escaped pipes and inline equations', () => {
  const html = renderSectionContent(['| Symbol | Meaning |', '| :--- | ---: |', '| `x_i` | $P(A|B)$ |', '| A\\|B | **union** |'], base);
  assert.equal((html.match(/<th>/g) || []).length, 2);
  assert.equal((html.match(/<td>/g) || []).length, 4);
  assert.match(html, /<td>\$P\(A\|B\)\$<\/td>/);
  assert.match(html, /<td>A\|B<\/td>/);
  assert.match(html, /<strong>union<\/strong>/);
});

test('paragraphs before subheadings and adjacent list types keep order', () => {
  const html = renderSectionContent(['Before.', '### Detail', 'After.', '', '- Item', '1. Step'], base);
  assert.ok(html.indexOf('<p>Before.</p>') < html.indexOf('<h3>Detail</h3>'));
  assert.match(html, /<ul><li>Item<\/li><\/ul>\s*<ol><li>Step<\/li><\/ol>/);
});

for (const deployment of [
  { name: 'default root', dataset: {}, sourceRoot: 'https://example.test/data/raw/' },
  { name: 'configured root', dataset: { repoRootUrl: '../repo', refinedRootUrl: '../repo/published/' }, sourceRoot: 'https://example.test/repo/data/raw/' },
]) test(`viewer retains prefix and source links with Markdown-relative assets: ${deployment.name}`, async () => {
  const elements = new Map();
  const element = () => ({ style: {}, children: [], appendChild(child) { this.children.push(child); } });
  const document = {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, element());
      return elements.get(id);
    },
    createElement: element,
    documentElement: { dataset: deployment.dataset, scrollHeight: 1000 },
  };
  const window = {
    location: { href: 'https://example.test/website/concept.html', search: deployment.dataset.repoRootUrl ? '?path=../repo/published/Model/concept.md' : '?path=../knowledge_base/refined/Model/concept.md' },
    MathJax: { typesetPromise: async () => {} }, innerHeight: 1000, scrollY: 0, addEventListener() {},
  };
  const fetched = [];
  const source = (await readFile(new URL('../../website/concept.js', import.meta.url), 'utf8'))
    .replace(/^import .*?;\s*$/gm, '')
    .replace('main().catch', 'globalThis.renderDone = main().catch');
  const context = vm.createContext({
    ...parser, resolveConceptPath, document, window, URLSearchParams, URL,
    fetch: async url => {
      fetched.push(String(url));
      return { ok: true, url: base, text: async () => '# Model\nIntro evidence.\n## Definition\n![plot](./plot.png)\n## Provenance\n[BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=1)' };
    },
  });
  vm.runInContext(source, context);
  await context.renderDone;
  const sections = elements.get('concept-article').children;
  assert.equal(sections.length, 3);
  assert.match(sections[0].innerHTML, /<p>Intro evidence\.<\/p>/);
  assert.match(sections[1].innerHTML, /src="https:\/\/example.test\/published\/Linear%20Regression\/plot.png"/);
  assert.ok(sections[2].innerHTML.includes(`href="${deployment.sourceRoot}BT2101/BT2101%20Midterms%20(L1-6).pdf#page=1"`));
  assert.equal(fetched[0], deployment.dataset.repoRootUrl ? 'https://example.test/repo/published/Model/concept.md' : 'https://example.test/knowledge_base/refined/Model/concept.md');
});
