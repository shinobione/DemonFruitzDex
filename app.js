/* DemonFruitzDex V4.9.b — curated YouTube power clips with provenance. */
(() => {
  'use strict';
  const fruits = Array.isArray(window.SHINO_DATA) ? window.SHINO_DATA : [];
  const $ = (id) => document.getElementById(id);
  const colors = {Logia:'#55c0ec','Zoan Mythique':'#a77cff','Zoan Ancien':'#fd985a',Zoan:'#65cf99',Paramecia:'#ee89a9','Indéterminé':'#f4c36b',Artificiel:'#f4c36b',Technologie:'#7edbcf'};
  const tiers = ['S+','S','A','B','C'];
  const enc = (str) => String(str ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (str) => String(str ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const canonicalType = (t) => String(t).startsWith('Zoan') ? 'Zoan' : t === 'Logia' ? 'Logia' : t === 'Paramecia' ? 'Paramecia' : 'Indéterminé';
  const mainIds = fruits.map(f=>f.id);
  const byId = new Map(fruits.map(f=>[f.id, f]));
  const clips = window.SHINO_CLIPS || {}; // source references, not media re-uploads
  const clipVideos = (entry) => entry ? [...(entry.youtubeId ? [entry] : []), ...(entry.moreVideos || [])] : [];
  const videoProvenance = (video) => {
    if (video?.verificationStatus === 'public-metadata-verified') return `${video?.contentKind === 'compilation' ? 'MONTAGE D’ATTAQUES' : 'EXTRAIT DE L’ANIMÉ'} · CHAÎNE COMMUNAUTAIRE ${String(video.channel||'').toUpperCase()} · MÉTADONNÉES RECENSÉES · LECTURE/INTÉGRATION NON TESTÉES`;
    if (video?.contentKind === 'live-action') return 'ADAPTATION NETFLIX LIVE-ACTION · PAS UNE SCÈNE DE L’ANIMÉ · LECTURE NON TESTÉE';
    if (video?.verificationStatus === 'legacy-unverified') return 'ANCIEN CLIP · PROVENANCE À CONFIRMER · LECTURE NON TESTÉE';
    if (video?.contentKind === 'preview') return 'BANDE-ANNONCE OFFICIELLE · PAS UN EXTRAIT DE POUVOIR';
    if (video?.verificationStatus === 'publisher-metadata-verified') return `SOURCE ${String(video.channel||'DIFFUSEUR').toUpperCase()} IDENTIFIÉE · LECTURE NON TESTÉE`;
    if (video?.sourceEvidence) return 'PUBLICATION DU DIFFUSEUR RÉFÉRENCÉE · LECTURE NON TESTÉE';
    return 'EXTRAIT CATALOGUÉ · PROVENANCE À RECONTRÔLER';
  };
  const hasYoutube = (id) => clipVideos(clips[id]).length > 0;
  const hasScene = hasYoutube;
  const motionLabels = {fire:'Flammes',magma:'Magma',lightning:'Éclairs',darkness:'Ténèbres',ice:'Glace',gravity:'Gravité',rubber:'Élasticité',room:'Espace',magnet:'Magnétisme',nature:'Végétation',sand:'Sable',smoke:'Fumée',quake:'Onde de choc',petals:'Éclosion',strings:'Fils',repulse:'Répulsion',barrier:'Barrière',toxin:'Toxines',time:'Temps',ghost:'Fantômes',heart:'Émotions',toy:'Métamorphose',dragon:'Dragon',beast:'Transformation',light:'Lumière'};
  const state = {search:'',type:'all',tier:'',sort:'default',awake:false,favoritesOnly:false,illustrated:false,videosOnly:false,reviewOnly:false,display:24,all:fruits,compare:[],active:null,motionRunning:true,animId:null,animStarted:0,animCanvas:null,video:null,videoFailed:false};
  const storageKey='demonfruitzdex.favorites.v4';
  let favorites = new Set();
  try { const raw=JSON.parse(localStorage.getItem(storageKey)||'[]'); if(Array.isArray(raw)) favorites=new Set(raw.filter(id=>byId.has(id))); }catch(_){}
  let notifyTimeout;
  function toast(message){const t=$('toast');t.textContent=message;t.classList.add('show');clearTimeout(notifyTimeout);notifyTimeout=setTimeout(()=>t.classList.remove('show'),2500)}
  function persist(){try{localStorage.setItem(storageKey,JSON.stringify([...favorites]));}catch(_){} $('favoriteCount').textContent=favorites.size;}
  function toggleFavorite(id){if(favorites.has(id)){favorites.delete(id);toast('Retiré des favoris')}else{favorites.add(id);toast('Ajouté aux favoris ♡')}persist();updateCards();if(state.active===id)refreshDetailActions();}
  function selectCompare(id){const i=state.compare.indexOf(id);if(i!==-1){state.compare.splice(i,1)}else if(state.compare.length>=2){toast('Choisis deux Fruits maximum');return;}else{state.compare.push(id)}updateDock();updateCards();if(state.active===id)refreshDetailActions();}
  function updateDock(){const size=state.compare.length;$('compareDock').hidden=size===0;$('compareCount').textContent=`${size} / 2`;$('compareOpen').disabled=size!==2;}
  function filters(){
    const query=norm(state.search.trim());
    const a=fruits.filter(f=>{
      if(query && !norm([f.fr,f.n,f.u,f.primary_user,f.p,f.t].join(' ')).includes(query))return false;
      if(state.type!=='all' && canonicalType(f.t)!==state.type)return false;
      if(state.tier && f.r!==state.tier)return false;
      if(state.awake && !f.w)return false;
      if(state.favoritesOnly && !favorites.has(f.id))return false;
      if(state.illustrated && !f.image)return false;
      if(state.videosOnly && !hasScene(f.id))return false;
      if(state.reviewOnly && !clips[f.id]?.auditV46)return false;
      return true;
    });
    if(state.sort==='az')a.sort((a,b)=>a.fr.localeCompare(b.fr,'fr'));
    if(state.sort==='za')a.sort((a,b)=>b.fr.localeCompare(a.fr,'fr'));
    if(state.sort==='tier')a.sort((a,b)=>tiers.indexOf(a.r)-tiers.indexOf(b.r)||a.fr.localeCompare(b.fr,'fr'));
    if(state.sort==='awake')a.sort((a,b)=>Number(b.w)-Number(a.w)||a.fr.localeCompare(b.fr,'fr'));
    if(state.sort==='clips')a.sort((a,b)=>Number(hasYoutube(b.id))-Number(hasYoutube(a.id))||Number(hasScene(b.id))-Number(hasScene(a.id))||a.fr.localeCompare(b.fr,'fr'));
    return a;
  }
  const wikiRedirect=(filename)=> filename && /\\.(png|jpg|jpeg|webp|gif)$/i.test(filename) ? 'https://onepiece.fandom.com/wiki/Special:Redirect/file/'+encodeURIComponent(filename.replaceAll(' ','_')) : '';
  // A remote URL in the catalogue is not proof that the image is viewable.
  // Try the wiki's named-file redirect once, then show the styled fallback.
  document.addEventListener('error',e=>{
    const img=e.target;
    if(!(img instanceof HTMLImageElement) || !img.matches('[data-media-fallback]'))return;
    const alternative=img.dataset.mediaFallback;
    if(alternative && img.dataset.retry!=='1' && alternative!==img.src){
      img.dataset.retry='1';img.src=alternative;return;
    }
    const frame=img.closest('.portrait-frame,.card-visual,.detail-fruit-mini,.compare-fruit');
    if(frame){frame.classList.add('media-unavailable');const badge=frame.querySelector('.art-meta');if(badge)badge.textContent='IMAGE EXTERNE INDISPONIBLE';}
    img.remove();
  },true);
  function portrait(f, large=false){const name=enc(f.primary_user||f.u);return `<div class="portrait-frame ${large?'portrait-large':''}" style="--accent:${colors[f.t]||'#9d77fc'}" title="Portrait : ${name}"><span>${enc(f.avatar||'OP')}</span>${f.portrait?`<img loading="lazy" alt="Portrait de ${name}" src="${enc(f.portrait)}" data-media-fallback="${enc(wikiRedirect(f.portrait_file))}" referrerpolicy="no-referrer">`:''}</div>`}
  function art(f, modal=false){
    if(f.image)return `<img class="artwork" loading="lazy" decoding="async" referrerpolicy="no-referrer" alt="Illustration de ${enc(f.fr)}" src="${enc(f.image)}" data-media-fallback="${enc(wikiRedirect(f.file))}">`;
    // If the fruit has never been illustrated, a large CHARACTER portrait is useful.
    // Never confuse this substitution with a depiction of the actual physical fruit.
    if(!modal && f.portrait && f.id!=='smile')return `<img class="artwork artwork-user-substitute" loading="lazy" decoding="async" referrerpolicy="no-referrer" alt="Portrait de ${enc(f.primary_user||f.u)} : apparence physique du fruit non documentée" src="${enc(f.portrait)}" data-media-fallback="${enc(wikiRedirect(f.portrait_file))}">`;
    return '';
  }
  function imageLabel(f){if(!f.image)return f.portrait?'PORTEUR · FRUIT NON REPRÉSENTÉ':'APPARENCE DU FRUIT INCONNUE';return f.visual==='fruit'?'FRUIT PHYSIQUE RÉFÉRENCÉ':f.image_kind==='pouvoir-animé'?'ANIMATION DU POUVOIR':f.visual==='pouvoir'?'ILLUSTRATION DU POUVOIR':f.visual==='artificiel'?'FRUIT ARTIFICIEL':'INTERPRÉTATION SYMBOLIQUE'}
  function card(f){
    const selected=state.compare.includes(f.id),saved=favorites.has(f.id);
    const color=colors[f.t]||'#f4c36b';
    return `<article class="fruit-card" style="--accent:${color}" tabindex="0" role="button" aria-label="Ouvrir ${enc(f.fr)}" data-id="${enc(f.id)}">
      <div class="card-visual">
        <span class="tier-badge">${enc(f.r)}</span>
        <div class="card-controls">
          <button type="button" aria-label="${saved?'Enlever des favoris':'Ajouter aux favoris'}" aria-pressed="${saved}" class="mini-action fav-btn ${saved?'saved':''}" data-id="${enc(f.id)}">${saved?'♥':'♡'}</button>
          <button type="button" aria-label="${selected?'Retirer du comparateur':'Ajouter au comparateur'}" aria-pressed="${selected}" class="mini-action cmp-btn ${selected?'selected':''}" data-id="${enc(f.id)}">${selected?'✓':'+'}</button>
        </div>
        <div class="art-fallback">${enc(f.icon||'✦')}</div>${art(f)}<div class="art-meta">${imageLabel(f)}</div>${hasYoutube(f.id)?'<div class="anime-ribbon">▶ CLIP VIDÉO</div>':''}${clips[f.id]?.auditV46?'<span class="source-review-badge" title="Références historiques en cours d’audit">À REVOIR</span>':''}
      </div>
      <div class="card-body"><div class="category">${enc(f.t)}</div><h3 class="card-title">${enc(f.fr)}</h3><div class="card-jp">${enc(f.n)}</div>
      <div class="card-user">${portrait(f)}<div class="user-name"><span>Utilisateur</span><b>${enc(f.primary_user||f.u)}</b></div></div>
      <p class="card-power">${enc(f.p)}</p><div class="card-foot"><span>${f.w?'⚡ Éveil confirmé':'◇ Éveil non confirmé'}</span><button type="button" class="view-details" data-id="${enc(f.id)}">DÉCOUVRIR ↗</button></div>
      </div></article>`;
  }
  let visibleResults=[];
  function render(resetPage=true){
    if(resetPage)state.display=24;
    visibleResults=filters();$('resultsCount').textContent=visibleResults.length;
    $('cards').innerHTML=visibleResults.slice(0,state.display).map(card).join('');
    $('emptyState').hidden=visibleResults.length!==0;
    const more=$('loadMore');more.hidden=visibleResults.length<=state.display;more.textContent=`CHARGER PLUS DE FRUITS (${Math.min(24,visibleResults.length-state.display)} RESTANTS À AFFICHER) ↓`;
  }
  function updateCards(){render(false)}
  function reset(){state.search='';state.type='all';state.tier='';state.sort='default';state.awake=false;state.favoritesOnly=false;state.illustrated=false;state.videosOnly=false;state.reviewOnly=false;
    $('search').value='';$('tier').value='';$('sort').value='default';$('onlyAwakened').checked=false;$('onlyFavorite').checked=false;$('onlyIllustrated').checked=false;$('onlyVideos').checked=false;$('onlyReview').checked=false;
    document.querySelectorAll('[data-type]').forEach(b=>b.classList.toggle('active',b.dataset.type==='all'));
    $('favoritesTop').classList.remove('is-active');render();
  }
  function setFavoriteOnly(next){state.favoritesOnly=next;$('onlyFavorite').checked=next;$('favoritesTop').classList.toggle('is-active',next);render();document.querySelector('#catalogue').scrollIntoView({behavior:'smooth',block:'start'});}
  const escapeForUrl=(s)=>encodeURIComponent(s);
  function setUrlId(id){try{const u=new URL(window.location.href);if(id){if(u.searchParams.get('fruit')!==id)u.searchParams.delete('clip');u.searchParams.set('fruit',id)}else{u.searchParams.delete('fruit');u.searchParams.delete('clip')}history.replaceState({},'',u.toString());}catch(_){}}
  function refreshDetailActions(){const f=byId.get(state.active);if(!f)return;const fav=$('detailFavorite'),cmp=$('detailCompare');if(fav){fav.textContent=favorites.has(f.id)?'♥ EN FAVORI':'♡ AJOUTER AUX FAVORIS';fav.classList.toggle('active',favorites.has(f.id))}if(cmp){cmp.textContent=state.compare.includes(f.id)?'✓ SÉLECTIONNÉ POUR LE DUEL':'+ AJOUTER AU DUEL';}}
  function makeDetail(f){
    const color=colors[f.t]||'#f4c36b';
    const clip=clips[f.id]||{};
    const safeFile=f.file?encodeURIComponent(f.file.replaceAll(' ','_')):'';
    const safePortraitFile=f.portrait_file?encodeURIComponent(f.portrait_file.replaceAll(' ','_')):'';
    const activeIndex=visibleResults.findIndex(x=>x.id===f.id);
    const videos=clipVideos(clip);
    const yt=videos[0]?.youtubeId;
    const makeVideoButton=(video,index)=>`<button type="button" class="official-choice ${index===0?'active':''}" data-video-index="${index}" title="${enc(video.title)}" aria-pressed="${index===0}"><img loading="lazy" src="https://i.ytimg.com/vi/${enc(video.youtubeId)}/mqdefault.jpg" alt=""><span>${enc(video.title)}</span><small>${enc(video.channel||'Diffuseur')} · ${enc(video.episode||'')}</small></button>`;
    const needsReview=Boolean(clip.auditV46 && videos.length);
    const ytThumb=yt?`https://i.ytimg.com/vi/${enc(yt)}/hqdefault.jpg`:'';
    const initial=videos[0];
    const videoBody=videos.length ? `<div class="official-player" id="officialPlayer">
      <button type="button" class="official-play" id="officialPlay" aria-label="Lire l'extrait : ${enc(initial.title)}" style="--poster:url('${ytThumb}')">
        <span class="official-play-icon" aria-hidden="true">▶</span><span class="official-play-title">${enc(initial.title)}</span><span class="official-play-by">${enc(initial.channel)} · ${enc(initial.episode||'')}</span>
      </button></div>
      <div class="clip-actions"><a id="clipYoutubeSource" href="${enc(initial.source)}" rel="noopener noreferrer" target="_blank">↗ Ouvrir sur YouTube</a> <a id="clipCheckSource" href="clip-check.html?fruit=${encodeURIComponent(f.id)}&amp;video=${encodeURIComponent(initial.youtubeId)}" target="_blank" rel="noopener noreferrer">✓ Tester / signaler cet extrait</a></div>
      <p id="clipKind" class="clip-kind">${videoProvenance(initial)}</p>
      ${videos.length>1?`<div class="clips-playlist"><div class="playlist-label">AUTRES EXTRAITS · ${videos.length} VIDÉOS</div><div class="clip-thumbnails">${videos.map(makeVideoButton).join('')}</div></div>`:''}`:
      `<div class="clip-empty"><span>◈</span><strong>Aucun extrait court sélectionné pour ce fruit</strong><p>Utilise la recherche YouTube ou Google Vidéos ci-dessous. Les liens vers les épisodes complets ne sont pas proposés.</p></div>`;
    const searchTerms='One Piece '+(f.primary_user||f.u)+' '+f.n+' '+f.fr+' powers anime clip';
    const youtubeSearch='https://www.youtube.com/results?search_query='+encodeURIComponent(searchTerms);
    const googleVideoSearch='https://www.google.com/search?tbm=vid&q='+encodeURIComponent(searchTerms);
    const openSearch=`<div class="open-video-discovery" aria-label="Trouver d'autres scènes sur le web">
      <div class="playlist-label">⌕ CHERCHER DES EXTRAITS COURTS · SANS ABONNEMENT</div>
      <a class="episode-item source-discover source-youtube" target="_blank" rel="noopener noreferrer" href="${youtubeSearch}"><span>▶</span><span>Explorer les clips YouTube pour ce fruit<small>Chaînes officielles et vidéos de fans · résultats à vérifier</small></span><b>YOUTUBE ↗</b></a>
      <a class="episode-item source-discover" target="_blank" rel="noopener noreferrer" href="${googleVideoSearch}"><span>⌕</span><span>Rechercher sur d'autres plateformes<small>Google Vidéos · recherche multi-sites, disponibilité variable</small></span><b>WEB ↗</b></a>
    </div>`;
    const auditNotice=needsReview?`<p class="clip-audit-warning">⚑ RÉFÉRENCE HISTORIQUE À RECONTRÔLER — ${enc(clip.auditV46.note||'Disponibilité et adéquation au pouvoir non encore vérifiées.')}</p>`:'';
    const socialBody=clip.social?.length?`<div class="social-sources">${clip.social.map(x=>`<a href="${enc(x.url)}" rel="noopener noreferrer" target="_blank">↗ ${enc(x.title)} · ${enc(x.platform)}</a>`).join('')}</div>`:'';
    return `<div style="--accent:${color}">
      <header class="detail-top"><div><div class="detail-overline">DEMONFRUITZDEX / ${enc(f.t).toUpperCase()} / TIER ${enc(f.r)}</div><h2 class="detail-title">${enc(f.fr)}</h2><div class="detail-jp">${enc(f.n)}</div></div><div class="detail-header-actions"><button type="button" class="action-icon" id="detailShare" title="Copier le lien" aria-label="Copier le lien">↗</button><button type="button" class="round-close" id="detailClose" aria-label="Fermer">×</button></div></header>
      <div class="detail-grid detail-grid-cinema">
        <div class="character-column">
          <div class="detail-character-hero">
            ${portrait(f,true)}
            <div class="character-overlay"><span>PORTEUR DU POUVOIR</span><strong>${enc(f.primary_user||f.u)}</strong><small>${enc(f.t)} · TIER ${enc(f.r)}</small></div>
          </div>
          <div class="detail-fruit-strip"><div class="detail-fruit-mini"><div class="art-fallback">${enc(f.icon||'✦')}</div>${art(f,true)}</div><div><span>LE FRUIT</span><strong>${enc(f.fr)}</strong><small>${imageLabel(f)}</small></div></div>
          <div class="detail-info-row"><div><span>Famille</span><strong>${enc(f.t)}</strong></div><div><span>Rang éditorial</span><strong style="color:var(--gold)">TIER ${enc(f.r)}</strong></div><div><span>Éveil</span><strong>${f.w?'⚡ Confirmé':'Non confirmé'}</strong></div><div><span>Fruit physique</span><strong>${String(f.a||'').startsWith('Connu')?'Apparence rapportée':'Non identifié'}</strong></div></div>
        </div>
        <div class="scene-column">
          <div class="detail-power-label">✦ / EXPRESSION DU POUVOIR</div><p class="detail-power">${enc(f.p)}</p>
          <div class="anime-section-head"><strong>▶ LE POUVOIR EN ACTION</strong><span>${videos.length?`${videos.length} CLIP${videos.length>1?'S':''}`:'EXTRAIT À TROUVER'}</span></div>
          ${videoBody}
          ${openSearch}${auditNotice}${videos.length&&clip.note?`<p class="clip-note">${enc(clip.note)}</p>`:''}${socialBody}
          <div class="clip-note">YouTube est accessible indépendamment de Crunchyroll, mais certaines vidéos peuvent être limitées selon le pays. Les épisodes Crunchyroll restent des références facultatives ; le lecteur dépend des droits du diffuseur.</div>
          <div class="detail-source">${f.file?`<a target="_blank" rel="noopener noreferrer" href="https://onepiece.fandom.com/wiki/File:${safeFile}">↗ Source du visuel du fruit / pouvoir</a>`:`Apparence officielle du fruit non documentée ici · <a target="_blank" rel="noopener noreferrer" href="https://onepiece.fandom.com/wiki/Special:Search?query=${encodeURIComponent(f.n)}">⌕ Explorer les illustrations du pouvoir</a>`}<br>
          ${f.portrait_file?`<a target="_blank" rel="noopener noreferrer" href="https://onepiece.fandom.com/wiki/File:${safePortraitFile}">↗ Source du portrait utilisateur${f.portrait_kind==='portrait-jeu'?' (illustration de jeu)':''}</a>`:'Portrait utilisateur de secours · <a target="_blank" rel="noopener noreferrer" href="https://onepiece.fandom.com/wiki/Special:Search?query=${encodeURIComponent(f.primary_user||f.u)}">⌕ Rechercher ce personnage</a>'}</div>
          <div class="detail-action-row"><button type="button" id="detailFavorite">${favorites.has(f.id)?'♥ EN FAVORI':'♡ AJOUTER AUX FAVORIS'}</button><button type="button" id="detailCompare">${state.compare.includes(f.id)?'✓ SÉLECTIONNÉ POUR LE DUEL':'+ AJOUTER AU DUEL'}</button></div>
        </div>
      </div>
      <div class="detail-nav"><button id="detailPrevious" ${activeIndex<=0?'disabled':''}>← FRUIT PRÉCÉDENT</button><button id="detailNext" ${activeIndex<0||activeIndex>=visibleResults.length-1?'disabled':''}>FRUIT SUIVANT →</button></div>
      </div>`;
  }
  function openDetail(id,updateUrl=true){const f=byId.get(id);if(!f)return;stopMotion();state.active=id;
    $('detailContent').innerHTML=makeDetail(f);if(!$('detailDialog').open)$('detailDialog').showModal();
    if(updateUrl)setUrlId(id);
    $('detailClose').onclick=()=>closeDetail();
    $('detailFavorite').onclick=()=>toggleFavorite(id);
    $('detailCompare').onclick=()=>selectCompare(id);
    $('detailShare').onclick=async()=>{const u=new URL(location.href);u.searchParams.set('fruit',id);try{await navigator.clipboard.writeText(u.toString());toast('Lien de la fiche copié');}catch(_){toast('Copie non disponible dans ce navigateur');}};
    const ix=visibleResults.findIndex(x=>x.id===id);
    $('detailPrevious').onclick=()=>{if(ix>0)openDetail(visibleResults[ix-1].id)};
    $('detailNext').onclick=()=>{if(ix!==-1&&ix<visibleResults.length-1)openDetail(visibleResults[ix+1].id)};
    wireOfficialClip(f);
  }
  function closeDetail(){stopMotion();const d=$('detailDialog');if(d.open)d.close();state.active=null;setUrlId(null)}
  function stopMotion(){
    // Closing or navigating a detail must stop any playing third-party video.
    const frame=$('officialClipFrame');if(frame){frame.src='about:blank';frame.remove();}
  }
  function wireOfficialClip(f){
    const meta=clips[f.id],choices=clipVideos(meta);if(!choices.length)return;
    let currentIndex=0;
    try { const requested=new URL(location.href).searchParams.get('clip'); const ix=choices.findIndex(x=>x.youtubeId===requested); if(ix>=0)currentIndex=ix; } catch(_){}
    function selectVideo(index){
      const selected=choices[index];if(!selected)return;
      currentIndex=index;
      try {const url=new URL(location.href);if(url.searchParams.get('fruit')===f.id){url.searchParams.set('clip',selected.youtubeId);history.replaceState({},'',url.toString());}}catch(_){}
      stopMotion();
      const box=$('officialPlayer');if(!box)return;
      const button=document.createElement('button');button.type='button';button.className='official-play';button.id='officialPlay';
      button.style.setProperty('--poster',`url('https://i.ytimg.com/vi/${selected.youtubeId}/hqdefault.jpg')`);
      button.setAttribute('aria-label',`Lire l’extrait : ${selected.title}`);
      button.innerHTML=`<span class="official-play-icon" aria-hidden="true">▶</span><span class="official-play-title">${enc(selected.title)}</span><span class="official-play-by">${enc(selected.channel)} · ${enc(selected.episode||'')}</span>`;
      box.replaceChildren(button);
      const source=$('clipYoutubeSource');if(source)source.href=selected.source;
      const clipAudit=$('clipCheckSource');if(clipAudit)clipAudit.href='clip-check.html?fruit='+encodeURIComponent(f.id)+'&video='+encodeURIComponent(selected.youtubeId);
      const kind=$('clipKind');if(kind)kind.textContent=videoProvenance(selected);
      document.querySelectorAll('[data-video-index]').forEach(x=>{
        const active=Number(x.dataset.videoIndex)===index;
        x.classList.toggle('active',active);x.setAttribute('aria-pressed',String(active));
      });
      button.addEventListener('click',()=>{
        const videoId=selected.youtubeId;
        if(!/^[A-Za-z0-9_-]{11}$/.test(videoId))return;
        const frame=document.createElement('iframe');frame.id='officialClipFrame';
        frame.title=`Extrait ${selected.title}`;frame.loading='eager';
        frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';
        frame.src=`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&playsinline=1`;
        button.replaceWith(frame);
        toast('Lecture depuis '+selected.channel);
      },{once:true});
    }
    document.querySelectorAll('[data-video-index]').forEach(button=>button.addEventListener('click',()=>selectVideo(Number(button.dataset.videoIndex))));
    selectVideo(currentIndex);
  }
  function renderCompare(){const choices=state.compare.map(id=>byId.get(id)).filter(Boolean);$('compareContent').innerHTML=choices.map(f=>`<div class="compare-col" style="--accent:${colors[f.t]||'#f4c36b'}"><div class="category" style="color:var(--accent)">${enc(f.t)}</div><h3>${enc(f.fr)}</h3><div class="compare-jp">${enc(f.n)}</div><div class="compare-fruit">${f.image?`<img src="${enc(f.image)}" referrerpolicy="no-referrer" alt="Illustration ${enc(f.fr)}">`:enc(f.icon||'✦')}</div><div class="card-user">${portrait(f)}<div class="user-name"><span>Utilisateur</span><b>${enc(f.primary_user||f.u)}</b></div></div><div class="compare-stat"><span>Tier</span><strong style="color:var(--gold)">${enc(f.r)}</strong></div><div class="compare-stat"><span>Éveil</span><strong>${f.w?'Confirmé ⚡':'Non confirmé'}</strong></div><div class="compare-stat"><span>Forme physique</span><strong>${String(f.a||'').startsWith('Connu')?'Connue':'Non documentée'}</strong></div><p class="detail-power">${enc(f.p)}</p><button class="btn btn-quiet compare-explore" data-id="${enc(f.id)}">VOIR LA FICHE ↗</button></div>`).join('')}
  function renderRanking(){const names=['Hito Hito no Mi, modèle Nika','Yami Yami no Mi','Gura Gura no Mi','Ope Ope no Mi','Akuma no Mi','Ryu Ryu no Mi, modèle Nidhöggr','Ryu Ryu no Mi, modèle Kirin','Nikyu Nikyu no Mi','Soru Soru no Mi','Hobi Hobi no Mi','Goro Goro no Mi','Zushi Zushi no Mi','Wapu Wapu no Mi','Shima Shima no Mi','Magu Magu no Mi','Pika Pika no Mi','Toshi Toshi no Mi','Shiku Shiku no Mi','Nomi Nomi no Mi','Toki Toki no Mi'];const byName=new Map(fruits.map(f=>[f.n,f]));$('ranking').innerHTML=names.map((n,i)=>{const f=byName.get(n);return f?`<button class="rank" data-id="${enc(f.id)}"><span class="rank-index">${String(i+1).padStart(2,'0')}</span><span class="rank-name">${enc(f.fr)}<small>${enc(f.n)}</small></span><span class="rank-tier">${enc(f.r)}</span></button>`:''}).join('')}
  function attachEvents(){
    $('search').addEventListener('input',e=>{state.search=e.target.value;render()});
    $('typeFilters').addEventListener('click',e=>{const b=e.target.closest('[data-type]');if(!b)return;state.type=b.dataset.type;document.querySelectorAll('[data-type]').forEach(x=>x.classList.toggle('active',x===b));render()});
    $('tier').addEventListener('change',e=>{state.tier=e.target.value;render()});$('sort').addEventListener('change',e=>{state.sort=e.target.value;render()});
    $('onlyAwakened').addEventListener('change',e=>{state.awake=e.target.checked;render()});$('onlyIllustrated').addEventListener('change',e=>{state.illustrated=e.target.checked;render()});
    $('onlyVideos').addEventListener('change',e=>{state.videosOnly=e.target.checked;render()});
    $('onlyReview').addEventListener('change',e=>{state.reviewOnly=e.target.checked;render()});
    $('onlyFavorite').addEventListener('change',e=>{state.favoritesOnly=e.target.checked;$('favoritesTop').classList.toggle('is-active',state.favoritesOnly);render()});
    $('favoritesTop').addEventListener('click',()=>setFavoriteOnly(!state.favoritesOnly));
    $('reset').addEventListener('click',reset);$('emptyReset').addEventListener('click',reset);
    $('loadMore').addEventListener('click',()=>{state.display+=24;render(false)});
    $('randomButton').addEventListener('click',()=>{const list=filters();if(!list.length){toast('Aucun fruit disponible avec les filtres actuels');return}openDetail(list[Math.floor(Math.random()*list.length)].id)});
    $('cards').addEventListener('click',e=>{const b=e.target.closest('[data-id]');if(!b)return;const id=b.dataset.id;if(b.classList.contains('fav-btn'))toggleFavorite(id);else if(b.classList.contains('cmp-btn'))selectCompare(id);else openDetail(id)});
    $('cards').addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.classList.contains('fruit-card')){e.preventDefault();openDetail(e.target.dataset.id)}});
    $('ranking').addEventListener('click',e=>{const b=e.target.closest('[data-id]');if(b)openDetail(b.dataset.id)});
    $('compareOpen').addEventListener('click',()=>{if(state.compare.length!==2)return;renderCompare();$('compareDialog').showModal()});
    $('compareClear').addEventListener('click',()=>{state.compare=[];updateDock();updateCards()});
    $('compareClose').addEventListener('click',()=>$('compareDialog').close());
    $('compareContent').addEventListener('click',e=>{const b=e.target.closest('.compare-explore');if(b){$('compareDialog').close();openDetail(b.dataset.id)}});
    ['detailDialog','compareDialog'].forEach(id=>$(id).addEventListener('click',e=>{if(e.target===$(id))$(id).close()}));
    $('detailDialog').addEventListener('close',()=>{stopMotion();state.active=null;setUrlId(null)});
    document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement?.tagName!=='INPUT'){e.preventDefault();$('search').focus()}if(e.key==='Escape')stopMotion()});
    // YouTube controls its own playback; frames are removed when changing/closing fiches.
    // Broken third-party links never result in blank portrait/card. Error capture handles nested markup.
    document.addEventListener('error',e=>{const img=e.target;if(img.tagName!=='IMG')return;if(img.classList.contains('artwork')||img.closest('.portrait-frame')||img.closest('.compare-fruit'))img.style.display='none'},true);
  }
  // Stats count exactly what is represented in this data source, including artificial/unknown.
  $('clipInventory').textContent=fruits.filter(f=>hasScene(f.id)).length;
  $('statTotal').textContent=fruits.length;$('statLogia').textContent=fruits.filter(f=>f.t==='Logia').length;
  $('statZoan').textContent=fruits.filter(f=>String(f.t).startsWith('Zoan')).length;
  $('statParamecia').textContent=fruits.filter(f=>f.t==='Paramecia').length;
  persist();attachEvents();renderRanking();render();
  try {const id=new URL(location.href).searchParams.get('fruit');if(id&&byId.has(id))openDetail(id,false)}catch(_){}
})();
