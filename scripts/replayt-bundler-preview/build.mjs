import * as esbuild from "esbuild";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const previewDir = __dirname;
const repoRoot = path.join(__dirname, "..", "..");
const outdir = path.join(repoRoot, "dist", "bundler-preview");
const entry = path.join(previewDir, "entry.mjs");
const watch = process.argv.includes("--watch");

function copyHtml() {
  fs.mkdirSync(outdir, { recursive: true });
  fs.copyFileSync(
    path.join(previewDir, "index.html"),
    path.join(outdir, "index.html"),
  );
}

const copyHtmlPlugin = {
  name: "copy-html",
  setup(build) {
    build.onEnd((result) => {
      if (result.errors.length === 0) {
        copyHtml();
      }
    });
  },
};

async function main() {
  const ctx = await esbuild.context({
    entryPoints: [entry],
    bundle: true,
    outfile: path.join(outdir, "bundle.iife.js"),
    format: "iife",
    platform: "browser",
    sourcemap: true,
    logLevel: "info",
    plugins: [copyHtmlPlugin],
  });

  await ctx.rebuild();
  if (watch) {
    await ctx.watch();
  } else {
    await ctx.dispose();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
