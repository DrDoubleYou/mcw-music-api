# Quick start: search, select, download

## 1. Get your API key

Open [Account / API key](https://api.matthewcwright.com/developers/), sign in using the email link, and create a key. Save it in your terminal environment or your tool's secret settings.

macOS / Linux, Bash or zsh:

```sh
export MCW_API_KEY='YOUR_API_KEY'
```

Windows PowerShell:

```powershell
$env:MCW_API_KEY = 'YOUR_API_KEY'
```

Replace the placeholder locally. Do not commit a real key, put it in a URL, or paste it into chat. The `.env.example` file documents the setting; these scripts read the process environment and do not load `.env` automatically.

## 2. Choose a language

Clone the repository, then run one of these from its root:

```sh
python3 examples/download_music.py
```

Python 3.10+ works without extra packages. On Windows you can use `py` in place of `python3`.

```sh
node examples/download_music.mjs
```

Node.js 22+ works without extra packages.

```sh
bash examples/download_music.sh
```

The shell example requires Bash, cURL with `--fail-with-body` support, and [jq](https://jqlang.org/download/).

## 3. Select and download

Each example searches for five relaxing tracks, displays their titles and lengths, and asks you to enter a number. To preview a track first, open its displayed preview link.

The example saves these files in `music/`:

- `TRACK_ID.mp3` — downloaded music.
- `TRACK_ID-credit.txt` — the supplied attribution.
- `TRACK_ID.json` — track metadata, source URL, and license information.

Downloads make a separate request without the API key. Use the credit when publishing your project.

## Change the search

The Python example supports filters and a different output directory:

```sh
python3 examples/download_music.py --query 'gentle piano' --output podcast-music
python3 examples/download_music.py --collection sleep
python3 examples/download_music.py --collection relaxation --min-duration 60
```

For an unattended workflow, `--first` selects the first matching result:

```sh
python3 examples/download_music.py --collection relaxation --min-duration 60 --first
```

Search order is stable track ID order, not a popularity or recommendation ranking. For a specific track ID, use:

```sh
python3 examples/download_music.py --track-id 000073-nebula
```

JavaScript and shell examples use the default relaxation search. Edit their search parameters to use [other filters](api.md#search-filters).

## Limits and errors

Free beta access allows 60 requests per UTC-aligned minute and 1,000 per UTC day, shared by REST and MCP for the same account. A download does not use the API allowance.

The examples stop on errors rather than repeatedly retrying. On HTTP 429, wait for the response's `Retry-After` delay. On 401, check the key in your environment. A search with no results is successful; try fewer filters. [Full error handling →](api.md#errors-and-limits)

## Keep the documentation current

The checked-in OpenAPI file and response examples are a snapshot from October 9, 2026. The [live documentation](https://api.matthewcwright.com/docs/) and [live OpenAPI file](https://api.matthewcwright.com/developers/openapi.json) are the current service contract. Counts can change as music is added.
