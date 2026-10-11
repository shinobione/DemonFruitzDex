#!/usr/bin/env python3
"""Validate and capture V4.9.c4 in Chrome, with GitHub Pages-relative asset paths.

Visual snapshots are review artifacts, not assertions that YouTube media actually plays.
"""
import functools
import http.server
import json
import pathlib
import os
import threading
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/os.environ.get('SHINO_CAPTURE_DIR','reports/screenshots/v49c4')
OUT.mkdir(parents=True,exist_ok=True)
class SiteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/DemonFruitzDex/"):
            self.path=self.path[len("/DemonFruitzDex"):]
        super().do_GET()
    def log_message(self,*args):
        pass
handler=functools.partial(SiteHandler,directory=str(ROOT))
httpd=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
thread=threading.Thread(target=httpd.serve_forever,daemon=True)
thread.start()
url=f"http://127.0.0.1:{httpd.server_port}/DemonFruitzDex/"
results=[]

def snapshot(page,name,suffix=""):
    target=OUT/f"ci-v49c4-{name}{suffix}.jpg"
    page.screenshot(path=str(target),type="jpeg",quality=83,animations="disabled")
    print(f"SCREENSHOT {target.relative_to(ROOT)} ({target.stat().st_size} bytes)",flush=True)

def no_overflow(page,selector="html"):
    box=page.locator(selector).evaluate("el => ({client:el.clientWidth,scroll:el.scrollWidth})")
    assert box["scroll"]<=box["client"]+1, f"{selector}: horizontal overflow {box}"
    return box

def contrast(rgb,paper=(196,161,107)):
    def luminance(values):
        c=[v/255 for v in values]
        c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c]
        return sum(v*w for v,w in zip(c,(.2126,.7152,.0722)))
    a,b=sorted((luminance(rgb),luminance(paper)))
    return (b+.05)/(a+.05)

try:
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox"])
        for name,width,height in [("wide",1920,1080),("desktop",1440,900),("tablet",768,1024),("mobile",390,844),("compact",360,800)]:
            context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,
                                        reduced_motion="reduce",has_touch=width<600,is_mobile=width<600)
            page=context.new_page()
            errors=[]
            missing=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("response",lambda r:missing.append(r.url) if r.url.startswith(url) and r.status>=400 else None)
            page.goto(url,wait_until="networkidle",timeout=30000)
            page.locator(".hero-stage").wait_for(timeout=15000)
            page.wait_for_function("document.fonts.status === 'loaded'",timeout=12000)
            css=page.evaluate("""() => ({
                bg: getComputedStyle(document.body).backgroundImage,
                bgRepeat: getComputedStyle(document.body).backgroundRepeat,
                bgSize: getComputedStyle(document.body).backgroundSize,
                bgAttachment: getComputedStyle(document.body).backgroundAttachment,
                stage: getComputedStyle(document.querySelector('.hero-stage')).backgroundImage,
                stageRepeat: getComputedStyle(document.querySelector('.hero-stage')).backgroundRepeat,
                stageSize: getComputedStyle(document.querySelector('.hero-stage')).backgroundSize,
                stageGrid: getComputedStyle(document.querySelector('.hero-stage'), '::before').backgroundImage,
                heroRepeat: getComputedStyle(document.querySelector('.hero')).backgroundRepeat,
                wear: getComputedStyle(document.body,'::before').backgroundImage,
                wearShadow: getComputedStyle(document.body,'::before').boxShadow,
                wearEvents: getComputedStyle(document.body,'::before').pointerEvents,
                frame: getComputedStyle(document.body,'::after').borderTopWidth,
                frameEvents: getComputedStyle(document.body,'::after').pointerEvents,
                heroInk: getComputedStyle(document.querySelector('.hero h1')).color,
                sectionInk: getComputedStyle(document.querySelector('.spotlight h2')).color,
                columns: getComputedStyle(document.querySelector('.cards')).gridTemplateColumns,
                fruits: window.SHINO_DATA.length,
                videos: Object.values(window.SHINO_CLIPS).reduce((n,r)=>n+(r.youtubeId?1:0)+(r.moreVideos||[]).length,0),
                horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1,
                title: document.title
            })""")
            if css["horizontalOverflow"]:
                raise AssertionError(f"{name}: horizontal overflow")
            if "parchment-bg.webp" not in css["bg"] or "parchment-bg.webp" not in css["stage"]:
                raise AssertionError(f"{name}: parchment texture not applied")
            if any(v.strip()!="no-repeat" for v in css["bgRepeat"].split(",")):
                raise AssertionError(f"{name}: parchment background repeats {css['bgRepeat']}")
            if any(v.strip()!="no-repeat" for v in css["stageRepeat"].split(",")):
                raise AssertionError(f"{name}: hero parchment background repeats {css['stageRepeat']}")
            if any(v.strip()!="cover" for v in css["bgSize"].split(",")):
                raise AssertionError(f"{name}: background not full-viewport cover {css['bgSize']}")
            if any(v.strip()!="fixed" for v in css["bgAttachment"].split(",")):
                raise AssertionError(f"{name}: background not fixed to viewport {css['bgAttachment']}")
            assert all(v.strip()=="no-repeat" for v in css["heroRepeat"].split(",")), f"{name}: hero frame repeats"
            assert all(v.strip()=="cover" for v in css["stageSize"].split(",")), f"{name}: plate is not cover"
            assert css["stageGrid"]=="none", f"{name}: modern repeating grid reintroduced"
            assert css["wear"]!="none" and css["wearShadow"]!="none" and css["frame"]=="1px", f"{name}: manuscript edges absent"
            assert css["wearEvents"]==css["frameEvents"]=="none", f"{name}: frame could intercept controls"
            assert css["heroInk"]=="rgb(36, 26, 17)" and css["sectionInk"]=="rgb(37, 26, 16)", f"{name}: pale headings on paper"
            assert css["fruits"]==166 and css["videos"]==50, f"{name}: catalogue changed"
            assert css["title"].startswith("DemonFruitzDex — SHINO-DEX V4.9."), f"{name}: unexpected site edition"

            asset=page.request.get(url+"assets/bg/parchment-bg.webp")
            if asset.status!=200:
                raise AssertionError(f"{name}: parchment asset {asset.status}")
            image=page.evaluate("""async url => {const im=new Image(); im.src=url; await im.decode(); return {width:im.naturalWidth,height:im.naturalHeight};}""",url+"assets/bg/parchment-bg.webp")
            assert image=={"width":1536,"height":1024}, f"{name}: parchment did not decode"
            snapshot(page,name)
            page.locator('#nouveaux-clips').evaluate("el => el.scrollIntoView({block:'start'})")
            no_overflow(page)
            after_scroll=page.evaluate("getComputedStyle(document.body).backgroundPosition")
            assert after_scroll=="50% 50%, 50% 50%, 50% 50%", f"{name}: paper crop changed on scroll"
            snapshot(page,name,"-scrolled")
            page.locator('#catalogue').evaluate("el => el.scrollIntoView({block:'start'})")
            no_overflow(page)
            if name in ("desktop","mobile"):
                snapshot(page,name,"-catalogue")

            # All interaction data stays in this disposable browser context.
            page.locator('#search').fill('Opération')
            assert int(page.locator('#resultsCount').inner_text())>=1
            page.locator('#reset').click()
            chip=page.locator('[data-type="Logia"]')
            chip.tap() if width<600 else chip.click()
            assert page.locator('.category').evaluate_all("es=>es.every(e=>e.textContent==='Logia')")
            page.locator('#reset').click()
            page.locator('.fav-btn').first.click()
            assert page.locator('#favoriteCount').inner_text()=='1'
            page.reload(wait_until="networkidle")
            assert page.locator('#favoriteCount').inner_text()=='1'
            page.locator('#onlyFavorite').check()
            assert page.locator('#resultsCount').inner_text()=='1'
            page.locator('#reset').click()
            for index in (0,1):
                page.locator('.cmp-btn').nth(index).click()
            page.locator('#compareOpen').click()
            no_overflow(page,'#compareDialog')
            assert page.locator('.compare-col').count()==2
            if name in ("desktop","mobile"):
                snapshot(page,name,"-compare")
            page.keyboard.press('Escape')

            page.goto(url+'?fruit=hito-hito-no-mi-mod-le-nika&clip=5L_Ek_CcREc',wait_until="networkidle")
            page.locator('#detailDialog[open]').wait_for()
            detail=no_overflow(page,'#detailDialog')
            assert page.locator('#clipYoutubeSource').get_attribute('href')=='https://www.youtube.com/watch?v=5L_Ek_CcREc'
            portrait=page.locator('.detail-character-hero').evaluate('el=>el.getBoundingClientRect().height')
            assert portrait==(370 if width<=540 else 420)
            if name in ("desktop","mobile"):
                snapshot(page,name,"-detail")
            page.locator('#officialPlay').click()
            assert '/5L_Ek_CcREc?' in page.locator('#officialClipFrame').get_attribute('src')
            page.locator('#detailDialog').evaluate('el=>el.scrollTop=el.scrollHeight')
            if name in ("desktop","mobile"):
                snapshot(page,name,"-detail-scrolled")
            page.locator('#detailNext').click()
            assert page.locator('#officialClipFrame').count()==0
            assert 'fruit=hito-hito-no-mi-mod-le-nika' not in page.url
            page.keyboard.press('Escape')

            for tool in ('clip-check.html','media-check.html'):
                page.goto(url+tool,wait_until="networkidle")
                no_overflow(page)
                intro=page.locator('.head > p' if tool=='clip-check.html' else 'main > p').first
                assert intro.evaluate('el=>getComputedStyle(el).color')=='rgb(51, 34, 23)', f"{name}: pale tool introduction on paper"
                if tool=='clip-check.html':
                    assert page.locator('.head h1 small').evaluate('el=>getComputedStyle(el).color')=='rgb(77, 49, 32)', f"{name}: pale tool version on paper"
                else:
                    assert page.locator('#summary').evaluate('el=>getComputedStyle(el).color')=='rgb(51, 34, 23)', f"{name}: pale media summary on paper"
                if name in ("desktop","mobile"):
                    snapshot(page,name,'-'+tool.replace('.html',''))
                if tool=='clip-check.html':
                    assert page.locator('.item').count()>0
                    page.locator('#play').click()
                    assert page.locator('#preview iframe').get_attribute('src').startswith('https://www.youtube-nocookie.com/embed/')
                    page.locator('#proposeUrl').fill('https://youtu.be/abcdefghijk')
                    page.locator('#proposeAdd').click()
                    assert 'abcdefghijk' in page.locator('#proposalList').inner_text()
                else:
                    assert '166 fiches' in page.locator('#summary').inner_text()

            page.goto(url,wait_until="networkidle")
            page.emulate_media(reduced_motion="no-preference")
            assert page.locator('.stage-fruit').evaluate('el=>getComputedStyle(el).animationDuration')=='5s'
            page.emulate_media(reduced_motion="reduce")
            assert float(page.locator('.stage-fruit').evaluate('el=>parseFloat(getComputedStyle(el).animationDuration)'))<.001
            palette={"title/paper":contrast((36,26,17)),"copy/paper":contrast((51,34,23)),"caption/paper":contrast((77,49,32))}
            assert min(palette.values())>=4.5
            assert not errors and not missing, f"{name}: JS errors {errors}; missing local resources {missing}"
            results.append({"viewport":[width,height],"css":css,"asset":image,"detail":detail,"portraitHeight":portrait,"contrast":palette,"errors":errors,"missingLocal":missing})
            print(f"PASS {name} {width}x{height}: sheet, frames, overflow, catalogue, interactions, tools, reduced motion",flush=True)
            context.close()
        browser.close()
    (OUT/'validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
finally:
    httpd.shutdown()
print("PASS V4.9.c4 Chrome: five viewports, decoded non-repeating cover parchment, manuscript borders, unchanged 166/50 catalogue.",flush=True)
