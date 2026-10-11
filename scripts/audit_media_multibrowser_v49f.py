#!/usr/bin/env python3
"""Cross-engine reality check: 316 remote media references in Chromium, Firefox and WebKit.
An engine's success/failure is network-local evidence, not a global URL verdict.
"""
import argparse, asyncio, collections, functools, http.server, json, pathlib, threading
from datetime import datetime, timezone
from playwright.async_api import async_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'reports/media-inventory-v49f.json'
TIMEOUT=6000
CONCURRENCY=18

async def run(engine):
    inv=json.loads(MANIFEST.read_text(encoding='utf-8'))
    entries=[{'id':r['id'],'name':r['name'],'kind':kind,
              'url':r[kind]['url'],'filename':r[kind]['filename']}
             for r in inv['records'] for kind in ('portrait','art') if r[kind]['referenced']]
    assert len(entries)==316
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        async with async_playwright() as playwright:
            browser_type=getattr(playwright,engine)
            browser=await browser_type.launch(headless=True,args=['--no-sandbox'] if engine=='chromium' else [])
            context=await browser.new_context(viewport={'width':1440,'height':900},service_workers='block')
            page=await context.new_page()
            response=await page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='domcontentloaded',timeout=30000)
            assert response and response.status==200
            await page.wait_for_function('window.SHINO_DATA?.length===166 && window.SHINO_MEDIA_RELIABILITY')
            measurements=await page.evaluate("""async ({items,concurrency,timeout})=>{
                let ix=0,found=new Array(items.length);
                const core=window.SHINO_MEDIA_RELIABILITY;
                async function worker(){
                    while(ix<items.length){
                        const idx=ix++,x=items[idx];
                        const test=await core.probe(x,{timeout});
                        found[idx]={id:x.id,kind:x.kind,url:x.url,
                            status:test.status,attempts:test.attempts};
                    }
                }
                await Promise.all(Array.from({length:Math.min(concurrency,items.length)},worker));
                return {records:found,catalogue:{
                    fruits:window.SHINO_DATA.length,
                    portraits:window.SHINO_DATA.filter(x=>!!x.portrait).length,
                    art:window.SHINO_DATA.filter(x=>!!x.image).length
                }};
            }""",{'items':entries,'concurrency':CONCURRENCY,'timeout':TIMEOUT})
            assert len(measurements['records'])==316
            assert measurements['catalogue']=={'fruits':166,'portraits':164,'art':152},measurements['catalogue']
            stats=dict(collections.Counter(x['status'] for x in measurements['records']))
            by_kind={k:dict(collections.Counter(x['status'] for x in measurements['records'] if x['kind']==k)) for k in ('portrait','art')}
            report={'schema':'demonfruitzdex.media-browser-audit.v49f',
               'testedAt':datetime.now(timezone.utc).isoformat(),
               'engine':engine,'engineVersion':browser.version,'environment':'GitHub runner or local machine; location not inferred',
               'timeoutMs':TIMEOUT,'concurrency':CONCURRENCY,
               'catalogue':measurements['catalogue'],'referencesTested':316,
               'outcomes':stats,'byKind':by_kind,
               'disclaimer':'Failure can be hotlink/geo/CDN/CSP/browser policy; image load cannot establish correct copyrighted content. CORS is not normally needed for HTML img display. This is not a network diagnosis of the user’s Windows browser.',
               'records':measurements['records']}
            target=ROOT/'reports'/f'media-browser-v49f-{engine}.json'
            target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print('MEDIA_V49F_ENGINE='+json.dumps({'engine':engine,'version':browser.version,'outcomes':stats,'byKind':by_kind},ensure_ascii=False),flush=True)
            await browser.close()
    finally:
        server.shutdown()
    return report

if __name__=='__main__':
    arg=argparse.ArgumentParser()
    arg.add_argument('--engine',choices=['chromium','firefox','webkit'],required=True)
    args=arg.parse_args()
    asyncio.run(run(args.engine))
