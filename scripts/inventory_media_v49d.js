#!/usr/bin/env node
'use strict';
// Freeze the V4.9.d baseline, before the V4.9.e illustration overlay.
// No external connections, no image downloads and no data rewrites.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'),context={window:{}};
vm.createContext(context);
for(const script of ['data/fruits.js','data/portrait-sources.js','data/portraits-v48.js','data/portraits-v49.js','data/portraits-v49d.js','data/power-art-v48.js']){
  vm.runInContext(fs.readFileSync(path.join(root,script),'utf8'),context,{filename:script,timeout:5000});
}
const rows=context.window.SHINO_DATA;
if(!Array.isArray(rows)||rows.length!==166)throw Error('Expected 166 effective fruit entries');
const ids=new Set();
const records=rows.map((f,i)=>{
 if(!f.id||ids.has(f.id))throw Error('Duplicate/missing fruit '+f.id);ids.add(f.id);
 const resource=(kind,url,filename,extra)=>({
   registered:!!url,url:url||null,filename:filename||null,
   fallback:filename&&/\.(png|jpg|jpeg|webp|gif)$/i.test(filename)
      ?'https://onepiece.fandom.com/wiki/Special:Redirect/file/'+encodeURIComponent(filename.replaceAll(' ','_')):null,
   ...extra
 });
 return {index:i,id:f.id,name:f.n||'',label:f.fr||'',holder:f.primary_user||f.u||'',family:f.t||'',
  portrait:resource('portrait',f.portrait,f.portrait_file,{origin:f.portrait_source||'uncatalogued',kind:f.portrait_kind||null}),
  visual:resource('visual',f.image,f.file,{type:f.visual||null,kind:f.image_kind||null}),
  substitution:!f.image&&!!f.portrait&&f.id!=='smile',
 };
});
const stats={entries:records.length,portraitRegistered:records.filter(x=>x.portrait.registered).length,
 visualRegistered:records.filter(x=>x.visual.registered).length,
 noPortrait:records.filter(x=>!x.portrait.registered).length,
 noVisual:records.filter(x=>!x.visual.registered).length,
 directReferences:records.reduce((n,x)=>n+ +x.portrait.registered+ +x.visual.registered,0)};
if(stats.portraitRegistered!==164||stats.visualRegistered!==140)throw Error('Regression in media counts: '+JSON.stringify(stats));
const result={schema:'demonfruitzdex.media-inventory.v49d',generatedAt:new Date().toISOString(),
 sourceFiles:['data/fruits.js','data/portrait-sources.js','data/portraits-v48.js','data/portraits-v49.js','data/portraits-v49d.js','data/power-art-v48.js'],
 disclaimer:'registered URLs are not verified to load; browser test is a separate report; remote art not licensed for redistribution',
 stats,records};
fs.mkdirSync(path.join(root,'reports'),{recursive:true});
fs.writeFileSync(path.join(root,'reports/media-inventory-v49d.json'),JSON.stringify(result,null,2)+'\n');
console.log('MEDIA_INVENTORY_STATS='+JSON.stringify(stats));
console.log('MEDIA_MISSING_PORTRAITS='+JSON.stringify(records.filter(x=>!x.portrait.registered).map(x=>({id:x.id,name:x.holder}))));
console.log('MEDIA_MISSING_VISUALS='+JSON.stringify(records.filter(x=>!x.visual.registered).map(x=>x.id)));
