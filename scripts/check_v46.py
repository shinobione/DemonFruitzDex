#!/usr/bin/env python3
"""V4.6 provenance QA. Checks data integrity, not external playback."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
fruits=json.loads((ROOT/'data/fruits.json').read_text(encoding='utf8'))
clips=json.loads((ROOT/'data/clips.json').read_text(encoding='utf8'))
script=(ROOT/'data/clips.js').read_text(encoding='utf8')
app=(ROOT/'app.js').read_text(encoding='utf8')
page=(ROOT/'index.html').read_text(encoding='utf8')
errors=[]
match=re.search(r'window\.SHINO_CLIPS\s*=\s*(\{.*\});\s*$',script,re.S)
if not match:errors.append('clips.js cannot be decoded')
elif json.loads(match.group(1))!=clips:errors.append('clips.json and clips.js differ')
valid={fruit['id'] for fruit in fruits}
if not set(clips).issubset(valid):errors.append('Unknown fruit identifiers')
audited=[k for k,c in clips.items() if c.get('auditV46')]
if len(audited)!=40:errors.append(f'Expected 40 legacy audit entries, found {len(audited)}')
for slug,entry in clips.items():
    vids=([entry] if entry.get('youtubeId') else [])+entry.get('moreVideos',[])
    seen=set()
    for item in vids:
        ident=item.get('youtubeId','')
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}',ident):errors.append(f'{slug}: invalid YouTube id')
        if ident in seen:errors.append(f'{slug}: duplicate YouTube ID')
        seen.add(ident)
        if item.get('source')!='https://www.youtube.com/watch?v='+ident:errors.append(f'{slug}: YouTube source does not match video ID')
    episodes=([entry] if entry.get('episodeUrl') else [])+entry.get('moreEpisodes',[])
    seen=set()
    for item in episodes:
        url=item.get('episodeUrl','')
        m=re.search(r'/watch/([A-Za-z0-9]+)',url)
        if not m or not url.startswith('https://www.crunchyroll.com/'):errors.append(f'{slug}: non-standard episode URL');continue
        if m.group(1) in seen:errors.append(f'{slug}: duplicate episode ID across language aliases')
        seen.add(m.group(1))
if clips.get('ito-ito-no-mi',{}).get('youtubeId')=='I752TYMkM7Y':errors.append('Wrongly attributed Doflamingo video returned')
if 'id="onlyReview"' not in page or "state.reviewOnly" not in app:errors.append('Review filter not connected')
if not ("app.js?v=" in page and "clips.js?v=" in page):errors.append('Versioned asset scripts missing')
if errors:
    for error in errors:print('ERROR: '+error,file=sys.stderr)
    raise SystemExit(1)
videos=sum(len(([v] if v.get('youtubeId') else [])+v.get('moreVideos',[])) for v in clips.values())
episodes=sum(len(([v] if v.get('episodeUrl') else [])+v.get('moreEpisodes',[])) for v in clips.values())
print(f'PASS: {len(fruits)} fiches, {len(clips)} documentées, {len(audited)} historiques marquées, {videos} vidéos, {episodes} épisodes')
print('Validation statique uniquement : les droits, les liens à distance et le géoblocage ne sont pas certifiés.')
