# Working with MCW Music API

This is the public documentation and examples repository for the hosted MCW Music API.

## Integrating the service

Read `docs/agent-guide.md` and `openapi.json` before using the API. The canonical live contract is https://api.matthewcwright.com/developers/openapi.json.

- REST base URL: https://api.matthewcwright.com/api/v1.
- MCP server: https://api.matthewcwright.com/mcp, Streamable HTTP with OAuth.
- Account / API key: https://api.matthewcwright.com/developers/.
- Ask about the desired mood and duration when they are missing.
- Prefer remote MCP when the user's client supports it; follow browser sign-in and explicit approval.
- Otherwise use `MCW_API_KEY` from secret settings or the process environment. Never print a key, put it in a URL or source file, or ask for it in chat.
- Send REST credentials only to the configured API origin. Reject API redirects; do not forward credentials to preview or download URLs.
- Search, show choices and previews, then download the user's choice unless they requested automatic selection.
- Save attribution, license, source URL, and track ID with the project. Include the music credit in published output; describe audio edits.
- Follow `Retry-After` / `retry_after_seconds` on 429. Do not rotate keys or accounts to avoid quotas.
- Unknown audio-analysis values are null. Do not invent energy, valence, danceability, or beat/scene matching.
- Editing and uploading happen through separate, authorized user tools.

## Maintaining this repository

Keep examples dependency-light and runnable from the README. Keep the API key in the environment, never commit private service configuration or account data, and distinguish the MIT example-code license from the music's CC BY 4.0 license.

Run `python3 tests/smoke_test.py` before submitting example changes. It uses a local mock API and synthetic media; it needs Python 3.10+, Node.js 22+, cURL, jq, FFmpeg, and ffprobe. No live account or API key is needed.
