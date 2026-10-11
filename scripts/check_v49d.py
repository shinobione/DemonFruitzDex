#!/usr/bin/env python3
"""Fail CI for incomplete audits and corrupt data, not for third-party host blocks."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, subprocess

root=Path(__file__).resolve().parents[1]
inv=json.loads((root/'reports/media-inventory-v49d.json').read_text(encoding='utf-8'))
audit=json.loads((root/'reports/media-browser-audit-v49d.json').read_text(encoding='utf-8'))
records=inv['records']
assert len(records)==166 and len({x['id'] for x in records})==166
assert inv['stats']['entries']==166
assert inv['stats']['portraitRegistered']==164
assert inv['stats']['visualRegistered']==140
assert inv['stats']['directReferences']==304
assert inv['stats']['noPortrait']==2
assert inv['stats']['noVisual']==26
assert audit['scope']['fruits']==166
assert audit['scope']['mediaReferencesTested']==304
assert audit['scope']['expectedFullMediaReferences']==304
assert audit['scope']['subset'] is False
assert len(audit['results'])==304
keys=[(x['id'],x['kind']) for x in audit['results']]
assert len(set(keys))==304
assert all(x['classification'] in {'direct-loaded','fallback-loaded','browser-load-failed','timeout-unconfirmed','wiki-placeholder'} for x in audit['results'])
assert sum(audit['outcomes'].values())==304
assert all(x['direct']['status'] in {'loaded','error','timeout','empty','placeholder'} for x in audit['results'])
expected={(f['id'],k) for f in records for k in ('portrait','visual') if f[k]['registered']}
assert set(keys)==expected
assert all('France browser' not in x.get('environment','') or 'NOT a France browser' in x['environment'] for x in [audit])

# Verify that every curated repair is present only in the intended sidecar.
sidecar=(root/'data/portraits-v49d.js').read_text(encoding='utf-8')
match=re.search(r'window\.SHINO_PORTRAITS_V49D\s*=\s*(\[.*?\]);',sidecar,re.S)
assert match, "missing curated portrait sidecar"
repairs=json.loads(match.group(1))
assert len(repairs)==28 and len({x['id'] for x in repairs})==28
assert sum(not x['previous_portrait'] for x in repairs)==2
assert any(x['id']=='akuma-no-mi' and x['portrait_kind']=='silhouette-anime' for x in repairs)
assert any(x['id']=='fruit-artificiel-seiryu' and x['portrait_kind']=='illustration-anime' for x in repairs)
assert all(x['portrait'].startswith('https://static.wikia.nocookie.net/onepiece/images/')
           and x['portrait_file'].endswith('.png') and x['portrait_evidence'].startswith('https://onepiece.fandom.com/wiki/File:')
           for x in repairs)
assert "corrected.previous_portrait" in sidecar, "repairs must not clobber newer data"
for file in ('index.html','media-check.html'):
    content=(root/file).read_text(encoding='utf-8')
    assert 'data/portraits-v49d.js?v=4.9d' in content, file+' did not load media corrections'

# Test the actual MEDIA CHECK inline JavaScript, not only its HTML.
media=(root/'media-check.html').read_text(encoding='utf-8')
assert "const getItems=()=>all.flatMap" in media
assert "reason:'missing-reference'" in media
assert "img.naturalWidth===300&&img.naturalHeight===171" in media
assert "slots:getItems().length" in media
assert "demonfruitzdex.media-browser-review.v49d" in media
assert "function check(url,alt,type)" in media

class InlineScript(HTMLParser):
    def __init__(self):
        super().__init__();self.active=False;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script':self.active=not dict(attrs).get('src')
    def handle_data(self,value):
        if self.active:self.parts.append(value)
    def handle_endtag(self,tag):
        if tag=='script':self.active=False
parser=InlineScript();parser.feed(media)
js='\n'.join(parser.parts)
parsed=subprocess.run(['node','--check','-'],input=js,text=True,capture_output=True)
assert parsed.returncode==0,parsed.stderr
print('PASS V4.9.d: 28 curated unique portrait replacements and MEDIA CHECK JavaScript syntax')

print('PASS V4.9.d: complete 166-fruit / 304-reference browser audit, structural coverage and honest status tags')
print('BROWSER OBSERVATIONS (NOT GLOBAL LINK VERDICT):',audit['outcomes'])
