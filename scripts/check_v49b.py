#!/usr/bin/env python3
"""V4.9.b offline safety and metadata-regression test (not actual playback)."""
from pathlib import Path
import json, re

root=Path(__file__).resolve().parents[1]
fruits=json.loads((root/"data/fruits.json").read_text(encoding="utf-8"))
clips=json.loads((root/"data/clips.json").read_text(encoding="utf-8"))
inventory=json.loads((root/"reports/catalogue-media-gap-v49b.json").read_text(encoding="utf-8"))
app=(root/"app.js").read_text(encoding="utf-8")
page=(root/"index.html").read_text(encoding="utf-8")
browser=(root/"data/clips.js").read_text(encoding="utf-8")
m=re.search(r"window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$",browser,re.S)
assert m and json.loads(m.group(1))==clips,"JS/JSON video catalog divergence"
assert len(fruits)==len(inventory["records"])==166
expected={
  "bari-bari-no-mi":["AdM7PV5kako","Zupy-QIf-8U"],
  "horo-horo-no-mi":["p5KF8XZlqEk"],
  "kage-kage-no-mi":["fSgU4NEqa4s"],
  "doku-doku-no-mi":["592XWC7Abkc"],
  "nikyu-nikyu-no-mi":["ofJ3DkkOo7Y","PvODesQjMgU"],
  "gasu-gasu-no-mi":["NKgXWO2RK-A"],
  "noro-noro-no-mi":["1hh_5xUZ5Mw"],
  "doa-doa-no-mi":["HnsL-5GHUrc"],
  "yuki-yuki-no-mi":["oLRxJVxoWWo"],
  "ito-ito-no-mi":["ow1Hpfnlri4"],
  "pero-pero-no-mi":["5r92RNbFpz4"],
}
all_vids=[]
for fruit,entry in clips.items():
    videos=([entry] if entry.get("youtubeId") else [])+entry.get("moreVideos",[])
    for clip in videos:
        vid=clip["youtubeId"]
        assert re.fullmatch(r"[A-Za-z0-9_-]{11}",vid),f"bad youtube ID: {fruit}"
        assert clip.get("source")=="https://www.youtube.com/watch?v="+vid
        all_vids.append((fruit,vid))
    if fruit in expected:
        actual=[clip["youtubeId"] for clip in videos]
        assert actual==expected[fruit],(fruit,actual)
        for clip in videos:
            assert clip.get("verificationStatus")=="public-metadata-verified"
            assert clip.get("publisherType")=="community-upload"
            assert clip.get("sourceEvidence")==clip.get("source")
            assert clip.get("contentKind") in ("clip","compilation")
            assert clip.get("playbackStatus")=="not-tested"
            assert clip.get("embedStatus")=="not-tested"
            assert clip.get("regionalStatus")=="not-tested"
assert len(all_vids)==50 and len({f for f,_ in all_vids})==36, "video totals"
assert inventory["counts"]["youtubeAssociations"]==50
assert inventory["counts"]["withYouTube"]==36
assert not re.search(r"https?://(?:www\.)?crunchyroll\.com/(?:fr/)?watch/",json.dumps(clips)), "full episode link returned"
assert not any("episodeUrl" in c or "moreEpisodes" in c for c in clips.values()),"full episode metadata returned"
assert "MONTAGE D’ATTAQUES" in app and "CHAÎNE COMMUNAUTAIRE" in app
assert "app.js?v=4.9b2" in page and "clips.js?v=4.9b2" in page
assert "clipInventory" in page and "hasScene = hasYoutube" in app
print("PASS V4.9.b2: 13 new associations, 50 YouTube references, 36 fruits, 0 full episodes")
print("WARNING: youtube iframe, age restriction, and no-login availability NOT TESTED")
