#!/usr/bin/env bash
# Search, select, and download MCW music. Requires cURL and jq.
set -euo pipefail
user_agent="mcw-music-api-example/1.0"
: "${MCW_API_KEY:?Set MCW_API_KEY first: https://api.matthewcwright.com/developers/}"
command -v jq >/dev/null || { echo 'Install jq first: https://jqlang.org/download/' >&2; exit 1; }
api_base="${MCW_API_BASE_URL:-https://api.matthewcwright.com/api/v1}"
# The override is used by local tests. Production uses the exact MCW API origin.
if [[ "$api_base" != 'https://api.matthewcwright.com/api/v1' && ! "$api_base" =~ ^http://127\.0\.0\.1:[0-9]+/api/v1$ ]]; then
  echo 'Use the MCW API URL or the local test API.' >&2
  exit 1
fi
response_file="$(mktemp)"
headers_file="$(mktemp)"
trap 'rm -f "$response_file" "$headers_file"' EXIT
# No --location: an authenticated API request must never follow a redirect.
status="$(curl --silent --show-error --max-time 30 --get "$api_base/tracks" \
  -H "Authorization: Bearer $MCW_API_KEY" --user-agent "$user_agent" \
  --data-urlencode 'collection=relaxation' --data-urlencode 'limit=5' \
  --dump-header "$headers_file" --output "$response_file" --write-out '%{http_code}')"
if [[ "$status" != 200 ]]; then
  printf 'API returned HTTP %s.\n' "$status" >&2
  if [[ "$status" == 429 ]]; then
    delay="$(awk 'tolower($1) == "retry-after:" {gsub(/\r/, "", $2); print $2}' "$headers_file")"
    printf 'Wait %s seconds before retrying.\n' "${delay:-the Retry-After delay}" >&2
  fi
  exit 1
fi
count="$(jq '.data | length' "$response_file")"
if [[ "$count" -eq 0 ]]; then
  echo 'No tracks found. Try fewer filters or another collection.' >&2
  exit 1
fi
jq -r '.data | to_entries[] | "\(.key + 1). \(.value.title) (\(.value.duration_seconds) seconds)\n   Preview: \(.value.preview_url)"' "$response_file"
read -r -p 'Download which track? Enter its number: ' choice
if [[ ! "$choice" =~ ^[0-9]{1,3}$ ]] || (( 10#$choice < 1 || 10#$choice > count )); then
  echo 'Run again and choose a number from the list.' >&2
  exit 1
fi
index=$((10#$choice - 1))
track="$(jq --argjson index "$index" '.data[$index]' "$response_file")"
track_id="$(jq -r '.id' <<< "$track")"
if [[ ! "$track_id" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo 'Track ID is not a safe filename.' >&2
  exit 1
fi
music_url="$(jq -r '.download_url' <<< "$track")"
if [[ "$music_url" != https://* && ! "$music_url" =~ ^http://127\.0\.0\.1:[0-9]+/ ]]; then
  echo 'Expected an HTTPS download URL.' >&2
  exit 1
fi
mkdir -p music
prefix="music/$track_id"
if [[ -e "$prefix.mp3" || -e "$prefix-credit.txt" || -e "$prefix.json" ]]; then
  echo 'Output already exists. Choose another track or move the existing files.' >&2
  exit 1
fi
# A separate public download request: no API key is sent to the media host.
curl --fail --silent --show-error --location --user-agent "$user_agent" --max-time 60 "$music_url" -o "$prefix.mp3"
jq -r '.attribution' <<< "$track" > "$prefix-credit.txt"
printf '%s\n' "$track" > "$prefix.json"
printf 'Downloaded: %s.mp3\nMusic credit: %s-credit.txt\nTrack metadata: %s.json\n' "$prefix" "$prefix" "$prefix"
