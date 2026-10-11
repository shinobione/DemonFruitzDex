#!/usr/bin/env python3
"""Chrome review of real Dex cards/details, MEDIA CHECK and visually reviewed content fingerprints.

Only browser screenshots are saved as requested review artifacts. Original third-party files
are never downloaded, copied to assets or redistributed. This does not grant a reuse licence.
"""
import argparse, asyncio, functools, html, http.server, io, json, os, pathlib, platform, subprocess, threading
from datetime import datetime, timezone
from PIL import Image
from playwright.async_api import async_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/screenshots/v49e'
MANIFEST=ROOT/'reports/illustration-evidence-v49e.json'
REPORT=ROOT/'reports/illustration-browser-audit-v49e.json'

class SiteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/DemonFruitzDex/'):
            self.path=self.path[len('/DemonFruitzDex'):]
        super().do_GET()
    def log_message(self,*args):
        pass

def dhash(png):
    # Fingerprint a browser screenshot, not an HTTP download of the source artwork.
    pixels=list(Image.open(io.BytesIO(png)).convert('L').resize((9,8)).getdata())
    bits=[pixels[y*9+x]>pixels[y*9+x+1] for y in range(8) for x in range(8)]
    return f'{sum(int(bit)<<(63-i) for i,bit in enumerate(bits)):016x}'

async def main(review=False):
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    selected=[x for x in manifest['decisions'] if x['decision']=='added']
    held=[x for x in manifest['decisions'] if x['decision']=='held']
    OUT.mkdir(parents=True,exist_ok=True)
    handler=functools.partial(SiteHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/DemonFruitzDex/'
    errors=[];results=[];captured=[];facts={};media_results=[];passed=False
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox'])
            context=await browser.new_context(viewport={'width':1440,'height':1000},service_workers='block')
            page=await context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            response=await page.goto(base,wait_until='domcontentloaded',timeout=30000)
            assert response.status==200
            facts=await page.evaluate('''()=>({fruits:SHINO_DATA.length,portraits:SHINO_DATA.filter(f=>f.portrait).length,
              artworks:SHINO_DATA.filter(f=>f.image).length,videos:Object.values(SHINO_CLIPS).reduce((n,c)=>n+(c.youtubeId?1:0)+(c.moreVideos||[]).length,0),
              selected:SHINO_POWER_ART_V49E.map(a=>SHINO_DATA.find(f=>f.id===a.id)),
              unillustrated:SHINO_DATA.filter(f=>!f.image).map(f=>f.id)})''')
            assert (facts['fruits'],facts['portraits'],facts['artworks'],facts['videos'])==(166,164,152,50),facts
            assert set(facts['unillustrated'])=={x['id'] for x in held}
            # Each source URL must load on the actual detail page, with the production referrer policy.
            for item in selected:
                url=base+'?fruit='+item['id']
                await page.goto(url,wait_until='domcontentloaded',timeout=30000)
                img=page.locator('#detailContent .detail-fruit-mini img.artwork')
                try:
                    await img.scroll_into_view_if_needed(timeout=10000)
                    await page.wait_for_function('''()=>{const i=document.querySelector('#detailContent .detail-fruit-mini img.artwork');return i&&i.complete&&i.naturalWidth>0}''',timeout=20000)
                    actual=await img.evaluate('i=>({url:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight,alt:i.alt,referrerPolicy:i.referrerPolicy})')
                    assert actual['url']==item['image'],actual
                    assert (actual['width'],actual['height'])==(item['browser']['width'],item['browser']['height']),actual
                    assert (actual['width'],actual['height'])!=(300,171)
                    assert actual['referrerPolicy']=='no-referrer'
                    assert actual['alt']==next(x['visual_description'] for x in facts['selected'] if x['id']==item['id'])
                    assert await page.locator('#detailContent .detail-source a').first.get_attribute('href')==item['provenance']
                    assert await page.locator('#detailContent .detail-source').get_by_text('Preuve canonique',exact=True).get_attribute('href')==item['canonicalEvidence']
                    label=await page.locator('#detailContent .detail-fruit-strip small').inner_text()
                    assert 'FRUIT PHYSIQUE' not in label
                    shot=OUT/(item['id']+'-detail.jpg')
                    await page.screenshot(path=str(shot),type='jpeg',quality=85,animations='disabled')
                    captured.append(str(shot.relative_to(ROOT)))
                    results.append({'id':item['id'],'status':'loaded-on-real-detail','kind':item['imageKind'],'label':label,'browser':actual,'screenshot':str(shot.relative_to(ROOT))})
                    print('DETAIL_OK '+item['id']+' '+str(actual['width'])+'x'+str(actual['height']),flush=True)
                except Exception as exc:
                    results.append({'id':item['id'],'status':'failed','error':str(exc)[:600]})
                    print('DETAIL_FAILED '+item['id']+' '+str(exc)[:100],flush=True)
            await page.goto(base,wait_until='domcontentloaded')
            await page.locator('#search').fill('Tama')
            card=page.locator('.fruit-card[data-id="kibi-kibi-no-mi"]')
            await card.scroll_into_view_if_needed()
            await page.wait_for_function('''()=>{const i=document.querySelector('.fruit-card[data-id="kibi-kibi-no-mi"] img.artwork');return i&&i.complete&&i.naturalWidth>0}''',timeout=20000)
            await page.screenshot(path=str(OUT/'dex-desktop.jpg'),type='jpeg',quality=85,animations='disabled')
            # A held slot remains empty in the modal; a character portrait cannot count as artwork.
            await page.goto(base+'?fruit=oshi-oshi-no-mi',wait_until='domcontentloaded')
            assert await page.locator('#detailContent .detail-fruit-mini img').count()==0
            for width in [768,390,360]:
                await page.set_viewport_size({'width':width,'height':900})
                await page.goto(base+'?fruit=kibi-kibi-no-mi',wait_until='domcontentloaded')
                await page.locator('#detailContent .detail-fruit-mini').scroll_into_view_if_needed()
                assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                assert await page.locator('#detailDialog').evaluate('e=>e.scrollWidth<=e.clientWidth+1')
                await page.screenshot(path=str(OUT/f'dex-detail-{width}.jpg'),type='jpeg',quality=85,animations='disabled')
            await page.set_viewport_size({'width':1440,'height':1000})
            await page.goto(base+'media-check.html',wait_until='domcontentloaded')
            await page.locator('#rescue').click()
            await page.wait_for_function('!document.getElementById("export").disabled',timeout=60000)
            assert await page.locator('#rows tr').count()==12
            async with page.expect_download() as dl:
                await page.locator('#export').click()
            payload=json.loads((await (await dl.value).path()).read_text(encoding='utf-8'))
            media_results=payload['results']
            assert payload['scope']=={'fruits':166,'slots':332,'examined':12}
            assert {x['id'] for x in media_results}=={x['id'] for x in selected}
            assert all(x['ok'] and x['width']>0 and x['height']>0 and x['type']=='art' for x in media_results)
            await page.screenshot(path=str(OUT/'media-check.jpg'),type='jpeg',quality=85,full_page=True)
            # Contact sheet is composed from the actual resolved catalogue URLs, not guessed filenames.
            gallery=await context.new_page()
            markup='<meta charset="utf-8"><style>body{margin:16px;background:#eee4cd;color:#322719;font:14px system-ui}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.cell{padding:10px;background:#fff8e8;border:1px solid #a89268}.cell img{display:block;width:384px;height:216px;object-fit:contain;background:white}.cell p{font-size:12px;margin:8px 0;min-height:35px}</style><h1>V4.9.e — illustrations examinées dans Chrome</h1><p>Références externes sous copyright · captures pour audit · aucun fruit physique inventé</p><div class="grid">'
            for f in facts['selected']:
                markup+=f'<div class="cell"><b>{html.escape(f["id"])}</b><p>{html.escape(f["image_kind"])}</p><img data-id="{html.escape(f["id"])}" referrerpolicy="no-referrer" src="{html.escape(f["image"])}"><p>{html.escape(f["visual_description"])}</p></div>'
            await gallery.set_content(markup+'</div>')
            await gallery.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)',timeout=30000)
            for row in results:
                if row['status']=='failed':continue
                png=await gallery.locator('img[data-id="'+row['id']+'"]').screenshot()
                fingerprint=dhash(png);row['dhash64']=fingerprint
                expected=next(x for x in selected if x['id']==row['id']).get('reviewedDhash64')
                if not review:
                    assert expected,'Missing visual review fingerprint: '+row['id']
                    distance=(int(fingerprint,16)^int(expected,16)).bit_count()
                    row['fingerprintDistance']=distance
                    assert distance<=6,'Content changed / possible placeholder: '+row['id']+' distance='+str(distance)
            await gallery.screenshot(path=str(OUT/'contact-validated.jpg'),type='jpeg',quality=90,full_page=True)
            assert not errors,errors
            assert all(x['status']=='loaded-on-real-detail' for x in results),results
            passed=True
            await browser.close()
    finally:
        server.shutdown()
        try:head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        except Exception:head=None
        report={'schema':'demonfruitzdex.illustration-browser-audit.v49e','date':datetime.now(timezone.utc).isoformat(),
          'environment':('GitHub Actions' if os.environ.get('GITHUB_ACTIONS') else 'Local')+' '+platform.system()+' Chrome',
          'commit':head,'passed':passed,'mode':'initial-review' if review else 'reviewed-content-verification',
          'scope':{'fruits':facts.get('fruits'),'portraits':facts.get('portraits'),'artworks':facts.get('artworks'),'videos':facts.get('videos'),'added':12,'remaining':14},
          'errors':errors,'results':results,'mediaCheck':media_results,'captures':captured,
          'limits':'Browser decoding and fingerprint matching do not grant a reuse licence or guarantee permanent/global availability. All originals remain on external hosts.'}
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS V4.9.e Chrome: 12 real details, MEDIA CHECK export, held slot, desktop/tablet/mobile, 166/164/152/50.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--review',action='store_true',help='Initial capture only; requires subsequent visual inspection before committing reviewed fingerprints.')
    asyncio.run(main(parser.parse_args().review))
