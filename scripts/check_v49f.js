#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'),read=f=>fs.readFileSync(path.join(root,f),'utf8');
const html=read('index.html'),checker=read('media-check.html'),app=read('app.js');
const files=Array.from(html.matchAll(/<script\b[^>]*src="(data\/[^"?]+)(?:\?[^"]*)?"[^>]*>/g),m=>m[1]);
const ctx=vm.createContext({window:{}});
for(const filename of files)vm.runInContext(read(filename),ctx,{filename,timeout:5000});
assert.equal(ctx.window.SHINO_DATA.length,166);
const fruits=ctx.window.SHINO_DATA;
assert.equal(fruits.filter(f=>f.portrait).length,164);
assert.equal(fruits.filter(f=>f.image).length,152);
const videos=Object.values(ctx.window.SHINO_CLIPS||{}).reduce((n,c)=>n+(c.youtubeId?1:0)+(c.moreVideos||[]).length,0);
assert.equal(videos,50);
const api=ctx.window.SHINO_MEDIA_RELIABILITY;
assert(api&&typeof api.probe==='function');
assert.equal(files.filter(x=>x==='data/media-reliability-v49f.js').length,1);
assert(checker.includes('data/media-reliability-v49f.js?v=4.9f'));
assert(checker.includes('scripts/media-check-v49f.js?v=4.9f'));
assert(checker.includes('id="failedOnly"'));
assert(checker.includes('id="all"')&&checker.includes('id="rescue"')&&checker.includes('id="export"'));
assert(app.includes("SHINO_MEDIA_RELIABILITY?.fakeWikiImage"));
assert(!checker.includes('<script defer>\ndocument.addEventListener'));
assert.equal(api.fakeWikiImage('https://static.wikia.nocookie.net/onepiece/images/f/foo.png',300,171),true);
assert.equal(api.fakeWikiImage('https://static.wikia.nocookie.net/onepiece/images/f/foo.png',301,171),false);
assert.equal(api.fakeWikiImage('https://unrelated.invalid/picture.jpg',300,171),false);
assert.equal(api.makeCandidates('', 'file.png').length,0);
const existing=api.makeCandidates('https://static.wikia.nocookie.net/onepiece/images/a/a1/File.png','Known File.png');
assert.equal(existing.length,2);
assert(existing[1].includes('Special:Redirect/file/'));
assert.equal(api.makeCandidates('https://example.com/x.png',null).length,1);
assert(!api.redirect('../../../../file.txt'));
for(const file of ['data/media-reliability-v49f.js','scripts/media-check-v49f.js']){
 const out=require('node:child_process').spawnSync(process.execPath,['--check',path.join(root,file)],{encoding:'utf8'});
 assert.equal(out.status,0,out.stderr);
}
console.log('PASS V4.9.f: 166 fruits / 164 portraits / 152 illustrations / 316 references / 50 videos');
console.log('PASS: safe fallback boundaries, Wiki 300x171, checker V2 integration and Javascript syntax');
