#!/usr/bin/env python3
"""V4.9.b3 regression: proposal flow, local verdict sync, YouTube ID validation."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, subprocess

root = Path(__file__).resolve().parents[1]
clips = json.loads((root/"data/clips.json").read_text(encoding="utf-8"))
app = (root/"app.js").read_text(encoding="utf-8")
site = (root/"index.html").read_text(encoding="utf-8")
page = (root/"clip-check.html").read_text(encoding="utf-8")
manifest = json.loads((root/"reports/catalogue-media-gap-v49b.json").read_text(encoding="utf-8"))

links = [(slug, v["youtubeId"]) for slug, item in clips.items()
         for v in ([item] if item.get("youtubeId") else []) + item.get("moreVideos", [])]
assert len(links) == 50 and len({x[0] for x in links}) == 36
assert manifest["counts"]["youtubeAssociations"] == 50
assert manifest["counts"]["withYouTube"] == 36
assert len(manifest["records"]) == 166
assert len(links) == len(set(links)), "duplicate clip IDs within fruit"
assert not re.search(r"https?://(?:www\.)?crunchyroll\.com/(?:fr/)?watch/",json.dumps(clips))

assert "clip-check.html?fruit=" in app and "suggest=1" in app
assert "clipLocalNotice" in app and "clipVerdictLabels" in app
assert "button.disabled=true" in app and "clipIsFlagged(reviewStatus)" in app
assert "toast('Lecture depuis '" not in app, "iframe insertion is not proof of playback"
assert "demonfruitzdex.clip-review.v49b" in app and "demonfruitzdex.clip-review.v49b" in page
assert "clip-review-local" in (root/"styles.css").read_text(encoding="utf-8")

assert 'id="proposeFruit"' in page and 'id="proposeUrl"' in page
assert 'id="proposeAdd"' in page and 'id="proposeExport"' in page
assert 'id="importFile"' in page
assert "demonfruitzdex.clip-proposals.v1" in page
assert "demonfruitzdex.clip-review.v1" in page
assert "unverified-user-proposal" in page
assert "PROPOSAL_KEY" in page and "localStorage.setItem(PROPOSAL_KEY" in page
assert "if(file.size>1024*1024)" in page, "audit JSON upload must be bounded"
assert "var known=new Set(entries.map(key))" in page, "reject unknown review keys"
assert "previous>=updated" in page, "do not replace fresher local review"
assert "window.SHINO_CLIPS=" not in page, "suggestions must not publish automatically"
assert "YouTube" in page and "sans compte" in page
assert "clips.js?v=4.9b3" in site and "clips.js?v=4.9b3" in page
assert "app.js?v=4.9b3" in site

class InlineScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.scripts=[]
    def handle_starttag(self, tag, attrs):
        if tag=="script":
            self.active=not dict(attrs).get("src")
    def handle_data(self, data):
        if self.active:
            self.scripts.append(data)
    def handle_endtag(self, tag):
        if tag=="script":
            self.active=False

parser=InlineScripts()
parser.feed(page)
js="\n".join(parser.scripts)
assert js
compile_result=subprocess.run(["node","--check","-"],input=js,text=True,capture_output=True)
assert compile_result.returncode==0,compile_result.stderr

fn=re.search(r"  function parseYouTube\(raw\)\{[\s\S]*?\n  \}\n  function renderProposals",js)
assert fn, "YouTube ID parser missing"
fn=fn.group(0).split("\n  function renderProposals")[0]
test_code=fn + """
const yes=[
'https://www.youtube.com/watch?v=1hh_5xUZ5Mw',
'https://youtu.be/1hh_5xUZ5Mw',
'https://youtube.com/shorts/1hh_5xUZ5Mw',
'https://www.youtube-nocookie.com/embed/1hh_5xUZ5Mw',
'https://m.youtube.com/live/1hh_5xUZ5Mw'
];
const no=[
'https://notyoutube.com/watch?v=1hh_5xUZ5Mw',
'http://youtube.com/watch?v=1hh_5xUZ5Mw',
'https://www.youtube.com/playlist?list=PLAAAA',
'https://www.youtube.com/watch?v=invalid',
'javascript:alert(1)'
];
if(!yes.every(x=>parseYouTube(x)==='1hh_5xUZ5Mw'))process.exit(2);
if(!no.every(x=>parseYouTube(x)===null))process.exit(3);
"""
validate=subprocess.run(["node","-e",test_code],text=True,capture_output=True)
assert validate.returncode==0,validate.stderr+" (video URL normalization failed)"

print("PASS V4.9.b3: 50 clips / 36 fruits, no full episodes, suggestion URL validation and local review wiring")
print("PASS: CLIP CHECK inline JS syntax, bounded import, explicit local proposals and verdicts")
print("Playback/iframe/no-login in France must still be tested by a human reviewer.")
