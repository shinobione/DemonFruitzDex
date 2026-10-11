#!/usr/bin/env python3
"""Probe candidate Wiki filenames for two missing specific-character portraits.

Status is a *browser observation*, not image-authenticity or republication rights.
Produces a contact sheet to review visually before selecting any filename.
"""
import asyncio, hashlib, json, pathlib, re
from playwright.async_api import async_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'/'media-candidate-probe-v49d.json'
names=[
 ('oshi-oshi-no-mi','Morley','Morley Portrait.png'),
 ('oshi-oshi-no-mi','Morley','Morley Anime Infobox.png'),
 ('oshi-oshi-no-mi','Morley','Morley Manga Infobox.png'),
 ('oshi-oshi-no-mi','Morley','Morley Infobox.png'),
 ('oshi-oshi-no-mi','Morley','Morley Anime Concept Art.png'),
 ('tsutsu-tsutsu-no-mi','Urban','Urban Portrait.png'),
 ('tsutsu-tsutsu-no-mi','Urban','Urban Anime Infobox.png'),
 ('tsutsu-tsutsu-no-mi','Urban','Urban Manga Infobox.png'),
 ('tsutsu-tsutsu-no-mi','Urban','Urban Infobox.png'),
 ('tsutsu-tsutsu-no-mi','Urban','Urban Concept Art.png'),
]
# Replace 26 old images that resolve to the wiki's generic 300x171 placeholder.
audit=json.loads((ROOT/'reports'/'media-browser-audit-v49d.json').read_text(encoding='utf-8'))
inventory=json.loads((ROOT/'reports'/'media-inventory-v49d.json').read_text(encoding='utf-8'))
by_id={r['id']:r for r in inventory['records']}
for old in audit['results']:
    if old['kind']!='portrait' or (old['direct']['width'],old['direct']['height'])!=(300,171):
        continue
    original=by_id[old['id']]['portrait']['filename']
    if not original:continue
    candidate=re.sub(r' (Anime|Manga) Infobox\.png$', ' Portrait.png', original)
    if candidate==original:continue
    names.append((old['id'],old['holder'],candidate))
    if candidate=="Kinemon Portrait.png":names.append((old['id'],old['holder'],"Kin'emon Portrait.png"))
    if candidate=="Charlotte Brulee Portrait.png":names.append((old['id'],old['holder'],"Charlotte Brûlée Portrait.png"))
names=list(dict.fromkeys(names))

def link(filename):
    base=filename.replace(' ','_')
    h=hashlib.md5(base.encode('utf-8')).hexdigest()
    return f'https://static.wikia.nocookie.net/onepiece/images/{h[0]}/{h[:2]}/{base}/revision/latest'

async def main():
    candidates=[{'fruitId':a,'character':b,'filename':c,'url':link(c)} for a,b,c in names]
    async with async_playwright() as p:
        browser=await p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1520,'height':1280},device_scale_factor=1)
        await page.goto('about:blank')
        states=await page.evaluate("""async (items)=>{
          return await Promise.all(items.map(x=>new Promise(resolve=>{
            let img=new Image(),finished=false;img.referrerPolicy='no-referrer';
            const timer=setTimeout(()=>finish('timeout'),9000);
            function finish(status){if(finished)return;finished=true;clearTimeout(timer);resolve({...x,status,width:img.naturalWidth||0,height:img.naturalHeight||0})}
            img.onload=()=>finish(img.naturalWidth===300&&img.naturalHeight===171?'placeholder':img.naturalWidth>0?'loaded':'empty');
            img.onerror=()=>finish('error');img.src=x.url;
          })));
        }""",candidates)
        # Contact sheet, loaded images only; incorrect candidates remain visibly labeled.
        pageHtml='<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#232831;color:#fff;font-family:Arial,sans-serif;padding:15px}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.item{padding:10px;background:#404753;border:1px solid #949ead;border-radius:10px}.item img{width:100%;height:245px;object-fit:contain;background:#10161f}.item p{height:49px;font-size:14px;margin:5px 0}.ok{color:#76df9f}.fail{color:#ff9292}</style><div class="grid">'
        for x in states:
            pageHtml+=f'<div class="item"><p>{x["character"]} — {x["filename"]}</p><img src="{x["url"]}" referrerpolicy="no-referrer"><p class="{"ok" if x["status"]=="loaded" else "fail"}">{x["status"]} {x["width"]}x{x["height"]}</p></div>'
        pageHtml+='</div>'
        await page.set_content(pageHtml)
        await page.wait_for_timeout(3500)
        sheet=ROOT/'reports'/'media-candidate-contact-v49d.jpg'
        await page.screenshot(path=str(sheet),type='jpeg',quality=75,full_page=True)
        await browser.close()
    data={'schema':'demonfruitzdex.media-candidates.v49d','status':'exploratory-browser-probe','candidates':states,
          'note':'Do not integrate by image load alone: visually confirm actual person and file provenance; images are externally linked only.'}
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for item in states:
        print('CANDIDATE_CHECK='+json.dumps({k:item[k] for k in ['fruitId','filename','url','status','width','height']},ensure_ascii=False),flush=True)
    print('CANDIDATE_CONTACT_SHEET='+str(sheet.relative_to(ROOT)),flush=True)

asyncio.run(main())
