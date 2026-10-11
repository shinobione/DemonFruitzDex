#!/usr/bin/env python3
"""Real external image loads in headless Chrome on a GitHub-hosted runner.

DO NOT equate a failed image on GitHub's network with a globally dead image.
Browser observations are grouped by outcome; network restrictions stay UNKNOWN.
No media copies, image scraping or repo data mutations.
"""
import argparse, asyncio, collections, json, pathlib, re
from datetime import datetime, timezone
from playwright.async_api import async_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'reports/media-inventory-v49d.json'
REPORT=ROOT/'reports/media-browser-audit-v49d.json'
TIMEOUT_MS=6500
CONCURRENCY=20

async def run(limit=None):
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    entries=[(row,kind,row[kind]) for row in manifest['records'] for kind in ('portrait','visual') if row[kind]['registered']]
    if limit:
        entries=entries[:limit]
    async with async_playwright() as p:
        browser=await p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox'])
        context=await browser.new_context(viewport={'width':1440,'height':900},service_workers='block')
        page=await context.new_page()
        # Use the same browser Image loading path as the site's media checker, with no-referrer.
        await page.goto('about:blank')
        payload=[{'id':row['id'],'name':row['name'],'holder':row['holder'],'kind':kind,
                  'url':res['url'],'fallback':res['fallback']} for row,kind,res in entries]
        results=await page.evaluate("""async ({items,timeout,concurrency})=>{
          let next=0;const results=new Array(items.length);
          const check=(url)=>new Promise(resolve=>{
            if(!url){resolve({status:'not-configured',width:0,height:0});return}
            const img=new Image();img.referrerPolicy='no-referrer';let settled=false;
            const timer=setTimeout(()=>finish('timeout'),timeout);
            function finish(status){if(settled)return;settled=true;clearTimeout(timer);
              img.onload=img.onerror=null;
              resolve({status,width:img.naturalWidth||0,height:img.naturalHeight||0});}
            img.onload=()=>finish(img.naturalWidth===300&&img.naturalHeight===171?'placeholder':img.naturalWidth>0&&img.naturalHeight>0?'loaded':'empty');
            img.onerror=()=>finish('error');
            img.src=url;
          });
          async function worker(){
            while(next<items.length){
              const i=next++,item=items[i];
              const direct=await check(item.url);
              const fallback=direct.status==='loaded'?{status:'not-needed',width:0,height:0}:
                item.fallback&&item.fallback!==item.url?await check(item.fallback):{status:'not-available',width:0,height:0};
              results[i]={...item,direct,fallback,
                classification:direct.status==='loaded'?'direct-loaded':
                  fallback.status==='loaded'?'fallback-loaded':
                  (direct.status==='placeholder'||fallback.status==='placeholder'?'wiki-placeholder':direct.status==='timeout'||fallback.status==='timeout'?'timeout-unconfirmed':'browser-load-failed')};
            }
          }
          await Promise.all(Array.from({length:Math.min(concurrency,items.length)},worker));
          return results;
        }""", {'items':payload,'timeout':TIMEOUT_MS,'concurrency':CONCURRENCY})
        await browser.close()

    counters=collections.Counter(x['classification'] for x in results)
    kinds={k:dict(collections.Counter(x['classification'] for x in results if x['kind']==k)) for k in ('portrait','visual')}
    report={'schema':'demonfruitzdex.media-browser-audit.v49d',
      'date':datetime.now(timezone.utc).isoformat(),
      'environment':'GitHub Actions Linux Chrome; NOT a France browser; remote host may block CI/hotlink',
      'timeoutMs':TIMEOUT_MS,'concurrency':CONCURRENCY,
      'scope':{'fruits':166,'mediaReferencesTested':len(results),'expectedFullMediaReferences':manifest['stats']['directReferences'],
               'subset':bool(limit)},
      'outcomes':dict(counters),'byKind':kinds,
      'disclaimer':'We visually confirmed the wiki responds with a generic blank placeholder at 300x171 for missing files; such responses are classified separately. A decoded image is not automatically the correct depicted character nor licensed. Browser failures can reflect hotlink/rate/geo filtering.',
      'results':results}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('MEDIA_BROWSER_AUDIT_STATS='+json.dumps({'outcomes':dict(counters),'byKind':kinds,'tested':len(results)},ensure_ascii=False),flush=True)
    for x in results:
        if x['classification']!='direct-loaded':
            print('MEDIA_BROWSER_ISSUE='+json.dumps({'id':x['id'],'kind':x['kind'],'class':x['classification'],
               'direct':x['direct']['status'],'fallback':x['fallback']['status'],'url':x['url']},ensure_ascii=False),flush=True)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=None,help='first N media resources, for a fast probe; omit for all 302')
    args=parser.parse_args()
    asyncio.run(run(args.limit))
