#!/usr/bin/env python3
"""Fail CI for incomplete audits and corrupt data, not for third-party host blocks."""
from pathlib import Path
import json

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
print('PASS V4.9.d: complete 166-fruit / 304-reference browser audit, structural coverage and honest status tags')
print('BROWSER OBSERVATIONS (NOT GLOBAL LINK VERDICT):',audit['outcomes'])
