"""Mix a suitable MCW track beneath a video. Requires FFmpeg and ffprobe."""
import argparse
import json
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.error import URLError
from download_music import api_get, save_track


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--collection", choices=["relaxation", "sleep", "stories"], default="relaxation")
    parser.add_argument("--volume", type=float, default=0.15, help="Music volume, 0 to 1 (default: 0.15)")
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error("Input video does not exist")
    if not 0 <= args.volume <= 1:
        parser.error("--volume must be between 0 and 1")
    if args.output.suffix.lower() != ".mp4":
        parser.error("Use an .mp4 output filename")
    credit = args.output.with_name(args.output.stem + "-credit.txt")
    metadata = args.output.with_name(args.output.stem + "-music.json")
    if any(path.exists() for path in (args.output, credit, metadata)):
        parser.error("Output already exists; choose another output filename")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("Install FFmpeg and ffprobe first: https://ffmpeg.org/download.html")
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
        "-of", "json", str(args.video.resolve()),
    ], check=True, capture_output=True, text=True)
    info = json.loads(probe.stdout)
    duration = float(info["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Could not determine a positive video duration.")
    has_audio = any(stream["codec_type"] == "audio" for stream in info["streams"])
    tracks = api_get("/tracks", {
        "collection": args.collection, "min_duration": math.ceil(duration), "limit": 20,
    })["data"]
    if not tracks:
        raise ValueError("No track is long enough. Try a different collection or a shorter video.")
    track = random.choice(tracks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mcw-music-") as working:
        audio, _, _ = save_track(track, working)
        fade = min(1.0, duration / 2)
        music_filter = (
            f"[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume={args.volume},"
            f"afade=t=in:st=0:d={fade},afade=t=out:st={duration-fade}:d={fade}[music]"
        )
        if has_audio:
            # The trimmed music keeps short original audio from shortening the video.
            # Avoid apad here: this graph can stall on FFmpeg 8 when no padding is needed.
            filters = (
                music_filter + f";[0:a]atrim=duration={duration},asetpts=PTS-STARTPTS[original];"
                "[original][music]amix=inputs=2:duration=longest:normalize=0[mix]"
            )
            mapped_audio = "[mix]"
        else:
            filters, mapped_audio = music_filter, "[music]"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
            "-i", str(args.video.resolve()), "-i", str(audio),
            "-filter_complex", filters, "-map", "0:v:0", "-map", mapped_audio,
            "-t", str(duration), "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-movflags", "+faststart", str(args.output.resolve()),
        ], check=True)
    edits = f"Trimmed to {duration:.2f} seconds; reduced music volume to {args.volume}; added fades; mixed with video."
    credit.write_text(track["attribution"] + "\nChanges: " + edits + "\n", encoding="utf-8")
    metadata.write_text(json.dumps({"track": track, "changes": edits}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created: {args.output}\nTrack: {track['title']}\nMusic credit: {credit}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, URLError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from None
