"""Search, select, and download MCW music. Python 3.10+; no dependencies."""
import argparse
import json
import os
import re
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, quote
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

API_BASE = "https://api.matthewcwright.com/api/v1"


class NoApiRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # An authenticated API request must not send its key to a redirect target.
        return None


def safe_url(value):
    parsed = urlsplit(value)
    local = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    if parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("Expected an absolute URL without credentials.")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and local):
        raise ValueError("Use HTTPS (HTTP is allowed only for local tests).")
    return value


def api_get(path, params=None):
    key = os.environ.get("MCW_API_KEY", "")
    if not key:
        raise ValueError("Set MCW_API_KEY first: https://api.matthewcwright.com/developers/")
    base = safe_url(os.environ.get("MCW_API_BASE_URL", API_BASE).rstrip("/"))
    if urlsplit(base).query or urlsplit(base).fragment:
        raise ValueError("The API base URL must not contain a query or fragment.")
    suffix = "?" + urlencode(params) if params else ""
    req = Request(base + path + suffix, headers={"Authorization": "Bearer " + key})
    try:
        with build_opener(NoApiRedirects()).open(req, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        delay = error.headers.get("Retry-After")
        wait = f" Wait {delay} seconds before retrying." if error.code == 429 and delay else ""
        raise ValueError(f"API returned HTTP {error.code}.{wait}") from None


def save_track(track, folder):
    track_id = track["id"]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", track_id):
        raise ValueError("Track ID is not a safe filename.")
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    audio = folder / f"{track_id}.mp3"
    credit = folder / f"{track_id}-credit.txt"
    metadata = folder / f"{track_id}.json"
    if any(path.exists() for path in (audio, credit, metadata)):
        raise ValueError("Output already exists. Choose another output directory or track.")
    # Separate, unauthenticated request: no Authorization header goes to media.
    with urlopen(safe_url(track["download_url"]), timeout=60) as response:
        with audio.open("xb") as output:
            shutil.copyfileobj(response, output)
    credit.write_text(track["attribution"] + "\n", encoding="utf-8")
    metadata.write_text(json.dumps(track, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return audio, credit, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", choices=["relaxation", "sleep", "stories"])
    parser.add_argument("--query", help="Search words, e.g. 'gentle piano'")
    parser.add_argument("--min-duration", type=float, default=0, help="Seconds")
    parser.add_argument("--track-id", help="Download a particular track ID instead of searching")
    parser.add_argument("--first", action="store_true", help="Automatically select the first result")
    parser.add_argument("--output", default="music", help="Output directory (default: music)")
    args = parser.parse_args()
    if args.min_duration < 0:
        parser.error("--min-duration must be nonnegative")
    if args.track_id:
        track = api_get("/tracks/" + quote(args.track_id, safe=""))["data"]
    else:
        params = {"limit": 5, "min_duration": args.min_duration}
        if args.collection:
            params["collection"] = args.collection
        elif not args.query:
            params["collection"] = "relaxation"
        if args.query:
            params["q"] = args.query
        tracks = api_get("/tracks", params)["data"]
        if not tracks:
            raise ValueError("No tracks found. Try fewer filters or another collection.")
        for number, item in enumerate(tracks, start=1):
            print(f"{number}. {item['title']} ({item['duration_seconds']} seconds)")
            print(f"   Preview: {item['preview_url']}")
        choice = "1" if args.first else input("Download which track? Enter its number: ").strip()
        if not choice.isdecimal() or not 1 <= int(choice) <= len(tracks):
            raise ValueError("Run again and choose a number from the list.")
        track = tracks[int(choice) - 1]
    audio, credit, metadata = save_track(track, args.output)
    print(f"Downloaded: {audio}\nMusic credit: {credit}\nTrack metadata: {metadata}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, URLError, OSError, EOFError) as error:
        raise SystemExit(str(error)) from None
