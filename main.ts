// news-image-20261120 — build artifact emitter.
// Copies the rendered 1024x1024 news front page into the make.fun output dir.
// Run:  MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE: string = dirname(fileURLToPath(import.meta.url));
const ARTIFACT: string = join(HERE, "entry.png");
const MAX_BYTES: number = 1024 * 1024;

function fail(msg: string): never {
  console.error(`[news-image-20261120] ${msg}`);
  process.exit(1);
}

if (!existsSync(ARTIFACT)) {
  fail(`missing artwork: ${ARTIFACT} (run "python3 draw_news.py" first)`);
}

const before = statSync(ARTIFACT);
if (before.size > MAX_BYTES) {
  fail(`entry.png is ${before.size} bytes, over the 1 MiB limit`);
}

const outDir: string = resolve(HERE, process.env.MAKEFUN_OUTPUT_DIR ?? "out");
mkdirSync(outDir, { recursive: true });

const dest: string = join(outDir, "entry.png");
copyFileSync(ARTIFACT, dest);

const after = statSync(dest);
if (after.size !== before.size) {
  fail(`copy mismatch: ${before.size} bytes -> ${after.size} bytes`);
}

console.log(
  `[news-image-20261120] wrote ${dest} (${after.size} bytes, 1024x1024)`
);
