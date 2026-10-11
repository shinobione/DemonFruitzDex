#!/usr/bin/env python3
"""V4.9.a gate: no full-episode URLs in client data or UI; clips retained."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
fruits = json.loads((ROOT / "data/fruits.json").read_text(encoding="utf-8"))
clips = json.loads((ROOT / "data/clips.json").read_text(encoding="utf-8"))
inventory = json.loads((ROOT / "reports/catalogue-media-gap-v49a.json").read_text(encoding="utf-8"))
browser = (ROOT / "data/clips.js").read_text(encoding="utf-8")
app = (ROOT / "app.js").read_text(encoding="utf-8")
html = (ROOT / "index.html").read_text(encoding="utf-8")
match = re.search(r"window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$", browser, re.S)
assert match and json.loads(match.group(1)) == clips, "browser clip export differs"
assert len(fruits) == len(inventory["records"]) == 166, "cross-reference rows missing"
assert len({x["id"] for x in inventory["records"]}) == 166, "duplicate IDs"
assert {x["id"] for x in inventory["records"]} == {x["id"] for x in fruits}, "source mapping incomplete"
assert not re.search(r"https?://(?:www\.)?crunchyroll\.com/(?:fr/)?watch/", json.dumps(clips)), "full-episode URL in data"
assert all(not any(k in c for k in ("episodeUrl", "moreEpisodes", "episodeEvidence")) for c in clips.values()), "episode fields in data"
assert not any(token in app for token in ("clipEpisodes", "makeEpisodeLink", "episodeBody", "episodes.length", "onlyYoutube")), "obsolete episode UI path"
assert "onlyYoutube" not in html and "ytInventory" not in html, "obsolete filter"
assert "hasScene = hasYoutube" in app, "clip filter includes unplayable episodes"
assoc = sum(bool(x.get("youtubeId")) + len(x.get("moreVideos", [])) for x in clips.values())
assert assoc == inventory["counts"]["youtubeAssociations"] and assoc >= 37, "existing YouTube clips lost"
assert inventory["counts"]["withYouTube"] >= 25, "existing YouTube fruit links lost"
assert inventory["counts"]["withPortrait"] == 162 and inventory["counts"]["withVisual"] == 140, "overlay inventory mismatch"
assert "episode-item" in app, "search links should remain visible"
print(f"PASS V4.9.a regression: 166 crosswalk rows, no full episodes, {assoc} YouTube clips (>=37 retained), 162 portraits, 140 visuals")
print("This does not certify YouTube iframe playback or provenance of fan art.")
