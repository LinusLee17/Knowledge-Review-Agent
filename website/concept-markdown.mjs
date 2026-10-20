// Supported concept-page Markdown only, not a full CommonMark implementation.
export function escapeHtml(value) {
  return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

export function parseFrontMatter(markdown) {
  const lines = markdown.split(/\r?\n/);
  const end = lines.indexOf('---', 1);
  if (lines[0] !== '---' || end < 0) return { meta: {}, body: markdown };
  const meta = {};
  for (const line of lines.slice(1, end)) {
    const match = line.match(/^([A-Za-z0-9_ -]+):\s*(.*)$/);
    if (match) meta[match[1].trim()] = match[2].trim().replace(/^"(.*)"$/, '$1');
  }
  return { meta, body: lines.slice(end + 1).join('\n') };
}

function openingFence(line) {
  const match = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
  if (!match || (match[1][0] === '`' && match[2].includes('`'))) return null;
  return match[1];
}

function closesFence(line, fence) {
  const match = line.match(/^ {0,3}(`+|~+)\s*$/);
  return match && match[1][0] === fence[0] && match[1].length >= fence.length;
}

export function splitSections(markdown) {
  const sections = [], preamble = [];
  let title = '', current = preamble, fence = null, inMath = false;
  for (const line of markdown.split(/\r?\n/)) {
    if (fence) {
      current.push(line);
      if (closesFence(line, fence)) fence = null;
      continue;
    }
    if (inMath) {
      current.push(line);
      if (line.trim() === '$$') inMath = false;
      continue;
    }
    fence = openingFence(line);
    if (fence || line.trim() === '$$') {
      inMath = !fence;
      current.push(line);
      continue;
    }
    const heading = line.match(/^ {0,3}(#{1,2})\s+(.*)$/);
    if (heading?.[1] === '#' && !title) {
      title = heading[2].trim();
    } else if (heading?.[1] === '##') {
      const section = { title: heading[2].trim(), lines: [] };
      sections.push(section);
      current = section.lines;
    } else current.push(line);
  }
  return { title, preamble, sections };
}

function decodeEntities(text) {
  const named = { amp: '&', quot: '"', apos: "'", lt: '<', gt: '>', colon: ':', Tab: '\t', NewLine: '\n' };
  return text.replace(/&(#x[0-9a-f]+|#\d+|[A-Za-z]+);/gi, (raw, name) => {
    if (!name.startsWith('#')) return named[name] ?? raw;
    const code = name[1].toLowerCase() === 'x' ? parseInt(name.slice(2), 16) : Number(name.slice(1));
    return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : '\ufffd';
  });
}

function unescapeMarkdown(text) {
  return decodeEntities(text.replace(/\\([!"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~\\])/g, '$1'));
}

function safeUrl(destination, baseUrl, image, options) {
  const raw = unescapeMarkdown(destination);
  if (/[\u0000-\u001f\u007f]/.test(raw)) return null;
  try {
    // Shipped provenance links predate Markdown-relative asset resolution.
    const legacyPrefix = '../data/raw/';
    const legacySource = !image && options.legacySourceRootUrl && raw.startsWith(legacyPrefix);
    const url = legacySource
      ? new URL(`./${raw.slice(legacyPrefix.length)}`, options.legacySourceRootUrl)
      : new URL(raw, baseUrl);
    const allowed = image ? ['https:', 'http:'] : ['https:', 'http:', 'mailto:'];
    return allowed.includes(url.protocol) ? url.href : null;
  } catch { return null; }
}

// Find delimiters without consuming escaped punctuation or nested parentheses.
function closingDelimiter(text, start, open, close) {
  let depth = 1;
  for (let i = start; i < text.length; i++) {
    if (text[i] === '\\') { i++; continue; }
    if (text[i] === open) depth++;
    if (text[i] === close) {
      depth--;
      if (!depth) return i;
    }
  }
  return -1;
}

function linkAt(text, start) {
  const image = text.startsWith('![', start);
  const labelStart = start + (image ? 2 : 1);
  const labelEnd = closingDelimiter(text, labelStart, '[', ']');
  if (labelEnd < 0 || text[labelEnd + 1] !== '(') return null;
  let depth = 1, quote = null, angle = false, end = -1;
  for (let i = labelEnd + 2; i < text.length; i++) {
    const char = text[i];
    if (char === '\\') { i++; continue; }
    if (quote) { if (char === quote) quote = null; continue; }
    if (angle) { if (char === '>') angle = false; continue; }
    if (char === '<' && i === labelEnd + 2) { angle = true; continue; }
    if ((char === '"' || char === "'") && /\s/.test(text[i - 1])) { quote = char; continue; }
    if (char === '(') depth++;
    if (char === ')' && --depth === 0) { end = i; break; }
  }
  if (end < 0) return null;
  let destination = text.slice(labelEnd + 2, end).trim(), title = null;
  const titleMatch = destination.match(/\s+(["'])([\s\S]*)\1$/);
  if (titleMatch) {
    title = unescapeMarkdown(titleMatch[2]);
    destination = destination.slice(0, titleMatch.index).trim();
  }
  if (destination.startsWith('<') && destination.endsWith('>')) destination = destination.slice(1, -1);
  return { image, label: text.slice(labelStart, labelEnd), destination, title, end: end + 1 };
}

function protectedSpan(text, start) {
  const rest = text.slice(start);
  const ticks = rest.match(/^`+/)?.[0];
  if (ticks) {
    let end = start + ticks.length;
    while ((end = text.indexOf(ticks, end)) >= 0) {
      if (text[end - 1] !== '`' && text[end + ticks.length] !== '`') {
        return { kind: 'code', body: text.slice(start + ticks.length, end), end: end + ticks.length };
      }
      end += ticks.length;
    }
  }
  const delimiters = rest.startsWith('\\(') ? ['\\(', '\\)'] : rest.startsWith('\\[') ? ['\\[', '\\]']
    : rest.startsWith('$$') ? ['$$', '$$'] : rest.startsWith('$') ? ['$', '$'] : null;
  if (delimiters) {
    let end = start + delimiters[0].length;
    while ((end = text.indexOf(delimiters[1], end)) >= 0) {
      if (text[end - 1] !== '\\') return { kind: 'math', body: text.slice(start, end + delimiters[1].length), end: end + delimiters[1].length };
      end += delimiters[1].length;
    }
  }
  return null;
}

export function inlineMarkdown(text, baseUrl, options = {}, depth = 0, allowLinks = true) {
  text = String(text ?? '');
  if (depth > 20) return escapeHtml(text);
  let html = '';
  for (let i = 0; i < text.length;) {
    const span = protectedSpan(text, i);
    if (span) {
      if (span.kind === 'math') html += escapeHtml(span.body);
      else {
        const code = span.body.trim();
        // Preserve legacy concept pages' backtick-math convention.
        const math = /\\[A-Za-z]+/.test(code) || /[\^_={}\[\]|+\-*/()]/.test(code);
        html += math ? `<span class="inline-math">\\(${escapeHtml(code)}\\)</span>` : `<code>${escapeHtml(code)}</code>`;
      }
      i = span.end;
      continue;
    }
    if (text[i] === '\\' && /[!"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~\\]/.test(text[i + 1] || '')) {
      html += escapeHtml(text[i + 1]); i += 2; continue;
    }
    if (text.startsWith('![', i) || (allowLinks && text[i] === '[')) {
      const link = linkAt(text, i);
      if (link) {
        const url = safeUrl(link.destination, baseUrl, link.image, options);
        const label = inlineMarkdown(link.label, baseUrl, options, depth + 1, false);
        const title = link.title === null ? '' : ` title="${escapeHtml(link.title)}"`;
        if (!url) html += label;
        else if (link.image) html += `<img src="${escapeHtml(url)}" alt="${escapeHtml(unescapeMarkdown(link.label))}"${title}>`;
        else html += `<a href="${escapeHtml(url)}" target="_blank" rel="noreferrer"${title}>${label}</a>`;
        i = link.end;
        continue;
      }
    }
    if (text.startsWith('**', i)) {
      const end = text.indexOf('**', i + 2);
      if (end > i + 2) {
        html += `<strong>${inlineMarkdown(text.slice(i + 2, end), baseUrl, options, depth + 1, allowLinks)}</strong>`;
        i = end + 2; continue;
      }
    }
    const entity = text[i] === '&' && text.slice(i).match(/^&(?:#x[0-9a-f]+|#\d+|[A-Za-z]+);/i);
    if (entity) { html += escapeHtml(decodeEntities(entity[0])); i += entity[0].length; }
    else { html += escapeHtml(text[i]); i++; }
  }
  return html;
}

function renderMathBlock(content) {
  return content.trim() ? `<div class="math-block">\\[\n${escapeHtml(content.trim())}\n\\]</div>` : '';
}

function tableCells(line) {
  const text = line.trim().slice(1, -1), cells = [];
  let cell = '';
  for (let i = 0; i < text.length;) {
    const span = protectedSpan(text, i);
    if (span) { cell += text.slice(i, span.end); i = span.end; continue; }
    if (text[i] === '\\' && text[i + 1]) { cell += text.slice(i, i + 2); i += 2; continue; }
    if (text[i] === '|') { cells.push(cell.trim()); cell = ''; }
    else cell += text[i];
    i++;
  }
  cells.push(cell.trim());
  return cells;
}

export function renderSectionContent(lines, baseUrl, options = {}) {
  const chunks = [];
  let paragraph = [], list = [], ordered = false, table = [], fence = null, code = [], inMath = false, math = [];
  const inline = text => inlineMarkdown(text, baseUrl, options);
  function flushParagraph() {
    if (paragraph.length) chunks.push(`<p>${inline(paragraph.join(' '))}</p>`);
    paragraph = [];
  }
  function flushList() {
    const tag = ordered ? 'ol' : 'ul';
    if (list.length) chunks.push(`<${tag}>${list.map(item => `<li>${inline(item)}</li>`).join('')}</${tag}>`);
    list = [];
  }
  function flushTable() {
    if (table.length) {
      const separator = table.length > 1 && table[1].every(cell => /^:?-{3,}:?$/.test(cell));
      const rows = separator ? table.slice(2) : table.slice(1);
      chunks.push(`<table><thead><tr>${table[0].map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${inline(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table>`);
    }
    table = [];
  }
  function flushBlocks() { flushParagraph(); flushList(); flushTable(); }
  for (const line of lines) {
    const trimmed = line.trim();
    if (fence) {
      if (closesFence(line, fence)) {
        chunks.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
        code = []; fence = null;
      } else code.push(line);
      continue;
    }
    if (inMath) {
      if (trimmed === '$$') { chunks.push(renderMathBlock(math.join('\n'))); math = []; inMath = false; }
      else math.push(line);
      continue;
    }
    fence = openingFence(line);
    if (fence) { flushBlocks(); continue; }
    if (trimmed === '$$') { flushBlocks(); inMath = true; continue; }
    if (trimmed.startsWith('$$') && trimmed.endsWith('$$') && trimmed.length > 4) {
      flushBlocks(); chunks.push(renderMathBlock(trimmed.slice(2, -2))); continue;
    }
    if (!trimmed) { flushBlocks(); continue; }
    const item = trimmed.match(/^(\d+\.|[-*\u2022])\s+(.*)$/);
    if (item) {
      flushParagraph(); flushTable();
      const nextOrdered = /^\d/.test(item[1]);
      if (list.length && nextOrdered !== ordered) flushList();
      ordered = nextOrdered; list.push(item[2]); continue;
    }
    if (/^\|.*\|$/.test(trimmed)) {
      flushParagraph(); flushList(); table.push(tableCells(line)); continue;
    }
    flushList(); flushTable();
    const heading = trimmed.match(/^#{1,6}\s+(.*)$/);
    if (heading) {
      flushParagraph(); chunks.push(`<h3>${inline(heading[1])}</h3>`); continue;
    }
    paragraph.push(trimmed);
  }
  flushBlocks();
  if (fence) chunks.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
  if (inMath) chunks.push(renderMathBlock(math.join('\n')));
  return chunks.join('\n');
}
