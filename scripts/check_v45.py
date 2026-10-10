#!/usr/bin/env python3
"""Offline validation of the V4.5 media catalogue; NOT a playback or geoblock check."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
fruits=json.loads((ROOT/'data/fruits.json').read_text(encoding='utf-8'))
clips=json.loads((ROOT/'data/clips.json').read_text(encoding='utf-8'))
browser=(ROOT/'data/clips.js').read_text(encoding='utf-8')
index=(ROOT/'index.html').read_text(encoding='utf-8')
errors=[]
m=re.search(r'window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$',browser,re.S)
if not m or json.loads(m.group(1))!=clips:errors.append('clips.js is out of sync with clips.json')
ids={f['id'] for f in fruits}
if set(clips)-ids:errors.append('Unknown fruit IDs: '+repr(set(clips)-ids))
verified=0
for fruit,entry in clips.items():
    videos=([entry] if entry.get('youtubeId') else [])+entry.get('moreVideos',[])
    seen=set()
    for v in videos:
        vid=v['youtubeId']
        if not re.fullmatch('[A-Za-z0-9_-]{11}',vid):errors.append(f'{fruit}: invalid video ID')
        if vid in seen:errors.append(f'{fruit}: duplicate in same playlist')
        seen.add(vid)
        if v.get('source')!='https://www.youtube.com/watch?v='+vid:errors.append(f'{fruit}: source URL mismatch')
        if v.get('verificationStatus')=='publisher-metadata-verified':
            verified+=1
            if v.get('sourceEvidence')!=v.get('source'):errors.append(f'{fruit}: publisher evidence missing')
            if v.get('channel') not in ('Crunchyroll','Crunchyroll FR','Toei Animation','Crunchyroll in Spanish'):
                errors.append(f'{fruit}: unknown claimed publisher')
            if v.get('contentKind')!='clip':errors.append(f'{fruit}: unexpected media kind')
for vid in re.findall(r'https://i\.ytimg\.com/vi/([A-Za-z0-9_-]{11})/',index):
    if not any(vid in [v.get('youtubeId') for v in ([e] if e.get('youtubeId') else [])+e.get('moreVideos',[])] for e in clips.values()):
        errors.append(f'Spotlight ID {vid} not in catalogue')
if index.count('class="spotlight-card"')!=4:errors.append('Four curated spotlight items required')
if '04.5' not in index:errors.append('Wrong displayed version')
if errors:
    print('\n'.join('ERROR: '+x for x in errors),file=sys.stderr);raise SystemExit(1)
print(f'PASS: {len(fruits)} entries, {len(clips)} documented, {verified} publisher-metadata associations, four spotlight clips.')
print('Note: embed rights, regional availability and playback not tested.')
