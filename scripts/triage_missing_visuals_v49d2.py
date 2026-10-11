#!/usr/bin/env python3
"""Editorial queue for exactly 26 empty fruit/power illustration slots.

Priority is not a claim of canonical art availability; all proposed imagery
must undergo human source/rights/content verification before publication.
"""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
inventory=json.loads((root/'reports/media-inventory-v49d.json').read_text(encoding='utf-8'))
missing=[r for r in inventory['records'] if not r['visual']['registered']]
assert len(missing)==26
P1={'toshi-toshi-no-mi','oshi-oshi-no-mi','kibi-kibi-no-mi','nomi-nomi-no-mi',
    'hito-hito-no-mi-mod-le-onyudo','inu-inu-no-mi-mod-le-dachshund','tori-tori-no-mi-mod-le-albatros',
    'gabu-gabu-no-mi','poke-poke-no-mi','shari-shari-no-mi'}
UNCERTAIN={'fruit-sans-nom-d-urouge','fruit-sans-nom-de-laffitte','minotaurus-fruit-inconnu',
           'minorhinoceros-fruit-inconnu','minozebra-fruit-inconnu','minokoala-fruit-inconnu'}
MYTHICAL={'ryu-ryu-no-mi-mod-le-kirin','risu-risu-no-mi-mod-le-ratatoskr',
          'fruit-mythique-gyuki','fruit-mythique-sandworm','fruit-mythique-bakotsu',
          'fruit-mythique-itsumade','fruit-mythique-fengxi','fruit-mythique-cerb-re'}
def classify(row):
    slug=row['id']
    if slug in UNCERTAIN:
        return 'C','unknown-fruit-or-power-name','Avoid asserting a physical Devil Fruit illustration; investigate confirmed transformation/technique scenes first.'
    if slug in MYTHICAL:
        return 'B','mythical-transformation','Look for an explicitly identified manga/anime transformation, distinguish manga spoilers, never invent a physical fruit.'
    if slug in P1:
        return 'A','named-power-or-zoan-form','Prefer a verified canon action scene or Zoan transformation, clearly labelled as power/form rather than physical fruit.'
    return 'B','named-power-candidate','Find a correctly attributed visual of the named power; no unverified fan art or fruit shape.'
items=[]
for row in missing:
    priority,kind,instruction=classify(row)
    items.append({'id':row['id'],'fruit':row['name'],'user':row['holder'],
                  'family':row['family'],'priority':priority,'illustrationWanted':kind,
                  'hasPortrait':row['portrait']['registered'],'acceptanceRule':instruction,
                  'candidateUrl':None,'candidateStatus':'not-researched-or-not-verified',
                  'evidenceUrl':None,'reviewedBy':None,'licenseStatus':'not-established'})
items.sort(key=lambda x:(x['priority'],x['fruit']))
totals={p:sum(x['priority']==p for x in items) for p in ('A','B','C')}
assert sum(totals.values())==26
result={'schema':'demonfruitzdex.media-illustration-backlog.v49d2',
        'scope':{'fruits':166,'notIllustrated':len(items),'priority':totals},
        'note':'Editorial priorities are research tasks, not verified canon media. Physical fruit appearance is not inferred from missing images.',
        'items':items}
dest=root/'reports/media-illustration-backlog-v49d2.json'
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ILLUSTRATION_BACKLOG='+json.dumps(totals),flush=True)
print('PASS: 26 unknown/absent visuals queued with honest evidence and license status',flush=True)
