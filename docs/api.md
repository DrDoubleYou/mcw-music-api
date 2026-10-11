# REST API requests and responses

Base URL: `https://api.matthewcwright.com/api/v1`. Every endpoint uses GET with an API key in the Authorization header. Set `MCW_API_KEY` as shown in [quick start](quickstart.md).

Responses below were generated from the service catalog on October 9, 2026. Catalog counts and music metadata can change. Account usage numbers are illustrative. [Live documentation](https://api.matthewcwright.com/docs/) · [OpenAPI specification](../openapi.json).

## GET /tracks

Search music for a project.



### Example request

```sh
curl --fail-with-body 'https://api.matthewcwright.com/api/v1/tracks?collection=relaxation&limit=2' \
  --user-agent 'mcw-music-api-example/1.0' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}"
```

### Example response: 200 OK

```json
{
  "data": [
    {
      "id": "000009-leaves-in-the-morning-light",
      "title": "Leaves in the Morning Light",
      "artist": "Matthew C. Wright",
      "description": "Morning sunshine leaks in through the windows or onto the leaves, leaving you with a sense of peace and calm.",
      "instrument": "piano",
      "duration_seconds": 267,
      "moods": [
        "peaceful",
        "luminous",
        "airy"
      ],
      "keywords": [
        "tranquil",
        "bittersweet",
        "hopeful",
        "soothing"
      ],
      "audio_features": {
        "tempo_bpm": 60,
        "tempo_source": "artist catalog",
        "valence": null,
        "energy": null,
        "danceability": null,
        "analysis_status": "not analyzed"
      },
      "preview_url": "https://media.matthewcwright.com/audio/previews/leaves_in_the_morning_light_preview.mp3",
      "download_url": "https://media.matthewcwright.com/audio/downloads/leaves_in_the_morning_light_download.mp3",
      "audio_format": "mp3",
      "source_url": "https://matthewcwright.com/music/royalty-free/000009-leaves-in-the-morning-light/",
      "license": {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution_required": true
      },
      "attribution": "Music: \"Leaves in the Morning Light\" by Matthew C. Wright\nLicensed under Creative Commons Attribution 4.0\nhttps://creativecommons.org/licenses/by/4.0/\nSource: https://matthewcwright.com/music/royalty-free/000009-leaves-in-the-morning-light/",
      "attribution_instructions": "Include the attribution with your project. If you edit, fade, trim, or loop the audio, add a Changes line describing those edits."
    },
    {
      "id": "000062-birdwatching",
      "title": "Birdwatching",
      "artist": "Matthew C. Wright",
      "description": "Birds fly by as you watch calmly from the park bench.",
      "instrument": "piano",
      "duration_seconds": 221,
      "moods": [
        "calm",
        "natural",
        "fluttering"
      ],
      "keywords": [
        "surprising",
        "nature",
        "longing"
      ],
      "audio_features": {
        "tempo_bpm": 39,
        "tempo_source": "artist catalog",
        "valence": null,
        "energy": null,
        "danceability": null,
        "analysis_status": "not analyzed"
      },
      "preview_url": "https://media.matthewcwright.com/audio/previews/birdwatching_preview.mp3",
      "download_url": "https://media.matthewcwright.com/audio/downloads/birdwatching_download.mp3",
      "audio_format": "mp3",
      "source_url": "https://matthewcwright.com/music/royalty-free/000062-birdwatching/",
      "license": {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution_required": true
      },
      "attribution": "Music: \"Birdwatching\" by Matthew C. Wright\nLicensed under Creative Commons Attribution 4.0\nhttps://creativecommons.org/licenses/by/4.0/\nSource: https://matthewcwright.com/music/royalty-free/000062-birdwatching/",
      "attribution_instructions": "Include the attribution with your project. If you edit, fade, trim, or loop the audio, add a Changes line describing those edits."
    }
  ],
  "pagination": {
    "total": 103,
    "limit": 2,
    "offset": 0,
    "next_offset": 2
  }
}
```

## GET /tracks/{id}

Get audio links, license, and attribution for one track.



### Example request

```sh
curl --fail-with-body 'https://api.matthewcwright.com/api/v1/tracks/000073-nebula' \
  --user-agent 'mcw-music-api-example/1.0' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}"
```

### Example response: 200 OK

```json
{
  "data": {
    "id": "000073-nebula",
    "title": "Nebula",
    "artist": "Matthew C. Wright",
    "description": "A slow, calming piano track for relaxation.",
    "instrument": "piano",
    "duration_seconds": 240,
    "moods": [
      "calming",
      "soothing",
      "relaxing"
    ],
    "keywords": [
      "sleepy",
      "calming",
      "relaxing",
      "peaceful",
      "soothing"
    ],
    "audio_features": {
      "tempo_bpm": 53,
      "tempo_source": "artist catalog",
      "valence": null,
      "energy": null,
      "danceability": null,
      "analysis_status": "not analyzed"
    },
    "preview_url": "https://media.matthewcwright.com/audio/previews/nebula_preview.mp3",
    "download_url": "https://media.matthewcwright.com/audio/downloads/nebula_download.mp3",
    "audio_format": "mp3",
    "source_url": "https://matthewcwright.com/music/royalty-free/000073-nebula/",
    "license": {
      "id": "CC-BY-4.0",
      "url": "https://creativecommons.org/licenses/by/4.0/",
      "attribution_required": true
    },
    "attribution": "Music: \"Nebula\" by Matthew C. Wright\nLicensed under Creative Commons Attribution 4.0\nhttps://creativecommons.org/licenses/by/4.0/\nSource: https://matthewcwright.com/music/royalty-free/000073-nebula/",
    "attribution_instructions": "Include the attribution with your project. If you edit, fade, trim, or loop the audio, add a Changes line describing those edits."
  }
}
```

## GET /collections

List available music collections.



### Example request

```sh
curl --fail-with-body 'https://api.matthewcwright.com/api/v1/collections' \
  --user-agent 'mcw-music-api-example/1.0' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}"
```

### Example response: 200 OK

```json
{
  "data": [
    {
      "id": "relaxation",
      "title": "Relaxation & focus",
      "description": "Unhurried music with calm, gentle, or peaceful descriptions.",
      "track_count": 103
    },
    {
      "id": "sleep",
      "title": "Sleep & stillness",
      "description": "Unhurried music described as sleepy, soothing, or lullaby-like.",
      "track_count": 101
    },
    {
      "id": "stories",
      "title": "Stories & films",
      "description": "Music with cinematic, emotional, dramatic, or hopeful descriptions.",
      "track_count": 9
    }
  ]
}
```

## GET /capabilities

Discover supported filters, instruments, moods, tools and pagination..



### Example request

```sh
curl --fail-with-body 'https://api.matthewcwright.com/api/v1/capabilities' \
  --user-agent 'mcw-music-api-example/1.0' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}"
```

### Example response: 200 OK

```json
{
  "version": "1",
  "track_count": 181,
  "instruments": [
    "piano",
    "guitar"
  ],
  "moods": [
    "acceptance",
    "affectionate",
    "affirming",
    "airy",
    "ambient",
    "anticipation",
    "anxious",
    "artisanal",
    "aspiration",
    "aspiring",
    "autumn",
    "awe",
    "beautiful",
    "beauty",
    "becoming",
    "beginning",
    "bittersweet",
    "bobbing",
    "bright",
    "brisk",
    "call and response",
    "calm",
    "calming",
    "care",
    "carefree",
    "cheerful",
    "chilly",
    "class",
    "cloudy",
    "colorful",
    "comfort",
    "comforting",
    "concluding",
    "contemplative",
    "content",
    "cozy",
    "cunning",
    "cute",
    "dainty",
    "defeat",
    "delicate",
    "depressed",
    "depression",
    "descending",
    "detached",
    "disappointed",
    "dormant",
    "dreamlike",
    "dreamy",
    "drifting",
    "earnest",
    "earthy",
    "elderly",
    "elegant",
    "empty",
    "enchanting",
    "ending",
    "endings",
    "energetic",
    "eureka",
    "exciting",
    "expansive",
    "exuberant",
    "falling",
    "fated",
    "flashing",
    "floating",
    "floaty",
    "floral",
    "flowing",
    "fluttering",
    "fondness",
    "foreboding",
    "friendly",
    "frosty",
    "fun",
    "glistening",
    "goodbyes",
    "grand",
    "grounding",
    "guilt",
    "heartfelt",
    "homely",
    "hopeful",
    "icy",
    "inspiration",
    "intense",
    "intrigue",
    "intriguing",
    "inviting",
    "isolated",
    "isolating",
    "isolation",
    "joyful",
    "joyous",
    "lighthearted",
    "liminal",
    "lonely",
    "longing",
    "loss",
    "love",
    "loving",
    "luminous",
    "magical",
    "maternal",
    "measured",
    "meditative",
    "melancholy",
    "mellow",
    "mischievous",
    "morning",
    "moving",
    "moving on",
    "mundane",
    "mystery",
    "mystic",
    "natural",
    "nighttime",
    "nostalgia",
    "nostalgic",
    "optimistic",
    "overcast",
    "overwhelming",
    "pastoral",
    "patience",
    "peaceful",
    "performative",
    "playful",
    "pretty",
    "process",
    "progressive",
    "pulsing",
    "pure",
    "purposeful",
    "quiet",
    "realization",
    "refined",
    "reflection",
    "reflective",
    "regret",
    "regretful",
    "relaxing",
    "reminiscent",
    "remorse",
    "renewal",
    "resigned",
    "resolution",
    "rich",
    "sad",
    "sadness",
    "scenic",
    "sentimental",
    "serene",
    "simple",
    "simplistic",
    "sleepy",
    "slow",
    "slowing",
    "snowy",
    "solemn",
    "solitary",
    "soothing",
    "sorrow",
    "soulful",
    "spacey",
    "spacious",
    "sprightly",
    "stately",
    "sunny",
    "sweet",
    "swirling",
    "tasteful",
    "temporary",
    "tender",
    "thoughtful",
    "tranquil",
    "twinkling",
    "unclear",
    "unsure",
    "vivid",
    "waiting",
    "waltz",
    "warm",
    "warmth",
    "weighty",
    "whimsical",
    "whimsy",
    "wholesome",
    "wisdom",
    "wishful",
    "wishfulness",
    "wistful",
    "woeful",
    "wonder",
    "worried",
    "yearning"
  ],
  "filters": [
    "q",
    "mood",
    "instrument",
    "collection",
    "min_duration",
    "max_duration",
    "min_bpm",
    "max_bpm",
    "limit",
    "offset"
  ],
  "pagination": {
    "default_limit": 20,
    "max_limit": 100
  },
  "tools": [
    "search_tracks",
    "get_track",
    "list_collections",
    "get_capabilities",
    "get_usage"
  ],
  "downloads": "Download download_url without forwarding credentials to the audio host. Save attribution and license with your project.",
  "tempo": "BPM can be null; BPM filters exclude tracks without measured BPM."
}
```

## GET /usage

Read account limits, requests used today, and reset time. This request counts toward usage..

Usage numbers are illustrative. requests_today includes this request; resets_at is the next midnight UTC in Unix seconds.

### Example request

```sh
curl --fail-with-body 'https://api.matthewcwright.com/api/v1/usage' \
  --user-agent 'mcw-music-api-example/1.0' \
  -H "Authorization: Bearer ${MCW_API_KEY:?Set MCW_API_KEY first}"
```

### Example response: 200 OK

```json
{
  "limits": {
    "per_minute": 60,
    "per_day": 1000
  },
  "requests_today": 12,
  "resets_at": 1791590400
}
```

## Search filters

Use these on `GET /tracks`. Unknown or repeated parameters, negative values, or a minimum larger than its maximum return 400.

| Parameter | Meaning |
| --- | --- |
| `q` | Case-insensitive text search. All whitespace-separated terms must appear in title, description, moods, or keywords. |
| `mood` | Exact mood tag, case-insensitive. Read available tags from returned tracks. |
| `instrument` | Instrument filter. Values: `piano`, `guitar`. |
| `collection` | Heuristic collection based on artist metadata. Values: `relaxation`, `sleep`, `stories`. |
| `min_duration` | Minimum duration in seconds. |
| `max_duration` | Maximum duration in seconds. |
| `min_bpm` | Minimum BPM; tracks without BPM are excluded when filtering tempo. |
| `max_bpm` | Maximum BPM. |
| `limit` | Page size. Default: 20. Maximum: 100. |
| `offset` | Zero-based offset. Follow next_offset until null. Default: 0. Maximum: 1000000. |

Duration is in seconds; tempo is in BPM. `q` requires every search word to match the track text. `mood` matches one exact mood tag, case-insensitively. Use `/capabilities` or returned tracks to find available moods. Collections use descriptive artist metadata, not audio analysis.

Search results use stable ID order. Follow `pagination.next_offset` until it is null. No matches return a successful response with `data: []`. BPM can be null; BPM filters exclude tracks without BPM. Energy, valence, and danceability are null until analyzed.

## Downloads and credits

Use the returned `download_url`; do not construct a media filename from the title. Make a separate unauthenticated download request, with no API key, cookies, or OAuth token. Public MP3 downloads do not count toward the API request allowance. Save `attribution`, `license`, `source_url`, and track ID beside the audio, and include the credit when publishing. Add a Changes line for trimming, fading, looping, or mixing.

## Errors and limits

Errors use `{ "error": { "code": "...", "message": "..." } }`; rate-limited errors may include `retry_after_seconds`.

| Status | Action |
| --- | --- |
| 400 | Fix invalid parameters; do not retry the same request. |
| 401 | Configure a valid API key; a replaced or revoked key no longer works. |
| 404 | Search for an available track ID. |
| 405 | Use GET. |
| 429 | Wait for `Retry-After` seconds. |
| 503 | Retry a limited number of times with exponential backoff, respecting `Retry-After`. |

Limits are 60 requests per UTC-aligned minute and 1,000 per UTC day per account, shared across REST, MCP, and key replacements. Valid authenticated requests with bad filters or missing track IDs also consume allowance. Successful authenticated responses expose `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `X-DailyLimit-Limit`, and `X-DailyLimit-Remaining`. Reset timestamps use Unix seconds. Cache metadata within your workflow to reduce repeated requests.
