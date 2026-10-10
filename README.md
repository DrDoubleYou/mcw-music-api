# MCW Music API

**Free REST API and MCP server for original, human-composed instrumental music by Matthew C. Wright.** Search for a track, preview it, download its MP3, and keep the credit with your project.

[Website](https://api.matthewcwright.com/) · [Account / API key](https://api.matthewcwright.com/developers/) · [Documentation](https://api.matthewcwright.com/docs/) · [Browse the music](https://matthewcwright.com/music/royalty-free/)

- **181 original tracks at launch:** piano and guitar, composed without AI.
- **Royalty-free music under CC BY 4.0:** usable in videos, films, podcasts, games, and commercial projects with attribution.
- **Direct MP3 downloads:** every track response includes audio links, license information, and a ready-to-use credit.
- **AI-friendly MCP:** connect a compatible assistant through browser sign-in and OAuth approval.
- **Free beta access:** 60 requests per minute and 1,000 per UTC day per account. REST and MCP share that allowance. Audio downloads do not count as API requests.

This repository contains integration examples and public documentation for the hosted service. The current track count is available through `/capabilities`.

## Search, select, and download in minutes

1. [Sign in and create an API key](https://api.matthewcwright.com/developers/).
2. Save it in your terminal environment or your tool's secret settings as `MCW_API_KEY`. Do not paste it into an AI conversation.
3. Clone this repo and run the example for your language:

```sh
git clone https://github.com/DrDoubleYou/mcw-music-api.git
cd mcw-music-api
python3 examples/download_music.py
```

The Python example uses only the standard library. It lists five relaxing tracks, asks which one you want, and saves the MP3, credit, and track metadata to `music/`.

**Other options:**

```sh
node examples/download_music.mjs    # Node.js 22+; no packages to install
bash examples/download_music.sh    # cURL + jq; Bash / zsh terminal
```

[Quick start, environment setup, and search options →](docs/quickstart.md)

## Connect your AI through MCP

Add this remote MCP server in an assistant that supports **Streamable HTTP and OAuth**:

```text
https://api.matthewcwright.com/mcp
```

Complete sign-in and approve access in your browser. MCP connections use OAuth; you do not need to paste an API key into the MCP connection.

Example prompt:

> Find three relaxing piano tracks for my 45-second Short. Show me the previews, download my choice, and save the music credit beside my video.

[Connect MCP →](docs/mcp.md) · [Instructions for AI agents →](docs/agent-guide.md) · [Copy-ready AI prompt →](docs/copy-for-your-ai.txt)

If your assistant cannot connect to remote MCP, give it the [agent guide](docs/agent-guide.md) and configure `MCW_API_KEY` in its secure settings so it can use REST.

## REST API

Base URL: `https://api.matthewcwright.com/api/v1`

```sh
curl --fail-with-body --get 'https://api.matthewcwright.com/api/v1/tracks' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}" \
  --data-urlencode 'collection=relaxation' \
  --data-urlencode 'limit=2'
```

| Endpoint | Purpose | MCP tool |
| --- | --- | --- |
| `GET /tracks` | Search by text, mood, instrument, collection, duration, and tempo | `search_tracks` |
| `GET /tracks/{id}` | Get one track's audio links, metadata, license, and credit | `get_track` |
| `GET /collections` | List collections and their track counts | `list_collections` |
| `GET /capabilities` | Discover filters, moods, instruments, tools, and catalog size | `get_capabilities` |
| `GET /usage` | Check your account's daily request usage and limits | `get_usage` |

[Example request and response for every endpoint →](docs/api.md) · [OpenAPI specification →](openapi.json)

## Creator workflows

- [Add relaxing music to a folder of Shorts](docs/workflows.md#add-music-to-a-folder-of-shorts).
- [Choose and trim a podcast intro](docs/workflows.md#make-a-podcast-intro).
- [Add music after each daily video is produced](docs/workflows.md#daily-video-pipeline).

The API supplies music and credits. Your editing tools mix or trim the audio, and your connected publishing tools upload the finished work.

## Credit Matthew C. Wright

**You must credit Matthew C. Wright when using the music under CC BY 4.0.** Every track includes an `attribution` field. Include that credit in your video description, podcast notes, game credits, or other published project; describe edits such as trimming, fading, or looping.

No-attribution licenses are available for **$49 per song** through [Matthew C. Wright's music website](https://matthewcwright.com/music/royalty-free/).

The repository's example code is MIT-licensed. That license does **not** apply to the music. See [music licensing](MUSIC-LICENSE.md) and [the code license](LICENSE).

## Help and contributions

[Report a bug](https://github.com/DrDoubleYou/mcw-music-api/issues/new?template=bug_report.yml), [request a feature](https://github.com/DrDoubleYou/mcw-music-api/issues/new?template=feature_request.yml), or [contact Matthew](https://api.matthewcwright.com/contact/).

Improvements to examples and documentation are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Never include API keys, sign-in links, personal account details, or tokens in an issue or pull request.
