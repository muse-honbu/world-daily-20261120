#!/usr/bin/env python3
"""Dense newspaper front page for 20 November 2026 - make.fun entry.
Pure standard library. Deterministic: no random, no time, no env in image.
Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png locally).
"""
import os, struct, zlib

W, H = 1024, 1024
# colours RGB
WHITE=(255,255,255); BLACK=(18,18,18); DARK=(45,45,45); GREY=(120,120,120)
LIGHT=(238,238,232); MIDGREY=(200,200,195); RED=(185,30,30); BLUE=(30,80,160)
SKY=(170,205,235); NAVY=(25,45,95); ORANGE=(235,130,30); YELLOW=(245,200,40)
GREEN=(35,140,70); BROWN=(140,95,55); SAND=(235,215,160); TEAL=(20,150,150)
PINK=(235,150,180); PURPLE=(110,70,160); CYAN=(120,220,230)

pix = bytearray(W*H*3)
def set_px(x,y,c):
    if 0 <= x < W and 0 <= y < H:
        i=(y*W+x)*3; pix[i]=c[0]; pix[i+1]=c[1]; pix[i+2]=c[2]
def rect(x,y,w,h,c):
    for yy in range(y,y+h):
        for xx in range(x,x+w): set_px(xx,yy,c)
def frame(x,y,w,h,c,t=2):
    rect(x,y,w,t,c); rect(x,y+h-t,w,t,c); rect(x,y,t,h,c); rect(x+w-t,y,t,h,c)
def line(x0,y0,x1,y1,c,t=2):
    steps=max(abs(x1-x0),abs(y1-y0),1)
    for s in range(steps+1):
        x=int(x0+(x1-x0)*s/steps); y=int(y0+(y1-y0)*s/steps)
        for dy in range(t):
            for dx in range(t): set_px(x+dx,y+dy,c)
def circle(cx,cy,r,c,fill=True):
    for yy in range(cy-r,cy+r+1):
        for xx in range(cx-r,cx+r+1):
            d=(xx-cx)*(xx-cx)+(yy-cy)*(yy-cy)
            if fill and d<=r*r: set_px(xx,yy,c)
            if not fill and r*r-2*r<=d<=r*r: set_px(xx,yy,c)
def tri(x,y,s,c,down=False):
    for row in range(s):
        wdt=s-row if not down else row+1
        for xx in range(x-wdt//2,x+wdt//2): set_px(xx,y+row,c)

# ---- 5x7 bitmap font ----
FONT={
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'C':["01110","10001","10000","10000","10000","10001","01110"],
'D':["11100","10010","10001","10001","10001","10010","11100"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'G':["01110","10001","10000","10111","10001","10001","01111"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["01110","00100","00100","00100","00100","00100","01110"],
'J':["00111","00010","00010","00010","00010","10010","01100"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'N':["10001","11001","10101","10011","10001","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'Q':["01110","10001","10001","10001","10101","10010","01101"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'W':["10001","10001","10001","10101","10101","10101","01010"],
'X':["10001","01010","00100","00100","00100","01010","10001"],
'Y':["10001","01010","00100","00100","00100","00100","00100"],
'Z':["11111","00001","00010","00100","01000","10000","11111"],
'0':["01110","10001","10011","10101","11001","10001","01110"],
'1':["00100","01100","00100","00100","00100","00100","01110"],
'2':["01110","10001","00001","00110","01000","10000","11111"],
'3':["11110","00001","00001","01110","00001","00001","11110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","11110","00001","00001","10001","01110"],
'6':["01110","10000","10000","11110","10001","10001","01110"],
'7':["11111","00001","00010","00100","01000","01000","01000"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00001","01110"],
' ':["00000"]*7, '.':["00000","00000","00000","00000","00000","01100","01100"],
',':["00000","00000","00000","00000","01100","00100","01000"],
"'":["00100","00100","01000","00000","00000","00000","00000"],
'-':["00000","00000","00000","01110","00000","00000","00000"],
':':["00000","01100","01100","00000","01100","01100","00000"],
'/':["00001","00010","00010","00100","01000","01000","10000"],
'!':["00100","00100","00100","00100","00100","00000","00100"],
'?':["01110","10001","00001","00110","00100","00000","00100"],
'%':["11001","11010","00010","00100","01000","01011","10011"],
'+':["00000","00100","00100","01110","00100","00100","00000"],
'&':["01100","10010","10100","01000","10101","10010","01101"],
'(':["00010","00100","01000","01000","01000","00100","00010"],
')':["01000","00100","00010","00010","00010","00100","01000"],
'$':["00100","01111","10100","01110","00101","11110","00100"],
}
def text_w(s,scale): return len(s)*(5*scale+scale)
def draw_text(x,y,s,scale,c):
    cx=x
    for ch in s.upper():
        g=FONT.get(ch,FONT['?'])
        for row in range(7):
            for col in range(5):
                if g[row][col]=='1':
                    rect(cx+col*scale,y+row*scale,scale,scale,c)
        cx+=6*scale
    return cx
def wrap(s,chars):
    words=s.split(); lines=[]; cur=""
    for wd in words:
        t=(cur+" "+wd).strip()
        if len(t)<=chars: cur=t
        else: lines.append(cur); cur=wd
    if cur: lines.append(cur)
    return lines
def draw_wrapped(x,y,s,chars,scale,c,lh=None):
    lh=lh or (8*scale+2)
    for i,ln in enumerate(wrap(s,chars)): draw_text(x,y+i*lh,ln,scale,c)
    return len(wrap(s,chars))
def centered(y,s,scale,c):
    draw_text((W-text_w(s,scale))//2,y,s,scale,c)

# ---- PNG writer ----
def write_png(path):
    raw=bytearray()
    for yy in range(H):
        raw.append(0); raw.extend(pix[yy*W*3:(yy+1)*W*3])
    comp=zlib.compress(bytes(raw),9)
    def chunk(typ,data):
        out=struct.pack(">I",len(data))+typ+data
        out+=struct.pack(">I",zlib.crc32(typ+data)&0xffffffff); return out
    png=b"\x89PNG\r\n\x1a\n"
    png+=chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,2,0,0,0))
    png+=chunk(b"IDAT",comp); png+=chunk(b"IEND",b"")
    with open(path,"wb") as f: f.write(png)

# ---- pictorial scenes (x,y,w,h are panel inner box) ----
def badge(x,y,n):
    circle(x+11,y+11,11,RED); 
    s=str(n); draw_text(x+11-text_w(s,1)//2,y+7,s,1,WHITE)
def scene(n,x,y,w,h):
    rect(x,y,w,h,SKY if n not in (5,8) else NAVY if n==5 else (200,220,235))
    if n==1: # missiles + jets over Poland
        rect(x,y+h-18,w,18,GREEN)
        line(x+10,y+h-18,x+w-10,y+h-18,WHITE,2)
        for mx in (x+28,x+62):
            line(mx,y+42,mx+16,y+14,RED,4); tri(mx+20,y+6,14,ORANGE)
        for jx in (x+w-58,x+w-30):
            rect(jx,y+18,22,6,DARK); tri(jx+24,y+16,10,DARK)
        rect(x+w-34,y+h-34,20,12,WHITE); rect(x+w-34,y+h-34,20,6,RED)
        rect(x+8,y+h-34,20,12,BLUE); rect(x+8,y+h-28,20,3,YELLOW)
    elif n==2: # falling markets
        rect(x,y,w,h,WHITE)
        pts=[(x+8,y+14),(x+38,y+26),(x+66,y+22),(x+94,y+46),(x+w-14,y+62)]
        for a,b in zip(pts,pts[1:]): line(a[0],a[1],b[0],b[1],RED,3)
        tri(x+w-20,y+58,16,RED,down=True)
        rect(x+14,y+h-28,34,22,NAVY); rect(x+20,y+h-22,22,4,CYAN); rect(x+20,y+h-14,22,4,GREEN)
    elif n==3: # tanker in strait
        rect(x,y,w,h,(170,215,235)); rect(x,y,26,h,SAND); rect(x+w-26,y,26,h,SAND)
        rect(x+w//2-34,y+h//2,68,12,BROWN); rect(x+w//2-8,y+h//2-12,18,12,DARK)
        circle(x+w//2+18,y+h//2-6,10,ORANGE); circle(x+w//2+22,y+h//2-10,7,RED)
    elif n==4: # game record
        rect(x,y,w,h,PURPLE); rect(x+8,y+h-16,w-16,16,NAVY)
        rect(x+w//2-28,y+22,56,22,DARK); circle(x+w//2-14,y+33,5,RED); circle(x+w//2+14,y+33,5,BLUE)
        rect(x+12,y+10,10,18,YELLOW); rect(x+w-22,y+10,10,18,GREEN); rect(x+18,y+52,16,8,YELLOW)
    elif n==5: # rocket night
        for sx,sy in [(20,8),(52,14),(90,6),(120,16)]: set_px(x+sx,y+sy,WHITE); set_px(x+sx+1,y+sy,WHITE)
        rect(x+w//2-7,y+10,14,20,WHITE); tri(x+w//2-1,y+1,14,RED)
        tri(x+w//2-1,y+30,12,ORANGE); rect(x+10,y+h-8,34,6,GREY); rect(x+w-44,y+h-8,34,6,GREY)
    elif n==6: # Mercury probe
        circle(x+26,y+24,18,YELLOW); circle(x+w-42,y+38,15,ORANGE)
        line(x+52,y+40,x+w-58,y+36,WHITE,3); rect(x+w//2-6,y+28,12,10,CYAN)
    elif n==7: # Kenya oil rig
        rect(x,y,w,h,(250,225,170)); rect(x,y+h-14,w,14,SAND)
        line(x+w//2,y+8,x+w//2,y+h-14,DARK,4); line(x+w//2,y+8,x+w//2-26,y+h-14,DARK,3); line(x+w//2,y+8,x+w//2+26,y+h-14,DARK,3)
        rect(x+w//2-3,y+20,28,5,DARK); circle(x+w-24,y+16,11,YELLOW)
    elif n==8: # cyclone
        for r in (16,12,8,4):
            circle(x+w//2,y+h//2,r,WHITE,fill=False)
        circle(x+w//2,y+h//2,3,BLUE); rect(x+8,y+h-12,28,8,GREEN); rect(x+w-36,y+6,22,8,BROWN)
    elif n==9: # Peru quake
        rect(x,y,w,h,(190,220,240))
        for off in (0,10,20):
            for xx in range(x+6,x+w-6):
                yy=y+14+off-abs((xx-x)%44-22)//3; set_px(xx,yy,BROWN); set_px(xx,yy+1,BROWN)
        for rr in (4,8,12): circle(x+w//2,y+h-6,rr,RED,fill=False)
        rect(x+12,y+h-14,14,8,BROWN); rect(x+w-28,y+h-14,14,8,BROWN)
    elif n==10: # EU for Ukraine
        rect(x,y,w,h,BLUE)
        for a in range(8):
            import math; cx=int(x+w//2+22*math.cos(a*0.785)); cy=int(y+26+16*math.sin(a*0.785)); circle(cx,cy,3,YELLOW)
        rect(x+12,y+h-24,26,14,DARK); rect(x+52,y+h-24,26,14,BROWN); draw_text(x+w-44,y+h-22,"1B",2,YELLOW)
    elif n==11: # Estonia border bridge
        rect(x,y,w,h,(190,220,240)); rect(x,y+h-10,w,10,TEAL)
        line(x+6,y+h-12,x+w-6,y+h-12,DARK,3)
        for bx in range(x+16,x+w-10,18): rect(bx,y+14,4,16,GREY)
        rect(x+34,y+4,18,9,BLUE); rect(x+w-28,y+4,18,9,WHITE); rect(x+w-28,y+8,18,3,RED)
    elif n==12: # Florida floods
        rect(x,y,w,h,(160,200,225)); rect(x,y+h//2,w,h//2,BLUE)
        rect(x+14,y+h//2-18,26,18,WHITE); rect(x+w-44,y+h//2-14,26,14,SAND)
        rect(x+w//2-14,y+h-24,28,8,RED); line(x+16,y+10,x+16,y+22,GREY,2); line(x+34,y+8,x+34,y+20,GREY,2)
    elif n==13: # Gen Z protests
        rect(x,y,w,h,(240,235,210))
        for i,cx in enumerate(range(x+28,x+w-8,16)):
            circle(cx,y+20,4,DARK); rect(cx-4,y+25,9,11,[RED,BLUE,GREEN,ORANGE,PURPLE][i%5])
            rect(cx+3,y+6,13,8,WHITE)
    badge(x+2,y+2,n)

PANELS=[
 (1,"MISSILES FALL ON POLAND NATO SCRAMBLES JETS","ISW AL JAZEERA AP"),
 (2,"AI STOCK ROUT DRAGS WORLD MARKETS DOWN","REUTERS AP S AND P -3.7 PCT"),
 (3,"TANKER HIT IN STRAIT OF HORMUZ","REUTERS ARAB NEWS"),
 (4,"GTA VI $3.79BN FIRST DAY SALES RECORD","REUTERS CNN"),
 (5,"SPACEX LAUNCHES SPACE FORCE MISSION","SPACEFLIGHT NOW"),
 (6,"BEPICOLOMBO NEARS MERCURY","ESA USA TODAY"),
 (7,"KENYA STARTS COMMERCIAL OIL DRILLING","KENYANS TUKIO"),
 (8,"CYCLONE XAVIER RELIEF TO COOK ISLANDS","RNZ PACIFIC"),
 (9,"M6.7 EARTHQUAKE STRIKES PERUVIAN ANDES","AFP USGS NO DEATHS"),
 (10,"EU 1BN EUROS MORE FOR UKRAINE ARMS","COUNCIL OF EU"),
 (11,"ESTONIA TO CLOSE RUSSIA BORDER CROSSINGS","AL JAZEERA"),
 (12,"RECORD FLORIDA FLOODS SWELL RIVER","FLORIDA TODAY NWS"),
 (13,"GEN Z PROTESTS IN 25 EUROPEAN COUNTRIES","CNN AFP"),
]
INDEX=[
 "UK EU AGREE FOOD TRADE YOUTH DEAL - REUTERS",
 "SAUDI COALITION STRIKES HODEIDAH PORT - REUTERS",
 "TBILISI MOURNING AFTER GAS BLAST - AP",
 "PRICE FIRST UNDISPUTED WELSH CHAMPION - REUTERS",
 "COP31 DRAFT DROPS FOSSIL FUELS - REUTERS",
 "DE VILLEPIN LAUNCHES 2027 FRENCH BID - REUTERS",
 "UKRAINE DRONES HIT RUSSIAN PLANT - KYIV IND",
 "S KOREA RULING PARTY IMPEACHMENT PLAN - YONHAP",
 "NEPAL PM FIRST INDIA VISIT NOV 22 - HINDU",
 "JAPAN CORE INFLATION HITS 2026 HIGH - CNBC",
 "SAUDI JAPAN EXPAND OIL STOCKPILE - NHK",
 "XI HAILS TURNAROUND IN AUSTRALIA TIES - REUTERS",
 "ISRAELI STRIKES KILL SIX IN GAZA - AFP",
 "IRAQI FORCES ENTER MILITIA STRONGHOLD - AJ",
 "FUNERAL BOAT CAPSIZES IN NIGERIA - REUTERS",
 "ARGENTINA COUNTRY RISK TOPS 1000 - HERALD",
 "GOLD FOR BIGGEST WEEKLY FALL SINCE MAR - BLOOMBERG",
 "BAYER $7.25BN ROUNDUP DEAL APPROVED - REUTERS",
 "MAN CONVICTED OVER PALISADES FIRE - REUTERS",
 "19 YEARS IN SIKH ASSASSINATION PLOT - REUTERS",
 "SALVADORAN SOLDIERS KILLED IN HAITI - REUTERS",
 "EU FAST TRACKS GRID RENEWABLES - ENERDATA",
 "UKRAINE CHILD CASUALTIES 4 YEAR HIGH - UNICEF",
 "CONGRESS SWEEPS RAJASTHAN RURAL POLLS - HINDU",
 "WHO UPDATES BUNDIBUGYO EBOLA OUTBREAK - WHO",
 "PTSD LEAVES MOLECULAR MARKS ON BRAIN - CELL",
 "SPACE RADIATION REWIRES BRAIN CELLS - SCI REP",
 "TAYLOR SWIFT ARTIST AWARD IN INDIA - WION",
 "MOROCCO ITALY RIOT AT U17 WORLD CUP - FIFA",
 "VERSTAPPEN POLE IN VEGAS QUALIFYING - F1",
 "HARDEN 51 PASSES KOBE IN 50PT GAMES - NBA",
 "UNADKAT HAT TRICK IN INDIA T20 DAY - HINDU",
 "M5.6 QUAKE NEAR LOYALTY ISLANDS - USGS",
]

def panel(x,y,w,h,n,title,src,tscale=1):
    frame(x,y,w,h,BLACK,2); scene(n,x+3,y+3,w-6,38)
    draw_wrapped(x+6,y+46,title, 40, tscale, BLACK)
    draw_text(x+6,y+h-11,src,1,GREY)

def build():
    rect(0,0,W,H,WHITE)
    # masthead
    rect(0,0,W,118,WHITE); rect(0,112,W,4,BLACK); rect(0,6,W,2,BLACK)
    centered(14,"THE WORLD DAILY",5,BLACK)
    centered(58,"20 NOVEMBER 2026",4,RED)
    centered(96,"FRIDAY  WORLD NEWS IN ONE PAGE  46 STORIES",1,DARK)
    # top story: left large panel
    frame(10,124,620,238,BLACK,3)
    scene(1,14,128,612,118)
    draw_wrapped(20,254,"1. MISSILES FALL ON POLAND NATO SCRAMBLES JETS",34,3,BLACK)
    draw_text(20,332,"RUSSIAN STRIKE WAVE SPILLS OVER BORDER  ISW / AL JAZEERA / AP",1,DARK)
    # world map box right of top story
    frame(640,124,374,238,BLACK,3); rect(644,128,366,120,(215,232,245))
    draw_text(652,132,"WORLD MAP  MARKERS 1-13",2,BLACK)
    # simplified continents as blocks
    rect(660,168,70,34,GREEN); rect(682,204,28,30,GREEN)   # Americas
    rect(760,166,52,28,GREEN); rect(778,196,30,36,GREEN)   # Europe/Africa
    rect(828,164,92,36,GREEN); rect(856,202,44,22,GREEN)   # Asia
    rect(922,206,44,22,GREEN)                              # Oceania
    spots={1:(800,168),2:(690,176),3:(822,186),4:(678,188),5:(668,172),6:(792,172),7:(800,204),8:(950,216),9:(688,214),10:(786,170),11:(806,164),12:(682,192),13:(776,174)}
    for n,(mx,my) in spots.items():
        circle(mx,my,8,RED); s=str(n); draw_text(mx-text_w(s,1)//2,my-3,s,1,WHITE)
    draw_wrapped(652,256,"POLAND TOP STORY. MARKETS, HORMUZ, GTA VI, SPACEX, MERCURY, KENYA OIL, CYCLONE, PERU QUAKE, EU AID, ESTONIA, FLORIDA, PROTESTS.",52,1,DARK)
    draw_text(652,338,"EVERY PANEL NUMBER MATCHES THE MAP",1,BLACK)
    # 12 panels: 4 columns x 3 rows
    pw,ph,gap=246,118,6; x0,y0=10,372
    for idx in range(12):
        n=idx+2; col=idx%4; row=idx//4
        x=x0+col*(pw+gap); y=y0+row*(ph+gap)
        t,s=PANELS[idx+1][1],PANELS[idx+1][2]
        panel(x,y,pw,ph,n,f"{n}. {t}",s,1)
    # headline index
    iy=372+3*ph+2*gap+6
    rect(10,iy,1004,28,BLACK); draw_text(18,iy+8,"MORE HEADLINES  33 STORIES  20 NOV 2026",2,WHITE)
    iy+=34
    colw=502
    for i,ln in enumerate(INDEX):
        col=0 if i<17 else 1; row=i if i<17 else i-17
        x=14+col*colw; y=iy+row*13
        draw_text(x,y,f"{i+14}.",1,RED); draw_text(x+26,y,ln,1,BLACK)
    fy=iy+17*13+6
    rect(10,fy,1004,2,BLACK)
    draw_text(14,fy+6,"SOURCES AS CREDITED. ALL STORIES REPORTED 20 NOVEMBER 2026.",1,DARK)
    outdir=os.environ.get("MAKEFUN_OUTPUT_DIR","/output")
    os.makedirs(outdir,exist_ok=True)
    write_png(os.path.join(outdir,"entry.png"))

if __name__=="__main__":
    build()
