"""Procedural, original silent animations: no copyrighted anime footage."""
from PIL import Image, ImageDraw, ImageFilter
import math, numpy as np, subprocess, random
from pathlib import Path
OUT=Path(__file__).resolve().parent.parent/'assets'/'powers'; OUT.mkdir(parents=True, exist_ok=True)
W,H=480,270; FPS=18; N=54
X,Y=np.meshgrid(np.arange(W,dtype=np.float32), np.arange(H,dtype=np.float32))
rng=np.random.default_rng(84)
particles=[(float(rng.uniform(0,W)),float(rng.uniform(0,H)),float(rng.uniform(1.0,5.0)),float(rng.uniform(0,2*math.pi))) for i in range(48)]

def frames_for(kind,t):
    cx,cy=W/2,H/2
    rr=np.sqrt((X-cx)**2+(Y-cy)**2)
    theta=np.arctan2(Y-cy,X-cx)
    wave=np.sin(theta*7-2*math.pi*t*2 + rr*.04)
    if kind=='fire':
        core=np.exp(-(rr/(90+15*np.sin(2*math.pi*t)))**2)
        field=np.maximum(0, np.sin((X*0.055)+8*Y/270+8*t)+.5*np.sin(Y*.09+X*.02-6*t))
        a=np.clip(.06+core*1.15+field*.18,0,1)
        colors=[24,8,18]; glow=[255,80+int(30*math.sin(2*math.pi*t)**2),25]
    elif kind=='lightning':
        core=np.exp(-(rr/(70+10*np.sin(2*math.pi*t*3)))**2)
        a=np.clip(.06+core*.8+(.5+.5*np.sin(rr*.16-14*t))*np.exp(-rr/145)*.32,0,1)
        colors=[7,17,33];glow=[52,188,255]
    elif kind=='darkness':
        a=np.clip(.08+(1-np.exp(-rr/130))*.22 + (.5+.5*np.sin(theta*9+rr*.085-6*t))*.25*np.exp(-rr/160),0,1)
        colors=[4,4,14];glow=[103,63,192]
    elif kind=='ice':
        core=np.exp(-(rr/145)**2)
        a=np.clip(.08+core*.42+(.5+.5*np.cos((X+Y)*.05+t*2*math.pi))*.08,0,1)
        colors=[6,19,33];glow=[107,212,255]
    elif kind=='gravity':
        center=(.5+.5*np.sin(theta*8+rr*.07-2*math.pi*t))*np.exp(-rr/160)
        a=np.clip(.12+center*.5+np.exp(-((rr-(75+3*math.sin(2*math.pi*t)))/20)**2)*.3,0,1)
        colors=[10,7,20];glow=[177,116,255]
    elif kind=='rubber':
        a=np.clip(.08+.35*np.exp(-rr/200)+(.5+.5*np.sin((rr-40*np.sin(theta*5-6.28*t))*.08))*np.exp(-rr/155)*.26,0,1)
        colors=[10,11,25];glow=[240,240,255]
    else:raise ValueError(kind)
    base=np.array(colors)[None,None,:]*(1-a[:,:,None])+np.array(glow)[None,None,:]*a[:,:,None]
    im=Image.fromarray(np.uint8(np.clip(base,0,255)),'RGB').convert('RGBA')
    overlay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(overlay,'RGBA')
    if kind=='fire':
      for idx,(px,py,s,phase) in enumerate(particles):
        x=(px+25*math.sin(phase+2*math.pi*t))%W
        y=(py - t*(65+idx%6*14))%H
        radius=max(1,int(s/1.3))
        d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(255,200+idx%55,42,180))
      for n in range(9):
        ph=2*math.pi*(n/9+t)
        x=cx+80*math.sin(ph)+30*math.sin(3*ph); y=cy+44*math.cos(ph)
        d.arc((x-30,y-40,x+30,y+40),40,220,fill=(255,172,55,95),width=5)
    elif kind=='lightning':
      for branch in range(5):
        phase=branch*1.7+2*math.pi*t
        coords=[]
        for i in range(14):
          yy=15+i*18
          xx=cx+120*math.sin(phase+branch)+19*math.sin(i*2.7+phase) + 30*math.sin(i*.43+phase)
          coords.append((xx,yy))
        d.line(coords,fill=(88,208,255,180),width=7,joint='curve')
        d.line(coords,fill=(224,251,255,245),width=2,joint='curve')
      for px,py,s,phase in particles[:22]:
        dx=(px+30*math.sin(phase+2*math.pi*t))%W
        dy=(py+22*math.cos(phase-2*math.pi*t))%H
        d.line(((dx-s*3,dy),(dx+s*3,dy)),fill=(150,235,255,135),width=2)
    elif kind=='darkness':
      for n in range(12):
        angle=n*math.pi/6+2*math.pi*t
        rad=70+22*math.sin(angle*3)
        x=cx+rad*math.cos(angle);y=cy+rad*.64*math.sin(angle)
        d.arc((x-45,y-45,x+45,y+45),n*26,n*26+190,fill=(155,95,255,95),width=3)
      d.ellipse((cx-63,cy-63,cx+63,cy+63),fill=(1,2,10,255),outline=(102,61,184,225),width=4)
      d.ellipse((cx-43,cy-43,cx+43,cy+43),outline=(189,128,245,110),width=2)
    elif kind=='ice':
      for n in range(28):
        x,y,s,phase=particles[n]
        x=(x+6*math.sin(phase+2*math.pi*t))%W
        y=(y+17*t)%H
        d.line([(x-5,y),(x+5,y)],fill=(196,241,255,130),width=2)
        d.line([(x,y-5),(x,y+5)],fill=(196,241,255,130),width=2)
      for n in range(10):
        angle=2*math.pi*n/10+.2*math.sin(t*2*math.pi)
        outer=60+40*(n%3)/2
        x=cx+outer*math.cos(angle);y=cy+outer*.8*math.sin(angle)
        d.polygon([(x,y-22),(x+9,y),(x,y+22),(x-9,y)],fill=(94,198,255,95),outline=(194,243,255,175))
    elif kind=='gravity':
      for n in range(8):
        r=46+n*15+5*math.sin(6.28*t+n)
        d.ellipse((cx-r,cy-r*.50,cx+r,cy+r*.50),outline=(200,145,255,120+n*8),width=2)
      for n in range(15):
        angle=2*math.pi*n/15+2*math.pi*t
        r=95+65*((n%5)/5)
        x=cx+r*math.cos(angle); y=cy+r*.5*math.sin(angle)
        d.ellipse((x-3,y-3,x+3,y+3),fill=(204,157,255,180))
      d.ellipse((cx-20,cy-20,cx+20,cy+20),fill=(225,186,255,110))
    elif kind=='rubber':
      for n in range(6):
        angle=2*math.pi*(n/6+t)
        stretch=85+28*math.sin(2*math.pi*t+n)
        x=cx+stretch*math.cos(angle);y=cy+stretch*.56*math.sin(angle)
        d.arc((x-50,y-50,x+50,y+50),30,330,fill=(237,245,255,165),width=6)
      d.ellipse((cx-34,cy-34,cx+34,cy+34),fill=(242,244,255,55),outline=(242,244,255,180),width=3)
    overlay=overlay.filter(ImageFilter.GaussianBlur(radius=0.4))
    return Image.alpha_composite(im,overlay).convert('RGB')

for kind in ['fire','lightning','darkness','ice','gravity','rubber']:
    outfile=OUT/(kind+'.mp4')
    cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart',str(outfile)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
      for j in range(N):proc.stdin.write(np.asarray(frames_for(kind,j/N)).tobytes())
      proc.stdin.close()
      err=proc.stderr.read(); rc=proc.wait()
      if rc:raise RuntimeError(f'{kind}: {err.decode()[-700:]}')
    finally:
      if proc.poll() is None:proc.kill()
    print(kind, outfile.stat().st_size, 'bytes')
