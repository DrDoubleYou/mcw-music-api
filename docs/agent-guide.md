# MCW Music API: agent quickstart

Base URL: https://api.matthewcwright.com/api/v1
OpenAPI: https://api.matthewcwright.com/developers/openapi.json
Account and keys: https://api.matthewcwright.com/developers/

## Connect once

The person signs in with an email link, confirms sign-in, and creates an API key.
They save it as MCW_API_KEY in the calling tool's secret settings or environment.
Ask them to do this if the secret is missing. Never ask for a password, email
sign-in token, browser session cookie, or for the key to be pasted into chat.
For an MCP-compatible AI app, add https://api.matthewcwright.com/mcp as a remote
Streamable HTTP server using OAuth. The app opens the website for sign-in and
explicit approval. Do not copy the account API key into OAuth settings.

Available MCP tools: search_tracks, get_track, list_collections,
get_capabilities, get_usage. search_tracks accepts the same filters as REST and
returns the same metadata, download links and credits in structuredContent.
GET /capabilities and GET /usage provide discovery and account usage over REST.

OAuth uses S256 PKCE and the resource https://api.matthewcwright.com/mcp. Request
music:read, plus offline_access for refresh access. Access tokens last 15 minutes;
connections expire after 30 days. The service supports client metadata documents
and dynamic client registration. Use discovery metadata rather than hardcoding
token endpoints. Disconnect an app from the developer account page to immediately
block its access. Token credentials are audience-bound to MCP; REST uses API keys.
MCP tool calls share the REST account quota; initialization and tool discovery do
not count. Tool errors have isError=true and a JSON error with a code, message,
and retry_after_seconds when rate limited. Respect that delay. A 401 from MCP
means reconnect through the client's OAuth flow. No email or API keys are exposed
by the MCP tools.

Send `Authorization: Bearer <MCW_API_KEY>` only to this API over HTTPS. Do not
include keys in URLs, logs, prompts, generated source code, or browser localStorage.
Do not embed a key in a publicly distributed browser application. Use a server-side
integration or a tool's secure credential handling. Every API request needs a key;
public documentation and existing public music downloads do not.

## Find a track

GET /tracks supports q, mood, instrument, collection, min_duration, max_duration,
min_bpm, max_bpm, limit, and offset. Duration is in seconds, tempo in BPM.

- q searches title, description, moods, and keywords; every word must match.
- mood matches one exact tag, case-insensitively. Read moods from track responses.
- instrument is piano or guitar.
- collection is relaxation, sleep, or stories; GET /collections lists their counts.
- Collections use artist metadata matching, not an audio-analysis model.
- limit defaults to 20, maximum 100. offset defaults to 0.
- Tracks are ordered by stable track ID. Follow pagination.next_offset until null.
- Unknown or repeated parameters, negative values, and inverted ranges return 400.
- A search with no matches returns data: [] and total: 0. Broaden filters if needed.

Example, after the key is stored in the environment:

```sh
curl --fail-with-body --get 'https://api.matthewcwright.com/api/v1/tracks' \
  --header "Authorization: Bearer $MCW_API_KEY" \
  --data-urlencode 'collection=relaxation' \
  --data-urlencode 'min_duration=60' \
  --data-urlencode 'limit=5'
```

GET /tracks/{id} returns { "data": <track> }. Search returns
{ "data": [<track>], "pagination": { "total": 181, "limit": 5, "offset": 0,
"next_offset": 5 } }; this total is illustrative and changes with the catalog.
The OpenAPI document defines every response field.

## Download and credit

Each track includes preview_url, download_url, duration_seconds, moods,
instrument, audio_features, license, attribution, attribution_instructions,
and source_url. The download is an MP3; it is not a video-rendering endpoint.

Fetch the returned download_url with a separate, unauthenticated request.
Never forward the API Authorization header to the media host, including redirects.
Do not guess filenames or construct download URLs from titles.
Save attribution, license, source_url, and track ID alongside the downloaded file.
Include the supplied credit in the published project's description or credits;
when editing, fading, trimming, or looping the music, add a Changes line recording
what actually changed. The API does not grant a no-attribution license.

Tempo comes from the artist catalog. Valence, energy, and danceability are null
until analyzed. Do not invent scores or claim beat/scene matching was analyzed.
Use the person's editing tools for fades, looping, mixing, or video rendering.
Do not claim the API performed those operations. Ask for the desired mood and
length if the user's project does not specify them.

## Limits, errors, and retries

Limits are per account, shared across old and replacement keys: 60 requests per
UTC-aligned minute and 1,000 per UTC day. Valid authenticated requests with bad
parameters or missing track IDs also consume quota. Audio downloads are separate
from API-request counts. Limits are fixed windows, not billing guarantees.

Successful authenticated responses include X-RateLimit-Limit,
X-RateLimit-Remaining, X-RateLimit-Reset (Unix seconds), X-DailyLimit-Limit,
and X-DailyLimit-Remaining. 429 responses include Retry-After in seconds.

Errors use { "error": { "code": "...", "message": "..." } } and may include
error.retry_after_seconds. Handle them as follows:

- 400: fix parameters; don't retry an unchanged request.
- 401: credential is missing, invalid, or revoked; ask the owner to configure it.
- 404: search for an available track ID.
- 405: use GET (or OPTIONS for a browser preflight).
- 429: wait for Retry-After before retrying. Don't create accounts or rotate keys
  to evade limits.
- 503: bounded retries with exponential backoff, honoring Retry-After when present.

Cache track metadata within your workflow to reduce repeated requests. Protect
cached credentials separately. On key replacement or revocation, the old key
stops working immediately. The service exposes no account/billing mutations to
API keys; key management requires a signed-in website session.
