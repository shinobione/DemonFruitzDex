/* V4.9.f — runtime/browser diagnostic helpers; images remain at their credited external URLs.
 * A successful browser image decode is NOT evidence of correctness, legality or world-wide access. */
(function(){
'use strict';
const WIKI_FILE=/\.(?:png|jpe?g|webp|gif)$/i;
const WIKI_HOST=/^https:\/\/(?:static\.wikia\.nocookie\.net\/onepiece\/|onepiece\.fandom\.com\/wiki\/Special:Redirect\/file\/)/i;
const ERROR_SIZE={width:300,height:171}; // Visually confirmed blank One Piece Wiki file substitute.
function redirect(filename){
  return typeof filename==='string'&&WIKI_FILE.test(filename)
  ? 'https://onepiece.fandom.com/wiki/Special:Redirect/file/'+encodeURIComponent(filename.replaceAll(' ','_')) : '';
}
function fakeWikiImage(url,width,height){
  return WIKI_HOST.test(url||'')&&width===ERROR_SIZE.width&&height===ERROR_SIZE.height;
}
function makeCandidates(url,filename){
  const direct=typeof url==='string'?url.trim():'';
  const alt=redirect(filename);
  if(!direct)return [];
  return [direct,...(alt&&alt!==direct?[alt]:[])];
}
function loadImage(url,timeout=6500){
  return new Promise(resolve=>{
    let img=new Image(),finished=false;
    img.referrerPolicy='no-referrer';
    function settle(status){
      if(finished)return;
      finished=true;clearTimeout(timer);
      img.onload=null;img.onerror=null;
      resolve({status,width:img.naturalWidth||0,height:img.naturalHeight||0});
    }
    const timer=setTimeout(()=>settle('timeout'),timeout);
    img.onload=()=>settle(fakeWikiImage(url,img.naturalWidth,img.naturalHeight)?'wiki-placeholder':img.naturalWidth>0&&img.naturalHeight>0?'loaded':'empty');
    img.onerror=()=>settle('error');
    img.src=url;
  });
}
async function probe(resource,{timeout=6500}={}){
  const candidates=makeCandidates(resource.url,resource.filename);
  if(!candidates.length)return {status:'not-referenced',attempts:[],selected:null};
  const attempts=[];
  for(const [i,url] of candidates.entries()){
    const result=await loadImage(url,timeout);
    attempts.push({kind:i?'named-file-redirect':'direct',url,...result});
    if(result.status==='loaded')return {status:i?'fallback-loaded':'direct-loaded',attempts,selected:url};
  }
  return {status:attempts.some(a=>a.status==='timeout')?'timeout-unconfirmed':
    attempts.some(a=>a.status==='wiki-placeholder')?'wiki-placeholder':'browser-load-failed',attempts,selected:null};
}
window.SHINO_MEDIA_RELIABILITY=Object.freeze({redirect,fakeWikiImage,makeCandidates,probe,ERROR_SIZE});
})();