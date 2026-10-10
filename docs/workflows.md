# Creator workflows

Start with [API key setup](quickstart.md). The API finds music; FFmpeg or your editor assembles the video or audio. Preview music and adjust the mix before publishing.

## Add music to a folder of Shorts

Requires Python 3.10+ and [FFmpeg](https://ffmpeg.org/download.html), including `ffprobe`, on your PATH.

The example chooses a random relaxing track at least as long as the video, downloads it, and mixes it beneath any existing audio. It applies a short fade at each end and saves the credit and metadata beside a new MP4. Input videos are preserved. This is a fixed-volume mix; it does not analyze speech or automatically duck the music.

One video:

```sh
python3 examples/add_music_to_video.py ./shorts/clip.mp4 --output ./ready/clip.mp4
```

Every MP4 in a folder, using Bash or zsh:

```sh
mkdir -p ready
for video in ./shorts/*.mp4; do
  python3 examples/add_music_to_video.py "$video" --output "./ready/$(basename "$video")"
done
```

Use `--volume 0.08` for quieter music or `--collection stories` for cinematic music. Tracks are sampled from the first 20 matching results, so repeats are possible. If no track is long enough, choose a different collection or edit the workflow to loop shorter audio and record that edit in the credit.

If an output already exists, the example stops instead of replacing it. MP4 video is re-encoded as H.264 and audio as AAC; output quality is controlled by FFmpeg's settings in the script.

## Make a podcast intro

Find and select a gentle piano track:

```sh
python3 examples/download_music.py --query 'gentle piano' --output podcast-music
```

Using the downloaded filename, create a 15-second intro with a one-second fade in and a two-second fade out:

```sh
ffmpeg -n -i podcast-music/TRACK_ID.mp3 -t 15 \
  -af 'afade=t=in:st=0:d=1,afade=t=out:st=13:d=2' podcast-intro.mp3
```

Replace `TRACK_ID` with your chosen ID. Add `Changes: Trimmed to 15 seconds; added fades.` to its credit, and put that credit in your published show notes.

## Daily video pipeline

Run the mixing example after your existing workflow has produced its video:

```sh
python3 examples/add_music_to_video.py ./daily/today.mp4 --output ./ready/today.mp4
```

That creates `today.mp4`, `today-credit.txt`, and `today-music.json` in `ready/`.

Pass the new video to your existing YouTube uploader, and append the entire credit file to the description. YouTube authentication and uploading are separate from MCW's API and must use your authorized YouTube account. This repository does not include a YouTube uploader or publish anything automatically.

For an assistant that already has your editing and YouTube tools, try:

> Update my ./daily workflow: after each video is produced, find a relaxing song with MCW, mix it quietly under the video, and upload it through my connected YouTube tool with the music credit in the description. Preserve the original video.

## What to keep with each project

Save the track ID, source URL, license, supplied attribution, and a description of any music edits. The examples save these beside the output. A music credit belongs in the published project's credits or description as well as in your working files.
