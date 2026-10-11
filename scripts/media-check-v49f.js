/* V4.9.f MEDIA CHECK V2 — audit 316 referenced images + 16 absent slots.
 * Browser decode only, never global validity, CORS evidence or copyright permission. */
document.addEventListener('DOMContentLoaded',()=>{
 'use strict';
 const $=id=>document.getElementById(id);
 const all=Array.isArray(window.SHINO_DATA)?window.SHINO_DATA:[];
 const core=window.SHINO_MEDIA_RELIABILITY;
 const tbody=$('rows'),status=$('summary'),progress=$('progress');
 const runSample=$('sample'),runAll=$('all'),runRescue=$('rescue'),exporter=$('export'),failOnly=$('failedOnly');
 if(!core){status.textContent='MODULE MEDIA RELIABILITY NON CHARGÉ';return}
 let running=false,results=[];
 const safe=x=>String(x??'');
 const getItems=()=>all.flatMap(f=>[
  {id:f.id,fruit:f.fr,type:'portrait',url:f.portrait||'',filename:f.portrait_file||null,imageKind:f.portrait_kind||'portrait',provenance:f.portrait_evidence||null},
  {id:f.id,fruit:f.fr,type:'art',url:f.image||'',filename:f.file||null,imageKind:f.image_kind||'illustration',provenance:f.visual_provenance||null}
 ].map(item=>({...item,missing:!item.url})));
 const labels={'direct-loaded':'VISIBLE','fallback-loaded':'VISIBLE VIA REDIRECTION',
  'not-referenced':'NON RÉFÉRENCÉ','timeout-unconfirmed':'DÉLAI DÉPASSÉ · INCERTAIN',
  'wiki-placeholder':'FAUSSE IMAGE WIKI','browser-load-failed':'ÉCHEC SUR CE NAVIGATEUR'};
 const failed=x=>!['direct-loaded','fallback-loaded'].includes(x.status);
 const create=(tag,content)=>{const e=document.createElement(tag);if(content!==undefined)e.textContent=safe(content);return e};
 function render(){
  tbody.replaceChildren();
  const subset=failOnly.checked?results.filter(failed):results;
  const fragment=document.createDocumentFragment();
  for(const entry of subset){
   const tr=create('tr');
   const state=labels[entry.status]||entry.status;
   const attempts=entry.attempts||[];
   const diag=entry.status==='not-referenced'?'Aucune URL':
      attempts.map(a=>a.kind+': '+a.status+(a.status==='loaded'?' '+a.width+'×'+a.height:'')).join(' → ');
   [entry.imageKind||entry.type,entry.fruit,state,diag].forEach((v,i)=>{
    const td=create('td',v);
    if(i===2)td.className=entry.status==='not-referenced'?'pending':failed(entry)?'failed':'ok';
    tr.append(td);
   });
   const td=create('td'),primary=entry.selected||entry.url;
   if(primary){
    const link=create('a','Voir image');link.href=primary;link.target='_blank';link.rel='noopener noreferrer';td.append(link);
   }else td.textContent='—';
   if(entry.provenance){
    const source=create('a',' · Source');source.href=entry.provenance;source.target='_blank';source.rel='noopener noreferrer';td.append(source);
   }
   tr.append(td);fragment.append(tr);
  }
  tbody.append(fragment);
 }
 function summary(){
  const counts={loaded:results.filter(x=>x.status==='direct-loaded').length,
    rescue:results.filter(x=>x.status==='fallback-loaded').length,
    missing:results.filter(x=>x.status==='not-referenced').length,
    failed:results.filter(x=>failed(x)&&x.status!=='not-referenced').length};
  status.textContent=results.length+' / 332 contrôlés · '+counts.loaded+' directs · '+counts.rescue+' via repli · '+counts.missing+' absents · '+counts.failed+' échecs/indéterminés dans CE navigateur';
 }
 async function launch(sample){
  if(running)return;
  running=true;results=[];tbody.replaceChildren();exporter.disabled=true;
  runSample.disabled=runAll.disabled=runRescue.disabled=true;
  let items=getItems();
  if(sample==='rescue'){
   const ids=new Set((window.SHINO_POWER_ART_V49E||[]).map(x=>x.id));
   items=items.filter(x=>x.type==='art'&&ids.has(x.id));
  }else if(sample){
   const favs=new Set([...(window.SHINO_PORTRAITS_V49||[]),...(window.SHINO_EXTRA_PORTRAITS||[])].map(x=>x.id));
   items=[...items.filter(x=>x.missing),
     ...items.filter(x=>!x.missing&&favs.has(x.id)),
     ...items.filter(x=>!x.missing&&!favs.has(x.id))].slice(0,30);
  }
  progress.max=Math.max(1,items.length);progress.value=0;
  let cursor=0;const values=new Array(items.length);
  async function worker(){
   while(cursor<items.length){
    const i=cursor++,item=items[i],probe=await core.probe({url:item.url,filename:item.filename},{timeout:6500});
    const imageResult=probe.attempts.find(a=>a.status==='loaded')||probe.attempts[probe.attempts.length-1];
    values[i]={...item,...probe,ok:probe.status==='direct-loaded'||probe.status==='fallback-loaded',
     width:imageResult?.width||0,height:imageResult?.height||0,
     final:probe.selected||item.url,reason:probe.status};
    progress.value=values.filter(Boolean).length;
   }
  }
  try{
   await Promise.all(Array.from({length:Math.min(8,items.length)},worker));
   results=values;summary();render();exporter.disabled=false;
  }catch(err){status.textContent='Erreur locale pendant l’audit : '+safe(err?.message||err)}
  finally{running=false;runSample.disabled=runAll.disabled=runRescue.disabled=false}
 }
 runSample.onclick=()=>launch(true);
 runAll.onclick=()=>launch(false);
 runRescue.onclick=()=>launch('rescue');
 failOnly.onchange=render;
 exporter.onclick=()=>{
  if(!results.length)return;
  const payload={schema:'demonfruitzdex.media-browser-review.v49d',revision:'v49f-media-check-v2',
   date:new Date().toISOString(),origin:location.origin,userAgent:navigator.userAgent,
   scope:{fruits:all.length,slots:getItems().length,examined:results.length},
   note:'Résultats limités à CE navigateur. Les erreurs peuvent venir de restrictions CDN/réseau/région. Aucune image chargée n’est automatiquement considérée canonique ni autorisée à être redistribuée. Aucune prétention sur CORS.',
   outcomes:Object.fromEntries([...new Set(results.map(x=>x.status))].map(k=>[k,results.filter(x=>x.status===k).length])),results};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json;charset=utf-8'});
  const u=URL.createObjectURL(blob),a=create('a');
  a.href=u;a.download='demonfruitzdex-media-v49f-'+new Date().toISOString().slice(0,10)+'.json';
  document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);
 };
 const refs=getItems().filter(x=>!x.missing).length;
 status.textContent='MEDIA CHECK V2 · '+all.length+' fiches · '+refs+' URL référencées · '+(all.length*2-refs)+' emplacements sans image. Tests réseau uniquement sur demande.';
});