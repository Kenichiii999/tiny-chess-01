import json,os,sys,urllib.request as R,random
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
V=(0,100,320,330,500,900,0)
KN=(-33,-31,-18,-14,14,18,31,33)
KI=(-17,-16,-15,-1,1,15,16,17)
SL=((-17,-15,15,17),(-16,-1,1,16),(-17,-16,-15,-1,1,15,16,17))
A="0123456789abcdefghijk"
PT=[(A.index(c)-10)*5 for c in "aaaaaaaabcc66ccbb98aa89baaaeeaaabbcffcbbcceggecckkkkkkkkaaaaaaaa0244442026abba624bcddcb44adeeda44bdeedb44acddca426aaaa6202444420688888868baaaab88cccccc88acccca88bbccbb88abccba88aaaaaa868888886aaabbaaa9aaaaaa99aaaaaa99aaaaaa99aaaaaa99aaaaaa9bccccccbaaaaaaaa688998868abaaaa88bbbbba8aabbbba99abbbba98abbbba88aaaaaa868899886egcaacgeeeaaaaee866666686442244642200224422002244220022442200224"]
_r=random.Random(20261119)
ZT=[[_r.getrandbits(64) for _ in range(128)] for __ in range(13)]
ZS=_r.getrandbits(64)
ZC=[_r.getrandbits(64) for _ in range(16)]
ZE=[_r.getrandbits(64) for _ in range(128)]
B=[0]*128
CA=0;EP=-1;Z=0;KP=[0,0];N=[0];BUD=100000;HIST={};TT={};KIL=[[None,None] for _ in range(200)];H=[]
BK={"philidor-defence|b|5":"OGZQNxMwY+XwwOArPyTLJuQJyoOMJiGyMOyrWIoiUoissiuAi3AuIWOyyaWNNla8ud8dogZYluYcg0","semi-slav|w|5":"6l5j469i01jq3h2gqIhIIQlAgp1pAGGApqAq52qAAPPJ2001Qy","sicilian-alapin|b|5":"PHVGHAziGXWPUWSKZSRJSJXIIyPBKBysJr/+Wa+ma8mjjiiasii3NxMFFxYPxpQHBuab8004baphummee6","slav-defence|w|4":"8o2bcsfnow08sA30rA8909985q8qlAAGqGbttH46511pGN","english-reversed-sicilian|b|4":"JzzpWuulXjpajaYPZpGrPHrBpyyk/UHQUXXbSJajjkkd","english-reversed-sicilian|w|4":"qz5e9il66nbj4601jsnCCssH3H2gHI1N53eGNPPQ3X","ruy-lopez-berlin|b|3":"sHZQPGY+HBGyBvRBQHWBXJBsJAAttffe","ruy-lopez-morphy|w|3":"46oh541ibi8ooxlCCI3Diqaihqqhip43Dy2CyH3202HO","bird-opening|b|3":"OyWPyrMEVGPuJsulsmGrrIXHY+HOzrItOtUXSrmDtmm66drSZXXzdr","italian-game|w|2":"bjsz3hqzh39pjs3c4cpw2k721bc5lCkrfvbhhy244Q04QRRSCIryST5eTQ"}
PR={"sicilian-alapin|b|5":{40:'q'}}
BC=None;BI=0;BO=0;K=''
A="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
def dec(c):
 f=A.index(c[0]);t=A.index(c[1])
 return "abcdefgh"[f&7]+str((f>>3)+1)+"abcdefgh"[t&7]+str((t>>3)+1)
def bset(op,col,rg):
 global BC,BI,BO,K
 K=op+"|"+col[0]+"|"+RUNG.get(rg,"?");BC=BK.get(K);BI=0;BO=1 if BC else 0
RUNG={'depth-2':'0','depth-3':'1','depth-4':'2','nodes-100k':'3','nodes-250k':'4','nodes-500k':'5','nodes-1M':'6','nodes-2M':'7'}
class Bud(Exception):pass
def uci(s):return "abcdefgh"[s&7]+str((s>>4)+1)
def att(s,by):
 for d in (15,17):
  t=s-d*by
  if not t&0x88 and B[t]==by:return 1
 for d in KN:
  t=s+d
  if not t&0x88 and B[t]==by*2:return 1
 for d in KI:
  t=s+d
  if not t&0x88 and B[t]==by*6:return 1
 for d in (-16,-1,1,16):
  t=s+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==by*4 or q==by*5:return 1
    break
   t+=d
 for d in (-17,-15,15,17):
  t=s+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==by*3 or q==by*5:return 1
    break
   t+=d
 return 0
def parse(fen):
 global CA,EP,Z
 p=fen.split();b=[0]*128
 for i,row in enumerate(p[0].split("/")):
  f=0
  for c in row:
   if c.isdigit():f+=int(c)
   else:
    k="PNBRQKpnbrqk".find(c);b[(7-i)*16+f]=(k%6+1)*(1 if k<6 else -1);f+=1
 B[:]=b;side=1 if p[1]=="w" else -1;CA=0
 if "K" in p[2]:CA|=1
 if "Q" in p[2]:CA|=2
 if "k" in p[2]:CA|=4
 if "q" in p[2]:CA|=8
 EP=-1 if p[3]=="-" else (int(p[3][1])-1)*16+ord(p[3][0])-97
 Z=0
 for s in range(128):
  q=b[s]
  if q:Z^=ZT[q+6][s]
  if abs(q)==6:KP[1 if q>0 else 0]=s
 if side<0:Z^=ZS
 Z^=ZC[CA]
 if EP>=0:Z^=ZE[EP]
 return side

def gen(side):
 m=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if p*side<=0:continue
  a=abs(p)
  if a==1:
   f=s+16*side
   if not f&0x88 and not B[f]:
    if (f>>4) in (0,7):
     for q in (5,4,3,2):m.append((s,f,q))
    else:
     m.append((s,f,0))
     if (s>>4)==(1 if side>0 else 6) and not B[s+32*side]:m.append((s,s+32*side,0))
   for d in (15,17):
    t=s+d*side
    if t&0x88:continue
    if B[t]*side<0 or t==EP:
     if (t>>4) in (0,7):
      for q in (5,4,3,2):m.append((s,t,q))
     else:m.append((s,t,0))
  elif a==2:
   for d in KN:
    t=s+d
    if not t&0x88 and B[t]*side<=0:m.append((s,t,0))
  elif a==6:
   for d in KI:
    t=s+d
    if not t&0x88 and B[t]*side<=0:m.append((s,t,0))
  else:
   for d in SL[a-3]:
    t=s+d
    while not t&0x88:
     q=B[t]
     if not q:m.append((s,t,0))
     elif q*side<0:m.append((s,t,0));break
     else:break
     t+=d
 if side>0:
  if CA&1 and not B[5] and not B[6] and B[4]==6 and B[7]==4 and not att(4,-1) and not att(5,-1) and not att(6,-1):m.append((4,6,0))
  if CA&2 and not B[1] and not B[2] and not B[3] and B[4]==6 and B[0]==4 and not att(4,-1) and not att(3,-1) and not att(2,-1):m.append((4,2,0))
 else:
  if CA&4 and not B[117] and not B[118] and B[116]==-6 and B[119]==-4 and not att(116,1) and not att(117,1) and not att(118,1):m.append((116,118,0))
  if CA&8 and not B[113] and not B[114] and not B[115] and B[116]==-6 and B[112]==-4 and not att(116,1) and not att(115,1) and not att(114,1):m.append((116,114,0))
 return m
def make(m,side):
 global CA,EP,Z
 f,t,q=m;p=B[f];c=B[t];cs=t;oz=Z
 if abs(p)==1 and (f&7)!=(t&7) and not c:cs=t-16*side;c=B[cs];B[cs]=0
 B[f]=0;np=q*side if q else p;B[t]=np;rf=0
 if abs(p)==6:
  KP[(side+1)//2]=t
  if abs(t-f)==2:
   if t>f:rf,rt=t+1,t-1
   else:rf,rt=t-2,t+1
   B[rt]=B[rf];B[rf]=0
 Z^=ZT[p+6][f]^ZT[np+6][t]
 if c:Z^=ZT[c+6][cs]
 if rf:Z^=ZT[4*side+6][rf]^ZT[4*side+6][rt]
 Z^=ZS;oc=CA;nc=CA
 if abs(p)==6:nc&=~(3 if side>0 else 12)
 if f==0 or t==0:nc&=~2
 if f==7 or t==7:nc&=~1
 if f==112 or t==112:nc&=~8
 if f==119 or t==119:nc&=~4
 if nc!=oc:Z^=ZC[oc]^ZC[nc]
 oep=EP;nep=f+16*side if abs(p)==1 and abs(t-f)==32 else -1
 if oep>=0:Z^=ZE[oep]
 if nep>=0:Z^=ZE[nep]
 CA,EP=nc,nep
 return (m,c,cs,oc,oep,oz)
def unmake(u,side):
 global CA,EP,Z
 m,c,cs,oc,oep,oz=u;f,t,q=m;p=B[t]
 if abs(p)==6 and abs(t-f)==2:
  if t>f:B[t+1]=B[t-1];B[t-1]=0
  else:B[t-2]=B[t+1];B[t+1]=0
 B[f]=1*side if q else p;B[t]=0
 if c:B[cs]=c
 if abs(p)==6:KP[(side+1)//2]=f
 CA,EP,Z=oc,oep,oz
def ev(side):
 s=0;wb=0;bb=0
 for q in range(128):
  if q&0x88:continue
  p=B[q]
  if p:
   i=((q>>4)<<3)|(q&7)
   if p>0:
    s+=V[p]+PT[(p-1)*64+i]
    if p==3:wb+=1
   else:
    s-=V[-p]+PT[(-p-1)*64+((7-(q>>4))<<3)|(q&7)]
    if p==-3:bb+=1
 if wb>1:s+=30
 if bb>1:s-=30
 return s if side>0 else -s

def mu(m):return uci(m[0])+uci(m[1])+("nbrq"[m[2]-2] if m[2] else "")
def qs(side,al,be,ply):
 N[0]+=1
 if N[0]>BUD:raise Bud
 chk=att(KP[(side+1)//2],-side)
 if not chk:
  s=ev(side)
  if s>=be:return be
  if s>al:al=s
  ms=[m for m in gen(side) if B[m[1]] or m[2] or (abs(B[m[0]])==1 and (m[0]&7)!=(m[1]&7))]
 else:
  ms=gen(side)
  if not ms:return -100000+ply
 ms.sort(key=lambda m:-(10*V[abs(B[m[1]])]-V[abs(B[m[0]])]) if B[m[1]] else -(900+V[m[2]] if m[2] else 0))
 legal=0
 for m in ms:
  u=make(m,side)
  if att(KP[(side+1)//2],-side):unmake(u,side);continue
  legal+=1;v=-qs(-side,-be,-al,ply+1);unmake(u,side)
  if v>=be:return be
  if v>al:al=v
 if chk and not legal:return -100000+ply
 return al
def sr(side,d,al,be,ply):
 N[0]+=1
 if N[0]>BUD:raise Bud
 if Z in H:return 0
 e=TT.get(Z)
 if e and e[0]>=d:
  _,fl,v,bm=e
  if fl==0:return v
  if fl==1 and v>=be:return v
  if fl==2 and v<=al:return v
 inc=att(KP[(side+1)//2],-side)
 if inc:d+=1
 if d<=0:return qs(side,al,be,ply)
 H.append(Z);ms=gen(side)
 ttm=e[3] if e else None
 def ok(m):
  f,t,q=m;c=B[t];s=0
  if m==ttm:s+=1000000
  if c:s+=10*V[abs(c)]-V[abs(B[f])]
  elif q:s+=900+V[q]
  elif m==KIL[ply][0]:s+=800
  elif m==KIL[ply][1]:s+=700
  else:s+=HIST.get((B[f],t),0)
  return -s
 ms.sort(key=ok);ao=al;best=-1000000;bm=None;legal=0
 for i,m in enumerate(ms):
  f,t,q=m
  cap=B[t] or q or (abs(B[f])==1 and (f&7)!=(t&7))
  u=make(m,side)
  if att(KP[(side+1)//2],-side):unmake(u,side);continue
  legal+=1
  if i>=3 and d>=3 and not cap and not inc:
   v=-sr(-side,d-2,-al-1,-al,ply+1)
   if v>al:v=-sr(-side,d-1,-be,-al,ply+1)
  else:v=-sr(-side,d-1,-be,-al,ply+1)
  unmake(u,side)
  if v>best:best=v;bm=m
  if v>al:al=v
  if al>=be:break
 H.pop()
 if not legal:return -100000+ply if att(KP[(side+1)//2],-side) else 0
 if best>=be:fl=1
 elif best>ao:fl=0
 else:fl=2
 if al>=be and not B[bm[1]] and not bm[2]:
  KIL[ply][1]=KIL[ply][0];KIL[ply][0]=bm
  k=(B[bm[0]],bm[1]);HIST[k]=HIST.get(k,0)+d*d
 TT[Z]=(d,fl,best,bm)
 return best
def choose(fen,legal):
 global BI,BO
 if BO and BC and BI*2+2<=len(BC):
  mv=dec(BC[BI*2:BI*2+2])
  p=PR.get(K,{}).get(BI)
  if p:mv+=p
  if mv in legal:BI+=1;return mv
  BO=0
 side=parse(fen);ls=set(legal)
 ms=[m for m in gen(side) if mu(m) in ls]
 if not ms:return legal[0]
 N[0]=0;H.clear();H.append(Z);best=ms[0]
 try:
  for d in range(1,100):
   al=-1000000;be=1000000;bm=None
   for m in ms:
    u=make(m,side);v=-sr(-side,d-1,-be,-al,1);unmake(u,side)
    if v>al:al=v;bm=m
   if bm:
    best=bm;ms.remove(bm);ms.insert(0,bm)
 except Bud:pass
 return mu(best)
def post(p,body):
 req=R.Request(E+p,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with R.urlopen(req) as r:return json.load(r)
 except Exception as e:sys.exit(f"{p}: {e}")
if __name__=="__main__":
 while True:
  g=post("/game",{})
  if g["status"]=="done":break
  bset((g.get("opening") or {}).get("id",""),g.get("colour",""),g.get("opponent",""))
  while g["status"]=="your_move":
   g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
  print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
