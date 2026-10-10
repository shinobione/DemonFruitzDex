#!/usr/bin/env python3
"""Documentary audit, not a live streaming/geoaccess test."""
from pathlib import Path
from collections import defaultdict
import json
ROOT=Path(__file__).resolve().parents[1]
clips=json.loads((ROOT/'data/clips.json').read_text(encoding='utf-8'))
fruits=json.loads((ROOT/'data/fruits.json').read_text(encoding='utf-8'))
vrefs=defaultdict(list);erefs=defaultdict(list);legacy=[]
for fid,entry in clips.items():
    for item in ([entry] if entry.get('youtubeId') else [])+entry.get('moreVideos',[]):
        vrefs[item['youtubeId']].append(fid)
    for item in ([entry] if entry.get('episodeUrl') else [])+entry.get('moreEpisodes',[]):
        erefs[item['episodeUrl']].append(fid)
    if not entry.get('episodeEvidence') and not entry.get('sourceEvidence'):
        legacy.append(fid)
report={
 'scope':'Provenance documentaire et structure uniquement. Lecture, géoblocage et intégration NON testés.',
 'fruitCards':len(fruits),'documentedFruits':len(clips),'uncovered':len(fruits)-len(clips),
 'youtubeAssociations':sum(map(len,vrefs.values())),'uniqueYoutubeVideos':len(vrefs),
 'episodeAssociations':sum(map(len,erefs.values())),'uniqueEpisodes':len(erefs),
 'legacyEntriesWithoutRootEvidence':legacy,
 'sharedYoutubeVideos':{k:v for k,v in vrefs.items() if len(v)>1},
 'sharedEpisodes':{k:v for k,v in erefs.items() if len(v)>1}
}
out=ROOT/'reports';out.mkdir(exist_ok=True)
(out/'media-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Sources {len(clips)}/{len(fruits)}, YouTube {report['youtubeAssociations']} ({report['uniqueYoutubeVideos']} distinctes), épisodes {report['episodeAssociations']} ({report['uniqueEpisodes']} distincts), à examiner {len(legacy)}")
