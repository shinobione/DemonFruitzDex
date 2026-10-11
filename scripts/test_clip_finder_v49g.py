#!/usr/bin/env python3
"""Real Chromium interaction tests for evidence-first clip discovery.

No web video playback is claimed and no third-party movie is downloaded.
"""
import asyncio,functools,http.server,json,pathlib,threading
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/screenshots/v49g'
async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        async with async_playwright() as playwright:
            browser=await playwright.chromium.launch(headless=True,args=['--no-sandbox'])
            context=await browser.new_context(viewport={'width':1440,'height':900},accept_downloads=True)
            page=await context.new_page()
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            response=await page.goto(f'http://127.0.0.1:{server.server_port}/clip-finder.html',wait_until='domcontentloaded')
            assert response and response.status==200
            await page.wait_for_function("window.SHINO_CLIP_FINDER_AUDIT?.uncovered===130")
            stats=await page.evaluate("window.SHINO_CLIP_FINDER_AUDIT")
            assert stats=={'fruits':166,'clips':50,'covered':36,'uncovered':130,'candidates':3},stats
            assert await page.locator('#rows tr').count()==130
            assert await page.get_by_role('link',name='⌕ Chercher sur YouTube').count()==130
            # Ensure exact fruit matching, and safe URL to existing CLIP CHECK proposals.
            await page.locator('#query').fill('mera mera')
            # Fruit label is French, so ID query makes direct slug discoverable.
            assert await page.locator('#rows tr').count()==1
            row=page.locator('#rows tr').first
            assert 'Feu' in (await row.inner_text())
            search=await row.get_by_text('⌕ Chercher sur YouTube').get_attribute('href')
            proposal=await row.get_by_text('＋ Proposer / vérifier').get_attribute('href')
            assert search.startswith('https://www.youtube.com/results?search_query=')
            assert proposal=='clip-check.html?fruit=mera-mera-no-mi&suggest=1'
            await page.locator('#query').fill('')
            await page.locator('#filter').select_option('covered')
            assert await page.locator('#rows tr').count()==36
            await page.locator('#filter').select_option('missing')
            await page.locator('#tier').select_option('A')
            priority_count=await page.locator('#rows tr').count()
            assert priority_count>=10
            await page.locator('#tier').select_option('all')
            async with page.expect_download() as pending:
                await page.locator('#export').click()
            dl=await pending.value
            content=json.loads(pathlib.Path(await dl.path()).read_text(encoding='utf-8'))
            assert content['schema']=='demonfruitzdex.clip-discovery.v49g'
            assert content['totals']=={'fruits':166,'clips':50,'covered':36,'uncovered':130,'candidates':3}
            assert len(content['items'])==130
            assert not any('youtubeId' in x for x in content['items'])
            assert sum(len(x['publisherCandidates']) for x in content['items'])==3
            assert {x['fruitId'] for x in content['items'] if x['publisherCandidates']}=={
                'mera-mera-no-mi','mero-mero-no-mi','inu-inu-no-mi-mod-le-okuchi-no-makami'}
            assert not any('crunchyroll.com/watch/' in x['youtubeSearch'].lower() for x in content['items'])
            await page.screenshot(path=str(OUT/'clip-finder-desktop.jpg'),type='jpeg',quality=80,full_page=True)
            # Cross-check integration with existing user-proposal interface.
            # Publisher clips are reviewable but not included in the 50 published videos.
            await page.goto(f'http://127.0.0.1:{server.server_port}/clip-check.html?fruit=mera-mera-no-mi&video=bAShh8lXaUI',wait_until='domcontentloaded')
            await page.wait_for_function("document.getElementById('external')?.href.includes('bAShh8lXaUI')")
            assert 'CANDIDAT NON PUBLIÉ' in (await page.locator('#subtitle').inner_text())
            assert '50 associations publiées' in (await page.locator('#stats').inner_text())
            assert '3 candidats officiels' in (await page.locator('#stats').inner_text())
            await page.locator('#verdict').select_option('embed-ok')
            await page.locator('#loggedOut').check()
            await page.locator('#notes').fill('Test navigateur automatisé : verdict de démonstration, non une validation réelle de lecture.')
            await page.locator('#save').click()
            async with page.expect_download() as review_info:
                await page.locator('#export').click()
            review=await review_info.value
            report=json.loads(pathlib.Path(await review.path()).read_text(encoding='utf-8'))
            assert report['catalogueCount']==50 and report['candidateCount']==3
            chosen=[row for row in report['results'] if row['videoId']=='bAShh8lXaUI']
            assert len(chosen)==1 and chosen[0]['candidate'] is True
            assert chosen[0]['verdict']=='embed-ok' and chosen[0]['testedWithoutAccount'] is True
            assert chosen[0]['selfReportedDossierComplete'] is False, "Iframe alone cannot certify a clip"
            assert chosen[0]['powerObserved'] is False
            # Gate rejects a missing/invalid timestamp and requires human declarations.
            await page.locator('#powerObserved').check()
            await page.locator('#publisherConfirmed').check()
            await page.locator('#shortClipConfirmed').check()
            await page.locator('#powerTimecode').fill('bad timecode')
            await page.locator('#save').click()
            assert 'Timecode invalide' in (await page.locator('#status').inner_text())
            await page.locator('#powerTimecode').fill('00:18')
            await page.locator('#save').click()
            assert 'Dossier déclaratif complet' in (await page.locator('#reviewGate').inner_text())
            async with page.expect_download() as full_review_info:
                await page.locator('#export').click()
            full_review=await full_review_info.value
            complete=json.loads(pathlib.Path(await full_review.path()).read_text(encoding='utf-8'))
            record=next(x for x in complete['results'] if x['videoId']=='bAShh8lXaUI')
            assert record['selfReportedDossierComplete'] is True
            assert record['powerTimecode']=='00:18'
            assert record['publisherConfirmed'] and record['powerObserved'] and record['shortClipConfirmed']
            assert complete['catalogueCount']==50 and complete['candidateCount']==3
            await page.screenshot(path=str(OUT/'clip-check-proof-g3-desktop.jpg'),type='jpeg',quality=81,full_page=True)
            await page.goto(f'http://127.0.0.1:{server.server_port}/clip-check.html?fruit=mera-mera-no-mi&suggest=1',wait_until='domcontentloaded')
            await page.wait_for_function("document.getElementById('proposeFruit')?.value==='mera-mera-no-mi'")
            assert not errors,errors
            mobile=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
            mobile_errors=[]
            mobile.on('pageerror',lambda err:mobile_errors.append(str(err)))
            await mobile.goto(f'http://127.0.0.1:{server.server_port}/clip-finder.html',wait_until='domcontentloaded')
            await mobile.wait_for_function("window.SHINO_CLIP_FINDER_AUDIT?.uncovered===130")
            width=await mobile.evaluate("({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth})")
            assert width['scroll']<=width['client']+1,width
            await mobile.screenshot(path=str(OUT/'clip-finder-mobile.jpg'),type='jpeg',quality=79,full_page=True)
            await mobile.goto(f'http://127.0.0.1:{server.server_port}/clip-check.html?fruit=mera-mera-no-mi&video=bAShh8lXaUI',wait_until='domcontentloaded')
            await mobile.wait_for_function("document.getElementById('powerObserved')!==null")
            audit_width=await mobile.evaluate("({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth})")
            assert audit_width['scroll']<=audit_width['client']+1,audit_width
            await mobile.screenshot(path=str(OUT/'clip-check-proof-g3-mobile.jpg'),type='jpeg',quality=80,full_page=True)

            assert not mobile_errors,mobile_errors
            print('PASS V49G_CLIP_FINDER='+json.dumps({'stats':stats,'prioritizedA':priority_count,
                  'publisherCandidates':3,'desktop':'reports/screenshots/v49g/clip-finder-desktop.jpg',
                  'mobile':'reports/screenshots/v49g/clip-finder-mobile.jpg','mobileWidth':width},
                  ensure_ascii=False),flush=True)
            await browser.close()
    finally:server.shutdown()
asyncio.run(main())
