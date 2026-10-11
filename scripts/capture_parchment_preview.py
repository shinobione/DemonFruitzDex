#!/usr/bin/env python3
"""Capture the actual V4.9.c3 parchment in headless Chrome, on GitHub Pages-like static hosting.

Visual snapshots are review artifacts, not assertions that YouTube media actually plays.
"""
import base64
import contextlib
import functools
import http.server
import pathlib
import threading
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"reports"/"screenshots"/"v49c"
OUT.mkdir(parents=True,exist_ok=True)
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
httpd=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
thread=threading.Thread(target=httpd.serve_forever,daemon=True)
thread.start()
url=f"http://127.0.0.1:{httpd.server_port}/index.html"
try:
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox"])
        for name,width,height in [("desktop",1440,900),("mobile",390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1,reduced_motion="reduce")
            page.goto(url,wait_until="domcontentloaded",timeout=20000)
            page.locator(".hero-stage").wait_for(timeout=15000)
            page.wait_for_function("document.fonts.status === 'loaded'",timeout=12000)
            css=page.evaluate("""() => ({
                bg: getComputedStyle(document.body).backgroundImage,
                bgRepeat: getComputedStyle(document.body).backgroundRepeat,
                bgSize: getComputedStyle(document.body).backgroundSize,
                bgAttachment: getComputedStyle(document.body).backgroundAttachment,
                stage: getComputedStyle(document.querySelector('.hero-stage')).backgroundImage,
                stageRepeat: getComputedStyle(document.querySelector('.hero-stage')).backgroundRepeat,
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

            asset=page.request.get(f"http://127.0.0.1:{httpd.server_port}/assets/bg/parchment-bg.webp")
            if asset.status!=200:
                raise AssertionError(f"{name}: parchment asset {asset.status}")
            shot=page.screenshot(type="jpeg",quality=75,animations="disabled")
            target=OUT/f"ci-v49c3-{name}.jpg"
            target.write_bytes(shot)
            print(f"SCREENSHOT_{name.upper()} path={target.relative_to(ROOT)} size={len(shot)} title={css['title']}",flush=True)
            if name=="desktop":
                print("PARCHMENT_PREVIEW_BASE64_BEGIN"+base64.b64encode(shot).decode("ascii")+"PARCHMENT_PREVIEW_BASE64_END",flush=True)
            elif name=="mobile":
                print("PARCHMENT_MOBILE_BASE64_BEGIN"+base64.b64encode(shot).decode("ascii")+"PARCHMENT_MOBILE_BASE64_END",flush=True)
            # Also inspect the paper after scrolling beyond the fold.
            page.evaluate("window.scrollTo(0, Math.min(950, document.body.scrollHeight - innerHeight))")
            page.wait_for_timeout(100)
            below=page.screenshot(type="jpeg",quality=74,animations="disabled")
            belowTarget=OUT/f"ci-v49c3-{name}-scrolled.jpg"
            belowTarget.write_bytes(below)
            print(f"SCROLLED_{name.upper()} path={belowTarget.relative_to(ROOT)} size={len(below)}",flush=True)
            page.close()
        browser.close()
finally:
    httpd.shutdown()
print("PASS V4.9.c3 Chrome screenshots: real parchment asset loaded, desktop/mobile CSS active, no overflow.",flush=True)
