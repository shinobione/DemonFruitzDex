#!/usr/bin/env python3
"""V4.9.b2: offline safety QA for CLIP CHECK and the expanded YouTube catalogue."""
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

root = Path(__file__).resolve().parents[1]
clips = json.loads((root / "data/clips.json").read_text(encoding="utf8"))
browser = (root / "data/clips.js").read_text(encoding="utf8")
page = (root / "index.html").read_text(encoding="utf8")
app = (root / "app.js").read_text(encoding="utf8")
checker = (root / "clip-check.html").read_text(encoding="utf8")
inventory = json.loads((root / "reports/catalogue-media-gap-v49b.json").read_text(encoding="utf8"))

m = re.search(r"window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$", browser, re.S)
assert m and json.loads(m.group(1)) == clips, "clip exports out of sync"

ids = {}
total = 0
for slug, record in clips.items():
    videos = ([record] if record.get("youtubeId") else []) + record.get("moreVideos", [])
    for v in videos:
        vid = v["youtubeId"]
        assert re.fullmatch(r"[A-Za-z0-9_-]{11}", vid), "invalid YouTube video ID"
        assert v.get("source") == "https://www.youtube.com/watch?v=" + vid, "non-YouTube watch URL"
        ids[(slug, vid)] = ids.get((slug, vid), 0) + 1
        total += 1
assert all(count == 1 for count in ids.values()), "duplicate videos on a fruit"
assert total == inventory["counts"]["youtubeAssociations"] == 48
assert len({slug for slug, _ in ids}) == inventory["counts"]["withYouTube"] == 34
assert set(ids) >= {
    ("nikyu-nikyu-no-mi", "ofJ3DkkOo7Y"),
    ("nikyu-nikyu-no-mi", "PvODesQjMgU"),
    ("gasu-gasu-no-mi", "NKgXWO2RK-A"),
    ("noro-noro-no-mi", "1hh_5xUZ5Mw"),
    ("doa-doa-no-mi", "HnsL-5GHUrc"),
    ("yuki-yuki-no-mi", "oLRxJVxoWWo"),
}, "Kuma sources missing"
assert not re.search(r"https?://(?:www\.)?crunchyroll\.com/(?:fr/)?watch/", json.dumps(clips)), "full episode URLs present"
assert all(not any(key in c for key in ("episodeUrl", "moreEpisodes", "episodeEvidence")) for c in clips.values()), "full-episode fields present"
assert "clip-check.html" in page and "clip-check.html?fruit=" in app
assert "clipCheckSource" in app, "details lack dedicated review link"
assert "data/clips.js?v=4.9b2" in page and "app.js?v=4.9b2" in page, "stale cache busting"
assert "data/clips.js?v=4.9b2" in checker, "clip-review catalogue version not aligned"
assert "nouveaux clips" in checker.lower() and "navigation privée" in checker.lower()
for status in ("embed-ok", "youtube-only", "login-required", "unavailable", "wrong-power", "other"):
    assert 'value="' + status + '"' in checker, f"missing manual review status {status}"
assert 'youtube-nocookie.com/embed/' in checker and 'https://www.youtube.com/watch?v=' in checker
assert "application/json" in checker and "URL.createObjectURL" in checker and "localStorage" in checker
assert "iframe chargé" in checker.lower() or "lecteur iframe chargé" in checker.lower(), "must not claim auto-verified playback"

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.inline = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.active = not dict(attrs).get("src")
    def handle_data(self, data):
        if self.active:
            self.inline.append(data)
    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False

parser = Scripts()
parser.feed(checker)
js = "\n".join(parser.inline)
assert js, "clip-check inline code missing"
node = subprocess.run(["node", "--check", "-"], input=js, text=True, capture_output=True)
assert node.returncode == 0, "clip-check JS syntax error: " + node.stderr

print("PASS V4.9.b2: 48 YouTube links, 34 fruits, including Foxy/Blueno/Monet, no episode URLs")
print("PASS V4.9.b2: Clip Check linked, verdicts available, JS parser checked")
print("WARNING: human playback tests required; iframe availability and France/no-login status remain unverified.")
