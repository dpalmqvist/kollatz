// Convert paper/draft.md (a regular Markdown subset) to a publication-styled .docx.
// usage: node md2docx.js in.md out.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType,
  ShadingType, BorderStyle, Footer, PageNumber, LevelFormat, TabStopType,
} = require("docx");

const [, , IN, OUT] = process.argv;
const src = fs.readFileSync(IN, "utf8").split("\n");

const BODY_FONT = process.env.BODY_FONT || "Georgia";
const CODE_FONT = "Consolas";
const BODY_SIZE = 22;          // half-points: 11 pt
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1418;   // A4, 2.5 cm
const TEXT_W = PAGE_W - 2 * MARGIN;

// ---------- inline parsing -> TextRun[] ----------
const SUP_BARE = /^\^([A-Za-zα-ωΑ-Ω0-9∞]+(?:\.[0-9]+)?)/u;
const SUB_BARE = /^_([A-Za-z0-9∞′*α-ωΑ-Ω]+)/u;

function runs(text, base = {}) {
  const out = [];
  let i = 0, buf = "";
  const flush = () => { if (buf) { out.push(new TextRun({ text: buf, font: BODY_FONT, size: BODY_SIZE, ...base })); buf = ""; } };
  const push = (t, extra) => { flush(); out.push(new TextRun({ text: t, font: BODY_FONT, size: BODY_SIZE, ...base, ...extra })); };
  while (i < text.length) {
    const rest = text.slice(i);
    let m;
    if (rest.startsWith("`")) {
      const j = rest.indexOf("`", 1);
      if (j > 0) { push(rest.slice(1, j), { font: CODE_FONT, size: BODY_SIZE - 2 }); i += j + 1; continue; }
    }
    if (rest.startsWith("**")) {
      const j = rest.indexOf("**", 2);
      if (j > 0) { flush(); out.push(...runs(rest.slice(2, j), { ...base, bold: true })); i += j + 2; continue; }
    }
    if (rest.startsWith("*") && !rest.startsWith("**")) {
      const j = rest.indexOf("*", 1);
      if (j > 0 && !/\s/.test(rest[1])) { flush(); out.push(...runs(rest.slice(1, j), { ...base, italics: true })); i += j + 1; continue; }
    }
    if (rest.startsWith("^{")) {
      const j = matchBrace(rest, 1);
      if (j > 0) { push(rest.slice(2, j), { superScript: true }); i += j + 1; continue; }
    }
    if (rest.startsWith("_{")) {
      const j = matchBrace(rest, 1);
      if (j > 0) { push(rest.slice(2, j), { subScript: true }); i += j + 1; continue; }
    }
    if ((m = SUP_BARE.exec(rest)) && i > 0) {
      let t = m[1]; let adv = m[0].length;
      if (t.endsWith(".") ) { t = t.slice(0, -1); adv -= 1; }
      push(t, { superScript: true }); i += adv; continue;
    }
    if ((m = SUB_BARE.exec(rest)) && i > 0 && /[A-Za-zα-ωΑ-Ω)\]̄′]/u.test(text[i - 1])) {
      push(m[1], { subScript: true }); i += m[0].length; continue;
    }
    buf += text[i]; i += 1;
  }
  flush();
  return out;
}

function matchBrace(s, open) {        // s[open] === '{' ; returns index of matching '}'
  let depth = 0;
  for (let j = open; j < s.length; j++) {
    if (s[j] === "{") depth++;
    else if (s[j] === "}") { depth--; if (depth === 0) return j; }
  }
  return -1;
}

// ---------- block parsing ----------
const blocks = [];
let i = 0;
let inRefs = false;
while (i < src.length) {
  const line = src[i];
  if (line.trim() === "") { i++; continue; }
  if (/^#{1,3} /.test(line)) {
    const level = line.match(/^#+/)[0].length;
    const text = line.replace(/^#+ /, "");
    inRefs = /references/i.test(text);
    blocks.push({ type: "h", level, text }); i++; continue;
  }
  if (line.startsWith("|")) {
    const rows = [];
    while (i < src.length && src[i].startsWith("|")) { rows.push(src[i]); i++; }
    const cells = rows.filter(r => !/^\|\s*-+/.test(r))
      .map(r => r.replace(/\\\|/g, "\u0001").replace(/^\||\|$/g, "").split("|").map(c => c.trim().replace(/\u0001/g, "|")));
    blocks.push({ type: "table", rows: cells }); continue;
  }
  if (line.startsWith("- ")) {
    let text = line.slice(2);
    i++;
    while (i < src.length && /^  \S/.test(src[i])) {
      text += " " + src[i].trim(); i++;
    }
    blocks.push({ type: inRefs ? "ref" : "li", text }); continue;
  }
  if (/^  \S/.test(line)) {           // display line
    blocks.push({ type: "display", text: line.trim() }); i++; continue;
  }
  if (line.startsWith("*Draft") && blocks.length <= 1) {   // draft note under the title (may span lines)
    let text = line; i++;
    while (i < src.length && src[i].trim() !== "") { text += " " + src[i].trim(); i++; }
    blocks.push({ type: "note", text: text.replace(/^\*/, "").replace(/\*$/, "") }); continue;
  }
  let text = line.trim(); i++;
  while (i < src.length && src[i].trim() !== "" && !/^(#|\||- |  \S)/.test(src[i])) { text += " " + src[i].trim(); i++; }
  blocks.push({ type: "p", text });
}

// ---------- build document ----------
const children = [];
let titleDone = false;
const H = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };

for (const b of blocks) {
  if (b.type === "h" && b.level === 1 && !titleDone) {
    titleDone = true;
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 240 },
      children: [new TextRun({ text: b.text, font: BODY_FONT, size: 34, bold: true })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: "Daniel Palmqvist", font: BODY_FONT, size: 24 })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
      children: [new TextRun({ text: "October 2026", font: BODY_FONT, size: 22 })] }));
    continue;
  }
  if (b.type === "note") {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, indent: { left: 720, right: 720 },
      children: runs(b.text, { italics: true, size: 19 }) }));
    continue;
  }
  if (b.type === "h") {
    children.push(new Paragraph({ heading: H[b.level], children: runs(b.text, { bold: true, size: b.level === 2 ? 26 : b.level === 3 ? 23 : 28, italics: b.level === 3 }) }));
    continue;
  }
  if (b.type === "p") {
    children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 264 }, children: runs(b.text) }));
    continue;
  }
  if (b.type === "display") {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 160 }, children: runs(b.text) }));
    continue;
  }
  if (b.type === "li") {
    children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, alignment: AlignmentType.JUSTIFIED,
      spacing: { after: 80, line: 264 }, children: runs(b.text) }));
    continue;
  }
  if (b.type === "ref") {
    children.push(new Paragraph({ indent: { left: 567, hanging: 567 }, spacing: { after: 80 }, children: runs(b.text, { size: 20 }) }));
    continue;
  }
  if (b.type === "table") {
    const ncol = Math.max(...b.rows.map(r => r.length));
    const rows = b.rows.map(r => { while (r.length < ncol) r.push(""); return r; });
    // column weight: 75th percentile of body-cell lengths (long one-off cells wrap), at least 5 and 70 % of the header
    const plain = s => s.replace(/[`*^_{}]/g, "");
    const maxlen = Array.from({ length: ncol }, (_, c) => {
      const body = rows.slice(1).map(r => plain(r[c]).length).sort((a, b) => a - b);
      const p75 = body.length ? body[Math.min(body.length - 1, Math.floor(0.75 * body.length))] : 0;
      return Math.max(5, p75 + 3, Math.ceil(0.7 * plain(rows[0][c]).length));
    });
    const total = maxlen.reduce((a, x) => a + x, 0);
    let widths = maxlen.map(l => Math.round(TEXT_W * l / total));
    widths[widths.length - 1] += TEXT_W - widths.reduce((a, x) => a + x, 0);
    const fsize = ncol >= 10 ? 15 : ncol >= 7 ? 17 : 19;
    const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
    const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
    const trows = rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((cell, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: "E8E8E8", color: "auto" } : undefined,
        borders: { top: ri === 0 ? border : none, bottom: ri === 0 || ri === rows.length - 1 ? border : none, left: none, right: none },
        margins: { top: 40, bottom: 40, left: 60, right: 60 },
        children: [new Paragraph({
          alignment: ri === 0 ? AlignmentType.CENTER : (/^[−+]?[0-9.·e^{}−+ ×%…/()]+$/u.test(cell.replace(/[`*]/g, "")) && cell !== "" ? AlignmentType.RIGHT : AlignmentType.LEFT),
          spacing: { after: 0 },
          children: runs(cell, { size: fsize, bold: ri === 0 }),
        })],
      })),
    }));
    children.push(new Table({ rows: trows, width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: widths }));
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    continue;
  }
}

const doc = new Document({
  creator: "Daniel Palmqvist",
  title: blocks.find(b => b.type === "h").text,
  styles: {
    default: { document: { run: { font: BODY_FONT, size: BODY_SIZE } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: BODY_FONT, size: 28, bold: true }, paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: BODY_FONT, size: 26, bold: true }, paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: BODY_FONT, size: 23, bold: true, italics: true }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: BODY_FONT, size: 20 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("wrote", OUT, buf.length, "bytes;", blocks.length, "blocks"); });
