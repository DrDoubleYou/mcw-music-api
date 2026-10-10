# Connect the MCW Music MCP server

Use an AI app that supports remote MCP over **Streamable HTTP**, with **OAuth authorization**. Availability and menu names depend on your app, version, and plan; an AI company logo is not a guarantee of MCP support.

1. Open your assistant's MCP / connector settings and add a remote server.
2. Use `https://api.matthewcwright.com/mcp` as the server URL.
3. Choose Streamable HTTP and OAuth if the app asks.
4. Follow the browser flow, sign in to your MCW developer account, and approve the connection.
5. Ask the assistant to find music for your project.

MCP uses its own OAuth connection; do not put your REST API key in its OAuth settings. If the app does not support this connection, configure an API key in its secret settings and use the [REST examples](quickstart.md).

## Tools

| Tool | What it does |
| --- | --- |
| `search_tracks` | Find tracks using text, mood, instrument, collection, duration, and tempo filters |
| `get_track` | Retrieve one track's links, metadata, license, and credit |
| `list_collections` | List music collections and track counts |
| `get_capabilities` | Discover filters, moods, instruments, and catalog size |
| `get_usage` | Check your account's request allowance and daily usage |

The tools return structured JSON. `search_tracks` accepts the same filters as REST. REST and MCP share account limits: 60 requests per UTC-aligned minute and 1,000 per UTC day. Initialization and tool discovery do not count as music-tool calls.

## Prompts to try

> Find three relaxing piano tracks for my 45-second Short. Show me the preview links. Download my choice and save its attribution beside the video.

> For each video in ./shorts, choose a suitable relaxing track, mix it quietly beneath the original audio using my editing tools, and save the music credit beside the output.

> After my ./daily workflow produces a video, select a relaxing song using the MCW MCP. Mix it under the video, then use my existing YouTube uploader and authorized account to publish it with the music credit in the description.

The MCP provides music links and credits. Audio editing, access to local files, and uploading require separate tools and your authorization. It does not provide YouTube upload or video rendering endpoints.

## Connection lifetime and control

Access tokens last 15 minutes. With `offline_access`, an authorized connection can refresh access for up to 30 days. An app can request `music:read` and optional `offline_access`; use the service's OAuth discovery rather than hardcoding token endpoints.

Manage or disconnect connected AI apps on [Account / API key](https://api.matthewcwright.com/developers/). A 401 means the app needs to reconnect. Tool errors set `isError=true`; rate-limit errors include `retry_after_seconds`.

[Detailed agent guide](agent-guide.md) · [Model Context Protocol](https://modelcontextprotocol.io/)
