/**
 * Serves dist/bundler-preview after `npm run build` (no extra npm deps).
 * Run `npm run preview` from the repository root.
 */
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.join(__dirname, "..", "..");
const root = path.join(repoRoot, "dist", "bundler-preview");
const port = Number(process.env.PORT || 8765);

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".map": "application/json; charset=utf-8",
};

function safeResolve(urlPath) {
  const rel = urlPath === "/" ? "index.html" : urlPath.replace(/^\//, "");
  const candidate = path.normalize(path.join(root, rel));
  const rootNorm = path.normalize(root + path.sep);
  if (!candidate.startsWith(rootNorm) && candidate !== path.normalize(root)) {
    return null;
  }
  return candidate;
}

const server = http.createServer((req, res) => {
  if (req.method !== "GET") {
    res.writeHead(405);
    res.end();
    return;
  }
  const url = new URL(req.url || "/", `http://${req.headers.host}`);
  const filePath = safeResolve(url.pathname);
  if (!filePath) {
    res.writeHead(403);
    res.end();
    return;
  }
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end("Not found — run npm run build first.");
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { "Content-Type": mime[ext] || "application/octet-stream" });
    res.end(data);
  });
});

server.listen(port, "127.0.0.1", () => {
  process.stderr.write(`Bundler preview at http://127.0.0.1:${port}/\n`);
});
