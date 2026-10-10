#!/usr/bin/env python3
"""Structural quality gate for publisher-hosted clip references (no scraping)."""
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
fruits=json.loads((ROOT/'data/fruits.json').read_text(encoding='utf8'))
clips=json.loads((ROOT/'data/clips.json').read_text(encoding='utf8'))
fruit_ids={f['id'] for f in fruits}
errors=[]
for slug,record in clips.items():
    if slug not in fruit_ids: errors.append(f'{slug}: fruit inconnu')
    seen=set()
    videos=([record] if record.get('youtubeId') else [])+record.get('moreVideos',[])
    for v in videos:
        mid=v.get('youtubeId','')
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}',mid):errors.append(f'{slug}: id YouTube invalide {mid}')
        if mid in seen:errors.append(f'{slug}: vidéo dupliquée {mid}')
        seen.add(mid)
        url=v.get('source','')
        if url != 'https://www.youtube.com/watch?v='+mid:errors.append(f'{slug}: URL YouTube non concordante {url}')
        if not v.get('title') or not v.get('channel'):errors.append(f'{slug}: titre/source manquant')
    eps=([{'episodeUrl':record['episodeUrl']}] if record.get('episodeUrl') else [])+record.get('moreEpisodes',[])
    seen=set()
    for ep in eps:
        url=ep.get('episodeUrl','')
        if not url.startswith('https://www.crunchyroll.com/'):errors.append(f'{slug}: source épisode invalide {url}')
        if url in seen:errors.append(f'{slug}: épisode dupliqué {url}')
        seen.add(url)
    for so in record.get('social',[]):
        if not so.get('url','').startswith('https://www.facebook.com/onepieceofficial/'):
            errors.append(f'{slug}: source sociale non autorisée')
if errors:
    for err in errors:print('ERREUR',err,file=sys.stderr)
    sys.exit(1)
print(f'PASS {len(fruits)} fruits, {len(clips)} avec sources, {sum(len(([x] if x.get("youtubeId") else [])+x.get("moreVideos",[])) for x in clips.values())} liens YouTube, {sum(len(([x] if x.get("episodeUrl") else [])+x.get("moreEpisodes",[])) for x in clips.values())} liens épisodes')
