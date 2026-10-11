/* V4.9.g — evidence-first clip discovery board, zero automatic YouTube imports.
 * Existing CLIP CHECK owns the local proposals; this page only guides research. */
(function(){
 'use strict';
 const F=window.SHINO_DATA, C=window.SHINO_CLIPS;
 if(!Array.isArray(F)||!C)return;
 const $=id=>document.getElementById(id);
 const observed=new Set();
 const ranked=new Set([
  'mera-mera-no-mi','bara-bara-no-mi','zushi-zushi-no-mi',
  'mero-mero-no-mi','inu-inu-no-mi-mod-le-okuchi-no-makami',
  'susu-susu-no-mi','numa-numa-no-mi','baku-baku-no-mi',
  'hito-hito-no-mi-mod-le-daibutsu','hobi-hobi-no-mi',
  'buki-buki-no-mi','fuwa-fuwa-no-mi','shiro-shiro-no-mi',
  'awa-awa-no-mi','kira-kira-no-mi','bane-bane-no-mi',
  'riki-riki-no-mi','fude-fude-no-mi','giro-giro-no-mi'
 ]);
 const unknown=f=>f.t==='Indéterminé'||f.t==='Technologie'||f.t==='Artificiel'||f.id.startsWith('fruit-mythique-');
 const videos=e=>(e&&e.youtubeId?[e]:[]).concat(e?.moreVideos||[]).filter(v=>/^[\w-]{11}$/.test(v.youtubeId||''));
 const count=Object.values(C).reduce((n,e)=>n+videos(e).length,0);
 const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const priority=f=>ranked.has(f.id)?'A':unknown(f)?'C':'B';
 const rows=F.map(f=>({
  id:f.id,fruit:f.fr||f.n,user:f.primary_user||f.u||'Utilisateur non confirmé',type:f.t,
  videos:videos(C[f.id]).length,priority:priority(f)
 })).sort((a,b)=>a.priority.localeCompare(b.priority)||a.fruit.localeCompare(b.fruit,'fr'));
 const missing=rows.filter(r=>r.videos===0);
 $('statFruits').textContent=String(rows.length);
 $('statVideos').textContent=String(count);
 $('statCovered').textContent=String(rows.length-missing.length);
 $('statMissing').textContent=String(missing.length);
 const allProposals=(()=>{
  try {
   const c=JSON.parse(localStorage.getItem('demonfruitzdex.clip-proposals.v49b')||'{}');
   return c&&typeof c==='object'&&!Array.isArray(c)?c:{};
  }catch(_){return {}}
 })();
 const proposalCounts={};
 for(const value of Object.values(allProposals)){
  if(value&&value.fruitId&&/^[\w-]{11}$/.test(value.videoId||''))
   proposalCounts[value.fruitId]=(proposalCounts[value.fruitId]||0)+1;
 }
 const searchTerms=r=>['One Piece',r.user,'devil fruit',r.fruit,'power ability anime clip'].join(' ');
 const link=(href,title)=>{
  const a=document.createElement('a');a.href=href;a.textContent=title;
  a.rel='noopener noreferrer';return a;
 };
 const selected=()=>{
  const q=norm($('query').value.trim());
  return rows.filter(r=>($('filter').value==='all'||$('filter').value==='missing'&&r.videos===0||$('filter').value==='covered'&&r.videos>0)
    &&($('tier').value==='all'||$('tier').value===r.priority)
    &&(!q||norm([r.fruit,r.user,r.type,r.id].join(' ')).includes(q)));
 };
 function render(){
  const filtered=selected();const tbody=$('rows'),fragment=document.createDocumentFragment();
  tbody.replaceChildren();
  for(const r of filtered){
   const tr=document.createElement('tr');
   const pr=document.createElement('td'),badge=document.createElement('span');
   badge.className='priority';badge.dataset.grade=r.priority;badge.textContent=r.priority;pr.append(badge);
   const fruit=document.createElement('td'),strong=document.createElement('strong');
   strong.textContent=r.fruit;fruit.append(strong);
   const user=document.createElement('td');user.textContent=r.user;
   const state=document.createElement('td'),stateText=document.createElement('span');
   stateText.className='state';
   const proposed=proposalCounts[r.id]||0;
   stateText.textContent=r.videos?String(r.videos)+' vidéo(s) sélectionnée(s)':
    'Aucun clip'+(proposed?' · '+proposed+' proposition(s) locale(s)':'');
   state.append(stateText);
   const td=document.createElement('td'),actions=document.createElement('div');
   actions.className='buttonline';
   actions.append(link('https://www.youtube.com/results?search_query='+encodeURIComponent(searchTerms(r)),'⌕ Chercher sur YouTube'));
   actions.append(link('clip-check.html?fruit='+encodeURIComponent(r.id)+'&suggest=1','＋ Proposer / vérifier'));
   actions.append(link('index.html?fruit='+encodeURIComponent(r.id),'↗ Voir la fiche'));
   td.append(actions);
   for(const cell of [pr,fruit,user,state,td])tr.append(cell);
   fragment.append(tr);
  }
  tbody.append(fragment);
  $('results').textContent=filtered.length+' fiche(s) affichée(s). '+missing.length+' fruits sans extrait sélectionné dans le catalogue ; les recherches ne garantissent pas un extrait librement consultable.';
 }
 function exportBacklog(){
  const entries=selected().map(r=>({
   fruitId:r.id,fruit:r.fruit,user:r.user,priority:r.priority,
   selectedVideos:r.videos,localProposals:proposalCounts[r.id]||0,
   youtubeSearch:'https://www.youtube.com/results?search_query='+encodeURIComponent(searchTerms(r)),
   reviewStatus:r.videos?'published-association-needs-browser-review':'source-research-needed'
  }));
  const payload={schema:'demonfruitzdex.clip-discovery.v49g',
   generatedAt:new Date().toISOString(),totals:{fruits:rows.length,clips:count,covered:rows.length-missing.length,uncovered:missing.length},
   note:'YouTube search URLs are NOT vetted clips. No video IDs are invented. Playback, legality, clip scope and attribution require human checks.',
   items:entries};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json;charset=utf-8'});
  const url=URL.createObjectURL(blob),a=link(url,'');
  a.download='demonfruitzdex-clip-discovery-v49g.json';a.hidden=true;document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1500);
 }
 for(const el of ['query','filter','tier'])$(el).addEventListener(el==='query'?'input':'change',render);
 $('export').addEventListener('click',exportBacklog);
 render();
 window.SHINO_CLIP_FINDER_AUDIT=Object.freeze({fruits:rows.length,clips:count,covered:rows.length-missing.length,uncovered:missing.length});
})();