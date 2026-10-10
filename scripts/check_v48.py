#!/usr/bin/env python3
"""V4.8 static asset-source gate. Browser playback and image-loading checks are separate."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
fruits=json.loads((ROOT/'data/fruits.json').read_text(encoding='utf8'))
portrait_js=(ROOT/'data/portraits-v48.js').read_text(encoding='utf8')
power_js=(ROOT/'data/power-art-v48.js').read_text(encoding='utf8')
index=(ROOT/'index.html').read_text(encoding='utf8')
app=(ROOT/'app.js').read_text(encoding='utf8')
diagnostics=(ROOT/'media-check.html').read_text(encoding='utf8')
errors=[]
def extract(js,key,closing):
    m=re.search(r'window\.'+key+r'\s*=\s*(\[.*?\])\s*;\s*'+closing,js,re.S)
    if not m:errors.append('Cannot extract '+key);return []
    return json.loads(m.group(1))
portraits=extract(portrait_js,'SHINO_EXTRA_PORTRAITS','if')
arts=extract(power_js,'SHINO_EXTRA_POWER_ART','if')
ids={f['id'] for f in fruits}
for group,entries in [('portraits',portraits),('art',arts)]:
    if len({x['id'] for x in entries})!=len(entries):errors.append('Repeated fruit id within '+group)
    if not {x['id'] for x in entries}.issubset(ids):errors.append('Unknown fruit ID in '+group)
    if any(not x.get('portrait_file') for x in entries) if group=='portraits' else any(not x.get('file') for x in entries):
        errors.append('Unnamed file in '+group)
if len(portraits)!=20 or len(arts)!=4:errors.append('Expected 20 portraits / 4 power images')
for x in arts:
    if x.get('visual')!='pouvoir':errors.append('Seraphim power artwork incorrectly claimed as fruit')
if not all(k in index for k in ('portraits-v48.js?v=','power-art-v48.js?v=','app.js?v=','href="media-check.html"')):
    errors.append('V4.8 UI/diagnostics entry not loaded')
if not all(k in app for k in ('data-media-fallback','IMAGE EXTERNE INDISPONIBLE','Special:Redirect/file')):
    errors.append('Remote-image retry and warning missing')
if 'Tester 30 images' not in diagnostics or 'Exporter le rapport JSON' not in diagnostics:
    errors.append('Browser-side diagnostics lacks required actions')
if errors:
    print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr);sys.exit(1)
print(f'PASS — {len(fruits)} base records, {len(portraits)} V4.8 portrait refs, {len(arts)} V4.8 power refs, image diagnostics available.')
print('A catalogued URL is NOT confirmed to render. Use media-check.html from the browser to test image delivery.')
