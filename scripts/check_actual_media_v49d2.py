#!/usr/bin/env python3
"""Real page integration QA: evaluate media sidecars in published script order in Chrome.

Do not infer permission to distribute third-party art from browser loading.
"""
import asyncio, functools, http.server, json, pathlib, threading
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
TARGET=[
'tori-tori-no-mi-mod-le-phoenix','mogu-mogu-no-mi','fude-fude-no-mi',
'toki-toki-no-mi','aro-aro-no-mi','akuma-no-mi','fruit-artificiel-seiryu'
]
OUT=ROOT/'reports'/'media-actual-page-v49d2.jpg'
async def main():
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/index.html'
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox'])
            page=await browser.new_page(viewport={'width':1450,'height':920})
            failed=[]
            page.on('pageerror',lambda exc:failed.append(str(exc)))
            response=await page.goto(url,wait_until='domcontentloaded',timeout=30000)
            assert response and response.status==200
            await page.wait_for_function('Array.isArray(window.SHINO_DATA) && window.SHINO_DATA.length===166')
            facts=await page.evaluate("""(ids)=>{
                const fruits=window.SHINO_DATA;
                return {
                  count:fruits.length,
                  portraits:fruits.filter(f=>!!f.portrait).length,
                  art:fruits.filter(f=>!!f.image).length,
                  seven:ids.map(id=>({id,fruit:fruits.find(f=>f.id===id)})).map(row=>({
                    id:row.id,user:row.fruit?.primary_user||row.fruit?.u,
                    filename:row.fruit?.portrait_file,kind:row.fruit?.portrait_kind,
                    source:row.fruit?.portrait_source,portrait:row.fruit?.portrait
                  }))
                }
            }""",TARGET)
            assert facts['count']==166 and facts['portraits']==164 and facts['art']==140,facts
            assert len(facts['seven'])==7
            for record in facts['seven']:
                assert record['portrait'].startswith('https://static.wikia.nocookie.net/onepiece/images/')
                assert record['filename'].lower() not in ('marco portrait.png','kanjuro portrait.png','imu portrait.png')
                assert record['source']=='One Piece Wiki'
            assert not failed,'JS runtime errors: '+repr(failed[:5])
            # Capture as actually resolved by the browser, not from a manually fabricated list.
            html='<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#0d141e;color:#fff;font-family:system-ui;padding:18px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.cell{border:1px solid #94755d;background:#222c35;border-radius:8px;padding:10px}.cell img{height:210px;max-width:100%;width:100%;object-fit:contain;background:#13171c}.cell p{font-size:13px;line-height:1.4;overflow-wrap:anywhere}</style><h2>DemonFruitzDex V4.9.d2: 7 resolved portraits</h2><div class="grid">'
            for item in facts['seven']:
                html+=f'<div class="cell"><p>{item["id"]} · {item["user"]} · {item["kind"]}</p><img referrerpolicy="no-referrer" src="{item["portrait"]}"><p>{item["filename"]}</p></div>'
            html+='</div>'
            await page.set_content(html)
            await page.wait_for_function("Array.from(document.images).every(x=>x.complete)")
            sizes=await page.evaluate("Array.from(document.images).map(x=>[x.naturalWidth,x.naturalHeight])")
            assert len(sizes)==7 and all(w>0 and h>0 and (w,h)!=(300,171) for w,h in sizes),sizes
            await page.screenshot(path=str(OUT),full_page=True,type='jpeg',quality=83)
            print('PASS ACTUAL_SITE_V49D2='+json.dumps({'fruitCount':facts['count'],
                'portraits':facts['portraits'],'visuals':facts['art'],
                'newImages':[{**{'id':f['id'],'file':f['filename']},'size':sizes[i]} for i,f in enumerate(facts['seven'])],
                'screenshot':str(OUT.relative_to(ROOT))},ensure_ascii=False),flush=True)
            await browser.close()
    finally:
        server.shutdown()
asyncio.run(main())
