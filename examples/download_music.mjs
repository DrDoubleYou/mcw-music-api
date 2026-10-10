// Search, select, and download MCW music. Node.js 22+; no dependencies.
import { mkdir, writeFile } from "node:fs/promises";
import { createInterface } from "node:readline/promises";
import { stdin, stdout } from "node:process";
import { join } from "node:path";

const key = process.env.MCW_API_KEY;
if (!key) {
  console.error("Set MCW_API_KEY first: https://api.matthewcwright.com/developers/");
  process.exit(1);
}

function safeUrl(value) {
  const url = new URL(value);
  const local = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
  if (url.username || url.password || (url.protocol !== "https:" && !(url.protocol === "http:" && local))) {
    throw new Error("Use an HTTPS URL without credentials (HTTP is allowed only for local tests).");
  }
  return url;
}

async function main() {
  const base = safeUrl(process.env.MCW_API_BASE_URL ?? "https://api.matthewcwright.com/api/v1");
  if (base.search || base.hash) throw new Error("API base must not have a query or fragment.");
  const url = new URL(base.toString().replace(/\/$/, "") + "/tracks");
  url.search = new URLSearchParams({ collection: "relaxation", limit: "5" }).toString();
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${key}` },
    redirect: "error", // Never send authenticated requests to a redirect target.
    signal: AbortSignal.timeout(30_000),
  });
  if (!response.ok) {
    const delay = response.headers.get("Retry-After");
    const wait = response.status === 429 && delay ? ` Wait ${delay} seconds before retrying.` : "";
    throw new Error(`API returned HTTP ${response.status}.${wait}`);
  }
  const { data: tracks } = await response.json();
  if (!tracks.length) throw new Error("No tracks found. Try fewer filters or another collection.");
  tracks.forEach((track, index) => {
    console.log(`${index + 1}. ${track.title} (${track.duration_seconds} seconds)`);
    console.log(`   Preview: ${track.preview_url}`);
  });
  const terminal = createInterface({ input: stdin, output: stdout });
  let answer;
  try {
    answer = (await terminal.question("Download which track? Enter its number: ")).trim();
  } finally {
    terminal.close();
  }
  if (!/^\d+$/.test(answer) || Number(answer) < 1 || Number(answer) > tracks.length) {
    throw new Error("Run again and choose a number from the list.");
  }
  const track = tracks[Number(answer) - 1];
  if (!/^[A-Za-z0-9_-]+$/.test(track.id)) throw new Error("Track ID is not a safe filename.");
  const audio = await fetch(safeUrl(track.download_url), {
    // This independent request deliberately has no Authorization header.
    signal: AbortSignal.timeout(60_000),
  });
  if (!audio.ok) throw new Error(`Download returned HTTP ${audio.status}.`);
  await mkdir("music", { recursive: true });
  const name = join("music", track.id);
  await writeFile(`${name}.mp3`, Buffer.from(await audio.arrayBuffer()), { flag: "wx" });
  await writeFile(`${name}-credit.txt`, track.attribution + "\n", { flag: "wx" });
  await writeFile(`${name}.json`, JSON.stringify(track, null, 2) + "\n", { flag: "wx" });
  console.log(`Downloaded: ${name}.mp3\nMusic credit: ${name}-credit.txt\nTrack metadata: ${name}.json`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
