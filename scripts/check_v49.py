#!/usr/bin/env python3
"""DemonFruitzDex V4.9 source-audit checks; playback and HTTP image load require a browser."""
from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
fruits=json.loads((root/'data/fruits.json').read_text(encoding='utf8'))
clips=json.loads((root/'data/clips.json').read_text(encoding='utf8'))
page=(root/'index.html').read_text(encoding='utf8')
media=(root/'media-check.html').read_text(encoding='utf8')
app=(root/'app.js').read_text(encoding='utf8')
portraits=(root/'data/portraits-v49.js').read_text(encoding='utf8')
videos=(root/'data/clips.js').read_text(encoding='utf8')
errors=[]
m=re.search(r'window\.SHINO_PORTRAITS_V49\s*=\s*(\[.*?\]);',portraits,re.S)
new=json.loads(m.group(1)) if m else []
if len(new)!=8: errors.append('V4.9 requires eight sourced portrait entries')
if len({x['id'] for x in new})!=len(new): errors.append('Duplicate V4.9 portrait IDs')
known={f['id'] for f in fruits}
if {x['id'] for x in new}-known: errors.append('Unknown fruit in portrait sources')
for x in new:
    if not x.get('portrait_evidence') or not x.get('portrait_file'):
        errors.append(x['id']+': missing file provenance')
    if x.get('portrait_load_status')!='à contrôler depuis Media Check':
        errors.append(x['id']+': newly linked remote image cannot be claimed verified')
    if not x['portrait'].startswith('https://static.wikia.nocookie.net/onepiece/images/'):
        errors.append(x['id']+': unexpected image source')
b=re.search(r'window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$',videos,re.S)
if not b or json.loads(b.group(1))!=clips:errors.append('JSON/browser video catalogues differ')
smoker=clips.get('moku-moku-no-mi',{})
v=[v for v in smoker.get('moreVideos',[]) if v.get('youtubeId')=='4frfkxIubLc']
if len(v)!=1 or v[0].get('contentKind')!='live-action':
    errors.append('Official Netflix live action must be explicitly marked')
if not ('ADAPTATION NETFLIX LIVE-ACTION' in app and 'artwork-user-substitute' in app):
    errors.append('On-screen provenance of substitutes is missing')
if not ('portraits-v49.js?v=4.9' in page and 'app.js?v=4.9' in page):
    errors.append('V4.9 sources are not loaded by the home page')
if not ('portraits-v49.js?v=4.9' in media and 'scripts/media-check-v49f.js?v=4.9f' in media and 'const getItems=()=>all.flatMap' in (root/'scripts/media-check-v49f.js').read_text(encoding='utf8')):
    errors.append('V4.9 portraits excluded from browser Media Check')
if errors:
    for e in errors:print('FAIL:',e,file=sys.stderr)
    raise SystemExit(1)
print('PASS: 8 source-traced portraits, user portrait fallback, 1 flagged Netflix clip, browser media check updated.')
print('Image URLs and playback are NOT automatically verified; run Media Check in a browser.')
