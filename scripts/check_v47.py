#!/usr/bin/env python3
"""V4.7 static gate: does not test external links, image loads or video playback."""
from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
fruits=json.loads((root/'data/fruits.json').read_text(encoding='utf8'))
clips=json.loads((root/'data/clips.json').read_text(encoding='utf8'))
client=(root/'data/clips.js').read_text(encoding='utf8')
sources=(root/'data/portrait-sources.js').read_text(encoding='utf8')
app=(root/'app.js').read_text(encoding='utf8')
page=(root/'index.html').read_text(encoding='utf8')
errors=[]
raw=re.search(r'window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$',client,re.S)
if not raw or json.loads(raw.group(1))!=clips:errors.append('JSON and browser clip data differ')
extra=re.search(r'window\.SHINO_PORTRAIT_SOURCES\s*=\s*(\{.*?\});\s*if',sources,re.S)
if not extra:errors.append('Portrait metadata missing');port={}
else:port=json.loads(extra.group(1))
ids={f['id'] for f in fruits}
if set(port)-ids:errors.append('Unknown portrait fruit IDs')
if not ('data/portrait-sources.js?v=' in page and 'app.js?v=' in page):errors.append('Scripts missing/version incorrect')
if not ('const openSearch=' in app and 'const youtubeSearch=' in app and '${openSearch}${episodeBody}' in app):errors.append('YouTube-first search UI not present')
for required in ('IRXco8fXxBE','aLG9XoxJE7g','SJtADPK0fKQ'):
  if not any(required==v.get('youtubeId') for c in clips.values() for v in ([c] if c.get('youtubeId') else [])+c.get('moreVideos',[])):
    errors.append('ADN publisher clip missing: '+required)
new_faces=len(port)+len(re.findall(r'\{\s*"id":"(?:inu-inu-no-mi-mod-le-dachshund|inu-inu-no-mi-mod-le-tanuki)"',sources))
new_art=len(re.findall(r'\{\s*"id":"(?:numa-numa-no-mi|wapu-wapu-no-mi|inu-inu-no-mi-mod-le-loup)"',sources))
if new_faces!=13:errors.append(f'Expected 13 source references, got {new_faces}')
if new_art!=3:errors.append(f'Expected 3 additional power illustrations, got {new_art}')
if errors:
  print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr);sys.exit(1)
print(f'PASS {len(fruits)} fruits, {len(clips)} documented, {new_faces} added user illustrations, {new_art} added power illustrations')
print('External load, geoavailability and actual video playback NOT verified.')
