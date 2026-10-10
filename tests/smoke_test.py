"""Exercise the public examples without a live API key or real music download."""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class ExampleSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        missing = [name for name in ("node", "curl", "jq", "ffmpeg", "ffprobe") if not shutil.which(name)]
        if missing:
            raise RuntimeError("Missing test tools: " + ", ".join(missing))
        cls.temporary = tempfile.TemporaryDirectory(prefix="mcw-example-tests-")
        cls.folder = Path(cls.temporary.name)
        cls.mode = "ok"
        cls.api_requests = []
        cls.media_requests = []
        cls.synthetic_audio = cls.folder / "synthetic.mp3"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
            "sine=frequency=440:duration=2", "-c:a", "libmp3lame", str(cls.synthetic_audio),
        ], check=True)
        cls.audio_bytes = cls.synthetic_audio.read_bytes()

        class MediaHandler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                cls.media_requests.append((self.path, self.headers.get("Authorization")))
                if self.path.startswith("/redirect/"):
                    self.send_response(302)
                    self.send_header("Location", "/audio/" + self.path.split("/")[-1])
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.end_headers()
                self.wfile.write(cls.audio_bytes)

        cls.media_server = ThreadingHTTPServer(("127.0.0.1", 0), MediaHandler)
        cls.media_origin = f"http://127.0.0.1:{cls.media_server.server_port}"
        cls.tracks = copy.deepcopy(json.loads((ROOT / "docs/responses/tracks.json").read_text())["data"])
        for track in cls.tracks:
            track["download_url"] = cls.media_origin + "/redirect/" + track["id"]
            track["preview_url"] = cls.media_origin + "/preview/" + track["id"]

        class ApiHandler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                cls.api_requests.append((self.path, self.headers.get("Authorization")))
                if cls.mode == "redirect":
                    self.send_response(302)
                    self.send_header("Location", cls.media_origin + "/credential-leak")
                    self.end_headers()
                    self.wfile.write(b'{"data": []}')
                    return
                if cls.mode in {"401", "429"}:
                    self.send_response(int(cls.mode))
                    self.send_header("Content-Type", "application/json")
                    if cls.mode == "429":
                        self.send_header("Retry-After", "7")
                    self.end_headers()
                    self.wfile.write(b'{"error":{"code":"test_error","message":"Synthetic failure"}}')
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                url = urlsplit(self.path)
                if url.path.startswith("/api/v1/tracks/"):
                    body = {"data": cls.tracks[0]}
                else:
                    minimum = float(parse_qs(url.query).get("min_duration", ["0"])[0])
                    tracks = [] if cls.mode == "empty" else [t for t in cls.tracks if t["duration_seconds"] >= minimum]
                    body = {"data": tracks, "pagination": {"total": len(tracks), "limit": 5, "offset": 0, "next_offset": None}}
                self.wfile.write(json.dumps(body).encode())

        cls.api_server = ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
        cls.api_origin = f"http://127.0.0.1:{cls.api_server.server_port}/api/v1"
        for server in (cls.api_server, cls.media_server):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        cls.clients = {
            "python": [sys.executable, str(ROOT / "examples/download_music.py")],
            "javascript": ["node", str(ROOT / "examples/download_music.mjs")],
            "shell": ["bash", str(ROOT / "examples/download_music.sh")],
        }

    @classmethod
    def tearDownClass(cls):
        for server in (cls.api_server, cls.media_server):
            server.shutdown()
            server.server_close()
        cls.temporary.cleanup()

    def setUp(self):
        type(self).mode = "ok"
        self.api_requests.clear()
        self.media_requests.clear()

    def run_example(self, command, answer="2\n", key=True):
        environment = dict(os.environ, MCW_API_BASE_URL=self.api_origin)
        environment.pop("MCW_API_KEY", None)
        if key:
            environment["MCW_API_KEY"] = "synthetic-test-key"
        working = Path(tempfile.mkdtemp(dir=self.folder))
        result = subprocess.run(command, input=answer, cwd=working, env=environment,
                                capture_output=True, text=True, timeout=30)
        self.assertNotIn("synthetic-test-key", result.stdout + result.stderr)
        return result, working

    def test_all_languages_download_the_selected_track_and_preserve_credits(self):
        for name, command in self.clients.items():
            with self.subTest(language=name):
                self.api_requests.clear()
                self.media_requests.clear()
                result, working = self.run_example(command)
                self.assertEqual(result.returncode, 0, result.stderr)
                selected = self.tracks[1]
                prefix = working / "music" / selected["id"]
                self.assertEqual(prefix.with_suffix(".mp3").read_bytes(), self.audio_bytes)
                self.assertEqual(Path(str(prefix) + "-credit.txt").read_text(), selected["attribution"] + "\n")
                self.assertEqual(prefix.with_suffix(".json").read_text().strip(),
                                 json.dumps(json.loads(prefix.with_suffix(".json").read_text()), ensure_ascii=False, indent=2))
                metadata = json.loads(prefix.with_suffix(".json").read_text())
                self.assertEqual(metadata["license"], selected["license"])
                self.assertEqual(metadata["source_url"], selected["source_url"])
                self.assertEqual(len(self.api_requests), 1)
                self.assertEqual(self.api_requests[0][1], "Bearer synthetic-test-key")
                self.assertGreaterEqual(len(self.media_requests), 2)
                self.assertTrue(all(auth is None for _, auth in self.media_requests))

    def test_api_redirects_never_receive_credentials(self):
        type(self).mode = "redirect"
        for name, command in self.clients.items():
            with self.subTest(language=name):
                result, _ = self.run_example(command)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.media_requests, [])

    def test_missing_keys_make_no_network_requests(self):
        for name, command in self.clients.items():
            with self.subTest(language=name):
                result, _ = self.run_example(command, key=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("MCW_API_KEY", result.stdout + result.stderr)
        self.assertEqual(self.api_requests, [])
        self.assertEqual(self.media_requests, [])

    def test_empty_searches_and_bad_choices_do_not_download(self):
        for mode, answer in (("empty", "1\n"), ("ok", "99\n")):
            type(self).mode = mode
            for name, command in self.clients.items():
                with self.subTest(mode=mode, language=name):
                    result, _ = self.run_example(command, answer=answer)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.media_requests, [])

    def test_unauthorized_and_rate_limited_requests_stop_without_retries(self):
        for status in ("401", "429"):
            type(self).mode = status
            for name, command in self.clients.items():
                with self.subTest(status=status, language=name):
                    self.api_requests.clear()
                    result, _ = self.run_example(command)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(status, result.stdout + result.stderr)
                    if status == "429":
                        self.assertIn("7", result.stdout + result.stderr)
                    self.assertEqual(len(self.api_requests), 1)
                    self.assertEqual(self.media_requests, [])

    def test_python_unattended_and_specific_track_modes(self):
        for arguments in (("--first",), ("--track-id", self.tracks[0]["id"])):
            with self.subTest(arguments=arguments):
                result, working = self.run_example(self.clients["python"] + list(arguments), answer="")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((working / "music" / (self.tracks[0]["id"] + ".mp3")).exists())

    def test_video_mixing_with_and_without_original_audio(self):
        for has_audio in (False, True):
            with self.subTest(original_audio=has_audio):
                original = self.folder / f"original-{has_audio}.mp4"
                command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                           "color=c=blue:s=64x64:d=1:r=24"]
                if has_audio:
                    command += ["-f", "lavfi", "-i", "sine=frequency=220:duration=1", "-c:a", "aac"]
                command += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(original)]
                subprocess.run(command, check=True)
                original_bytes = original.read_bytes()
                result, working = self.run_example([
                    sys.executable, str(ROOT / "examples/add_music_to_video.py"),
                    str(original), "--output", "ready/result.mp4",
                ], answer="")
                self.assertEqual(result.returncode, 0, result.stderr)
                output = working / "ready/result.mp4"
                info = json.loads(subprocess.check_output([
                    "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                    "-of", "json", str(output),
                ], text=True))
                self.assertAlmostEqual(float(info["format"]["duration"]), 1.0, delta=0.15)
                self.assertEqual({s["codec_type"] for s in info["streams"]}, {"video", "audio"})
                self.assertIn("Changes: ", (working / "ready/result-credit.txt").read_text())
                self.assertEqual(original.read_bytes(), original_bytes)
                self.assertTrue(all(auth is None for _, auth in self.media_requests))
                # The same output must not be silently replaced.
                environment = dict(os.environ, MCW_API_BASE_URL=self.api_origin, MCW_API_KEY="synthetic-test-key")
                repeat = subprocess.run([
                    sys.executable, str(ROOT / "examples/add_music_to_video.py"),
                    str(original), "--output", str(output),
                ], env=environment, capture_output=True, text=True, timeout=30)
                self.assertNotEqual(repeat.returncode, 0)
                self.assertIn("already exists", repeat.stderr)

    def test_documentation_links_and_response_contracts(self):
        for document in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                if ":" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative:
                    self.assertTrue((document.parent / relative).exists(), f"Broken link in {document.name}: {target}")
        specification = json.loads((ROOT / "openapi.json").read_text())
        self.assertEqual(len(specification["paths"]), 5)
        required = set(specification["components"]["schemas"]["Track"]["required"])
        for track in json.loads((ROOT / "docs/responses/tracks.json").read_text())["data"]:
            self.assertTrue(required.issubset(track))
        track = json.loads((ROOT / "docs/responses/track.json").read_text())["data"]
        self.assertTrue(required.issubset(track))
        self.assertEqual(json.loads((ROOT / "docs/responses/capabilities.json").read_text())["track_count"], 181)


if __name__ == "__main__":
    unittest.main(verbosity=2)
