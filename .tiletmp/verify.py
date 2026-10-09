import io, os, math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def alpha_tile(name, size):
    d = svg2rlg(name + '.svg')
    buf = io.BytesIO()
    renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
    buf.seek(0)
    g = Image.open(buf).convert('L')
    if g.size != (size, size):
        g = g.resize((size, size))
    return g.point(lambda v: 255 - v)  # ink alpha

def colsum(a, x0, x1):
    w, h = a.size
    px = a.load()
    return sum(px[x, y] for x in range(x0, x1) for y in range(h)) // 255

def rowsum(a, y0, y1):
    w, h = a.size
    px = a.load()
    return sum(px[x, y] for y in range(y0, y1) for x in range(w)) // 255

print('== edge seam ink (crossing elements appear on BOTH edges) ==')
for name, size in [('doc_fine',144),('viet_fine',144),('noi_fine',144),
                   ('doc_mega',640),('viet_mega',640),('noi_mega',640)]:
    a = alpha_tile(name, size)
    L, R = colsum(a, 0, 3), colsum(a, size-3, size)
    T, B = rowsum(a, 0, 3), rowsum(a, size-3, size)
    tot = colsum(a, 0, size)
    print('%-10s total_ink=%-7d  L=%-4d R=%-4d  T=%-4d B=%-4d' % (name, tot, L, R, T, B))

print()
print('== viet_fine: meander coverage per tile half (geo 4x4) ==')
im = Image.open('viet_fine_geo.png').convert('L')
for ty in range(4):
    for tx in range(4):
        L = R = 0
        for y in range(ty*144, (ty+1)*144):
            for x in range(tx*144, tx*144+72):
                if im.getpixel((x, y)) < 160: L += 1
            for x in range(tx*144+72, (tx+1)*144):
                if im.getpixel((x, y)) < 160: R += 1
        print('tile(%d,%d) L=%d R=%d ratio=%.2f' % (tx, ty, L, R, R/max(L,1)))

print()
print('== spiral center ink: doc_fine curls should hit cell centers ==')
a = alpha_tile('doc_fine', 144)
px = a.load()
for (cx, cy) in [(36,36),(108,36),(108,108),(36,108),(0,72),(144%144,72),(72,0),(72,144%144)]:
    hit = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            x, y = (cx+dx) % 144, (cy+dy) % 144
            if px[x, y] > 40: hit += 1
    print('curl at (%d,%d): ink pixels in 9x9 = %d' % (cx, cy, hit))

print()
print('== mega annulus identity ==')
def annulus(name, cx, cy, r0, r1, size=640):
    im = Image.open(name + '_geo.png')  # 2x2
    px = im.load()
    hit = 0
    for th in range(0, 360, 3):
        rr = math.radians(th)
        for r in range(r0, r1):
            for base_x, base_y in [(0,0),(size,0),(0,size),(size,size)]:
                x = int(base_x + cx + r*math.cos(rr))
                y = int(base_y + cy + r*math.sin(rr))
                if 0 <= x < im.size[0] and 0 <= y < im.size[1] and sum(px[x,y][:3]) < 480:
                    hit += 1
                    break
    return hit
print('doc_mega ring r=98 @ (200,215):', annulus('doc_mega', 200, 215, 94, 102))
print('doc_mega ring r=98 @ (462,438) scaled .86 -> r=84:', annulus('doc_mega', 462, 438, 80, 88))
print('noi_mega ring r=118 @ (210,230):', annulus('noi_mega', 210, 230, 114, 122))

print()
print('== viet_mega: spindle tip pinch (ink width narrows toward ends) ==')
im = Image.open('viet_mega_geo.png').convert('L')
# big swash centered at (322,296) rotated -27; sample perpendicular bands along its axis
cx, cy, ang = 322, 296, -27
ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
for t in (-160, -80, 0, 80, 160):
    hit = 0
    for u in range(-40, 41):   # perpendicular offset
        x = int(cx + t*ca - u*sa); y = int(cy + t*sa + u*ca)
        if 0 <= x < im.size[0] and 0 <= y < im.size[1] and im.getpixel((x,y)) < 170:
            hit += 1
    print('axis t=%+4d: perpendicular ink=%d' % (t, hit))
