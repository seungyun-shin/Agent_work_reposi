// 상품 원고(Markdown) → 판매용 PDF.
// 원고는 공개 저장소에 올리지 않으므로 경로를 인자로 받는다.
//   node product/build_pdf.mjs <kit.md> <out.pdf>
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node22/lib/node_modules/playwright");

const [src, out] = process.argv.slice(2);
if (!src || !out) {
  console.error("usage: node product/build_pdf.mjs <kit.md> <out.pdf>");
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(join(here, "pdf.css"), "utf8");
const body = execFileSync("pandoc", [src, "-f", "gfm+yaml_metadata_block", "-t", "html5"], { encoding: "utf8" });
const meta = Object.fromEntries(
  (readFileSync(src, "utf8").match(/^---\n([\s\S]*?)\n---/)?.[1] || "")
    .split("\n").map((l) => l.match(/^(\w+):\s*"?(.*?)"?$/)).filter(Boolean).map((m) => [m[1], m[2]])
);

const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap">
<style>${css}</style></head><body>
<section class="cover"><div class="badge">${meta.version || ""}</div>
<h1>${meta.title || ""}</h1><p class="sub">${meta.subtitle || ""}</p></section>
${body}</body></html>`;

const tmp = join(mkdtempSync(join(tmpdir(), "kit-")), "kit.html");
writeFileSync(tmp, html);
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + tmp, { waitUntil: "networkidle" });
await page.pdf({
  path: out, printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#999"><span class="pageNumber"></span></div>',
});
await browser.close();
console.log("wrote", out);
