#!/usr/bin/env node
'use strict';
// Effective catalogue INCLUDING portrait and power-image sidecars as loaded by index.html.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const dataScripts=[...html.matchAll(/<script\b[^>]*src="(data\/[^"?]+)(?:\?[^"]*)?"[^>]*>/g)].map(x=>x[1]);
const ctx=vm.createContext({window:{}});
for(const file of dataScripts)vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file,timeout:5000});
const rows=ctx.window.SHINO_DATA;
if(!Array.isArray(rows)||rows.length!==166)throw Error('Effective catalogue must contain 166 fruits');
const unique=new Set();
const records=rows.map(f=>{
  if(!f.id||unique.has(f.id))throw Error('Missing or duplicate fruit ID: '+f.id);
  unique.add(f.id);
  const media=(kind,url,filename,metadata)=>({
    kind,url:url||null,filename:filename||null,referenced:!!url,...metadata
  });
  return {id:f.id,name:f.fr,holder:f.primary_user||f.u,
    portrait:media('portrait',f.portrait,f.portrait_file,{source:f.portrait_source||null,provenance:f.portrait_evidence||null}),
    art:media('art',f.image,f.file,{source:f.visual_credit||null,provenance:f.visual_provenance||null,image_kind:f.image_kind||null})};
});
const stats={fruitCount:records.length,
 portraitCount:records.filter(x=>x.portrait.referenced).length,
 artCount:records.filter(x=>x.art.referenced).length,
 registeredImages:records.reduce((n,x)=>n+(x.portrait.referenced?1:0)+(x.art.referenced?1:0),0),
 missingSlots:records.reduce((n,x)=>n+(!x.portrait.referenced?1:0)+(!x.art.referenced?1:0),0)};
if(JSON.stringify(stats)!==JSON.stringify({fruitCount:166,portraitCount:164,artCount:152,registeredImages:316,missingSlots:16}))
 throw Error('Unexpected baseline totals '+JSON.stringify(stats));
const out={schema:'demonfruitzdex.media-inventory.v49f',generatedAt:new Date().toISOString(),sources:dataScripts,stats,records};
fs.mkdirSync(path.join(root,'reports'),{recursive:true});
fs.writeFileSync(path.join(root,'reports/media-inventory-v49f.json'),JSON.stringify(out,null,2)+'\n');
console.log('MEDIA_INVENTORY='+JSON.stringify(stats));
