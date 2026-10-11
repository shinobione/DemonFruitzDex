#!/usr/bin/env node
'use strict';
// Validate the actual HTML script order, guard semantics, baseline parity and evidence coverage.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=file=>fs.readFileSync(path.join(root,file),'utf8');
const manifest=JSON.parse(read('reports/illustration-evidence-v49e.json'));
const backlog=JSON.parse(read('reports/media-illustration-backlog-v49d2.json')).items;
const overlay='data/power-art-v49e.js';
const scripts=html=>[...html.matchAll(/<script\b[^>]*src="([^"?]+)(?:\?[^\"]*)?"[^>]*>/g)].map(x=>x[1]).filter(x=>x.startsWith('data/'));
const indexScripts=scripts(read('index.html')),checkScripts=scripts(read('media-check.html'));
assert.deepEqual(checkScripts,indexScripts.filter(x=>x!=='data/clips.js'));
assert.equal(indexScripts.filter(x=>x===overlay).length,1);
assert(indexScripts.indexOf(overlay)>indexScripts.indexOf('data/power-art-v48.js'));
const context=vm.createContext({window:{}});
for(const file of indexScripts.filter(x=>x!==overlay))vm.runInContext(read(file),context,{filename:file,timeout:5000});
const plain=x=>JSON.parse(JSON.stringify(x));
const baseline=plain(context.window.SHINO_DATA),clips=plain(context.window.SHINO_CLIPS);
assert.equal(baseline.length,166);
assert.equal(baseline.filter(f=>f.image).length,140);
assert.equal(baseline.filter(f=>f.portrait).length,164);
const videoCount=Object.values(clips).reduce((n,c)=>n+(c.youtubeId?1:0)+(c.moreVideos||[]).length,0);
assert.equal(videoCount,50);
vm.runInContext(read(overlay),context,{filename:overlay,timeout:5000});
const additions=plain(context.window.SHINO_POWER_ART_V49E),effective=plain(context.window.SHINO_DATA);
const allowed=new Set(['file','image','visual','image_kind','visual_description','visual_provenance','visual_proof','visual_credit','visual_canon_note','visual_rights','visual_validation']);
const kinds=new Set(['pouvoir-action-anime','pouvoir-action-manga','transformation-zoan-anime','transformation-zoan-manga','transformation-arme-manga','explication-pouvoir-manga','manifestation-pouvoir-anime','transformation-avenir-anime']);
const ids=new Set(additions.map(a=>a.id));
assert.equal(ids.size,12);assert.equal(additions.length,12);
assert.equal(effective.filter(f=>f.image).length,152);
assert.equal(effective.filter(f=>f.portrait).length,164);
assert.deepEqual(plain(context.window.SHINO_CLIPS),clips);
for(const art of additions){
  assert.equal(art.previous_image,null);assert.equal(art.file,null);assert.equal(art.visual,'pouvoir');
  assert(kinds.has(art.image_kind));
  assert.equal(art.visual_rights,'copyright-external-reference-only');
  assert(art.visual_credit.includes('Shueisha'));
  assert(art.visual_description&&art.visual_canon_note&&art.visual_validation);
  for(const key of Object.keys(art))assert(key==='id'||key==='previous_image'||allowed.has(key),key);
  for(const key of ['image','visual_provenance','visual_proof']){
    const url=new URL(art[key]);assert.equal(url.protocol,'https:');
    assert(!url.pathname.includes('/watch/'),'No full episodes');
  }
  assert.equal(new URL(art.visual_proof).hostname,'one-piece.com');
  const before=baseline.find(f=>f.id===art.id);assert(before&&!before.image);
  assert(backlog.some(f=>f.id===art.id));
}
for(let i=0;i<baseline.length;i++){
  const before=baseline[i],after=effective[i];assert.equal(before.id,after.id);
  if(!ids.has(before.id))assert.deepEqual(after,before,'Unrelated fruit changed: '+before.id);
  else{
    const expected={...before};const {id,previous_image,...fields}=additions.find(a=>a.id===before.id);
    Object.assign(expected,fields);assert.deepEqual(after,expected);
  }
}
// Replay is idempotent; an unexpected existing image must prevent ALL metadata changes.
vm.runInContext(read(overlay),context,{timeout:5000});assert.deepEqual(plain(context.window.SHINO_DATA),effective);
const newer=vm.createContext({window:{SHINO_DATA:plain(baseline)}});
for(const fruit of newer.window.SHINO_DATA)if(ids.has(fruit.id)){fruit.image='https://example.invalid/newer.png';fruit.visual_description='Newer editorial review';}
const preserved=plain(newer.window.SHINO_DATA);vm.runInContext(read(overlay),newer,{timeout:5000});
assert.deepEqual(plain(newer.window.SHINO_DATA),preserved);
const unguarded=vm.createContext({window:{SHINO_DATA:plain(baseline)}});
vm.runInContext(read(overlay).replace('"previous_image": null,',''),unguarded,{timeout:5000});
assert.deepEqual(plain(unguarded.window.SHINO_DATA.find(f=>f.id===additions[0].id)),baseline.find(f=>f.id===additions[0].id));
vm.runInNewContext(read(overlay),{window:{}},{timeout:5000});
assert.equal(manifest.decisions.length,26);
assert.deepEqual(manifest.decisions.map(x=>x.id).sort(),backlog.map(x=>x.id).sort());
assert.deepEqual(manifest.decisions.filter(x=>x.decision==='added').map(x=>x.id).sort(),[...ids].sort());
assert.equal(manifest.decisions.filter(x=>x.decision==='held').length,14);
assert(manifest.decisions.every(x=>x.physicalFruitDepicted===false));
for(const decision of manifest.decisions){
  assert.equal(decision.priority,backlog.find(x=>x.id===decision.id).priority);
  const f=effective.find(x=>x.id===decision.id);
  if(decision.decision==='held'){assert(!f.image);assert(decision.reason);}
  else{assert.equal(f.image,decision.image);assert.equal(f.image_kind,decision.imageKind);assert(decision.browser.width>0&&decision.browser.height>0);assert(/^[0-9a-f]{16}$/.test(decision.reviewedDhash64));assert(decision.visualReview);}
}
assert.equal(manifest.rightsPolicy.originalsDownloaded,false);
assert.equal(manifest.rightsPolicy.originalsRehosted,false);
assert.equal(manifest.rightsPolicy.publicReuseAuthorized,false);
assert.equal(manifest.base.head,'0a42057158a00a2175b835a7f91c72221a889165');
assert.deepEqual(manifest.counts,{fruits:166,portraits:164,videos:50,baselineArt:140,baselineMissing:26,added:12,effectiveArt:152,remaining:14});
console.log('PASS V4.9.e: 12 guarded additions / 14 held; exact 166-fruit, 164-portrait, 50-video parity; 26/26 evidence decisions; no rehosted originals.');
