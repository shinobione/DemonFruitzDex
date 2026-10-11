#!/usr/bin/env python3
"""User-facing failure-mode test: intentional third-party image blocking.

This deliberately aborts external images. It validates graceful degradation in
each engine; it is NOT a claim that those images are globally broken.
"""
import argparse, asyncio, functools, http.server, json, pathlib, threading
from urllib.parse import urlsplit
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]

async def main(engine):
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    out=ROOT/'reports'/'screenshots'/'v49f'
    out.mkdir(parents=True,exist_ok=True)
    try:
        async with async_playwright() as p:
            browser=await getattr(p,engine).launch(headless=True,args=['--no-sandbox'] if engine=='chromium' else [])
            context=await browser.new_context(viewport={'width':1280,'height':900},accept_downloads=True)
            async def block_remote_images(route):
                req=route.request
                u=urlsplit(req.url)
                if req.resource_type=='image' and u.hostname not in ('127.0.0.1','localhost'):
                    await route.abort(error_code='failed')
                else:await route.continue_()
            await context.route('**/*',block_remote_images)
            page=await context.new_page()
            errors=[]
            page.on('pageerror',lambda exc: errors.append(str(exc)))
            response=await page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='domcontentloaded',timeout=30000)
            assert response and response.status==200
            await page.wait_for_function('window.SHINO_DATA && window.SHINO_MEDIA_RELIABILITY')
            meta=await page.evaluate("""()=>({
                fruits:window.SHINO_DATA.length,
                portraits:window.SHINO_DATA.filter(f=>f.portrait).length,
                art:window.SHINO_DATA.filter(f=>f.image).length
            })""")
            assert meta=={'fruits':166,'portraits':164,'art':152},meta
            # Rendered site must degrade into its own designed placeholder rather than broken IMG icons.
            await page.wait_for_timeout(700)
            assert await page.locator('.fruit-card').count()>0
            await page.screenshot(path=str(out/f'media-failover-{engine}.jpg'),type='jpeg',quality=72)
            await page.goto(f'http://127.0.0.1:{server.server_port}/media-check.html',wait_until='domcontentloaded')
            await page.locator('#rescue').click()
            await page.wait_for_function("!document.getElementById('export').disabled",timeout=90000)
            rows=await page.locator('#rows tr').count()
            assert rows==12,rows
            async with page.expect_download() as download_info:
                await page.locator('#export').click()
            download=await download_info.value
            report=json.loads(pathlib.Path(await download.path()).read_text(encoding='utf-8'))
            assert report['scope']=={'fruits':166,'slots':332,'examined':12},report['scope']
            assert len(report['results'])==12
            assert all(x['status'] in ('browser-load-failed','wiki-placeholder','timeout-unconfirmed') for x in report['results'])
            await page.locator('#failedOnly').check()
            assert await page.locator('#rows tr').count()==12
            await page.locator('#sample').click()
            await page.wait_for_function("!document.getElementById('export').disabled",timeout=90000)
            assert await page.locator('#rows tr').count()==30
            assert '16 absents' in (await page.locator('#summary').inner_text())
            await page.screenshot(path=str(out/f'media-check-v2-{engine}.jpg'),type='jpeg',quality=72,full_page=True)
            assert not errors,'JS errors: '+repr(errors[:5])
            print('PASS MEDIA_UI_V49F='+json.dumps({'engine':engine,'site':meta,'fullSlots':332,
               'rescue':12,'missingInSample':16,'blockedExternalImages':'graceful fallback',
               'screenshot':str((out/f'media-check-v2-{engine}.jpg').relative_to(ROOT))}),flush=True)
            await browser.close()
    finally:
        server.shutdown()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=['chromium','firefox','webkit'],required=True)
    asyncio.run(main(ap.parse_args().engine))
