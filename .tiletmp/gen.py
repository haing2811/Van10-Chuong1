import math, re, os

def star(n, r1, r2):
    pts = []
    for i in range(n * 2):
        a = math.radians(i * (360 / (n * 2)) - 90)
        r = r1 if i % 2 == 0 else r2
        pts.append('%.1f %.1f' % (r * math.cos(a), r * math.sin(a)))
    return 'M' + 'L'.join(pts) + 'Z'

def rays(n, r0, r1, jit):
    segs = []
    for k in range(n):
        a = math.radians(k * (360 / n) - 90)
        rr = r1 + jit[k % len(jit)]
        segs.append('M%.1f %.1fL%.1f %.1f' % (r0 * math.cos(a), r0 * math.sin(a), rr * math.cos(a), rr * math.sin(a)))
    return ''.join(segs)

def spiral(r0, r1, turns, start_deg=135.0, step_deg=18.0, tail=None):
    import math
    n = max(4, int(360 * turns / step_deg))
    pts = []
    for i in range(n + 1):
        th = math.radians(start_deg + i * step_deg)
        r = r0 + (r1 - r0) * i / n
        pts.append((r * math.cos(th), r * math.sin(th)))
    d = 'M%.1f %.1f' % pts[0] + ''.join('L%.1f %.1f' % p for p in pts[1:])
    if tail:
        d = tail + d
    return d

def filt(w, h):
    return ('<filter id="r" filterUnits="userSpaceOnUse" x="0" y="0" width="%d" height="%d">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" stitchTiles="stitch" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="1.3" xChannelSelector="R" yChannelSelector="G"/>'
            '</filter>') % (w, h)

# ---------- DOC FINE 144 ----------
curls = ''
for (x, y, rot, op) in [(36, 36, 0, .9), (108, 36, 90, .8), (108, 108, 180, .88), (36, 108, -90, .75),
                        (0, 72, 0, .8), (144, 72, 0, .82), (72, 0, 90, .86), (72, 144, 90, .78)]:
    curls += '<use href="#k" opacity="%.2f" transform="translate(%d %d) rotate(%d)"/>' % (op, x, y, rot)
d1 = ''.join('M0 %dL144 %d' % (c, c + 144) for c in range(-144, 109, 36))
d2 = ''.join('M0 %dL144 %d' % (c, c - 144) for c in range(0, 289, 36))
doc_fine_body = ('<path stroke-width="1.1" stroke-opacity=".42" d="%s"/>'
                 '<path stroke-width="1" stroke-opacity=".36" d="%s"/>%s') % (d1, d2, curls)
DEFS_DOC_FINE = ('<path id="k" stroke-width="1.2" stroke-opacity=".62" d="'
                 + spiral(9, 1.6, 1.8, tail='M-15 10C-11 11-8 9-6.4 6.4') + '"/>')

# ---------- DOC MEGA 640 ----------
DEFS_DOC_MEGA = ('<path id="k2" stroke-width="2.6" stroke-opacity=".62" d="'
  + spiral(15, 2.5, 1.9, step_deg=17, tail='M-30 19C-22 21-15 18-10.6 10.6') + '"/>'
  '<path id="p" stroke-width="2" stroke-opacity=".6" d="M0-9c6-9 4-21 0-27-4 6-6 18 0 27"/>'
  '<g id="m">'
  '<circle r="98" stroke-width="3" stroke-opacity=".5"/>'
  '<circle r="86" stroke-width="2" stroke-opacity=".52"/>'
  + ''.join('<use href="#k2" transform="rotate(%d) translate(-13 -68)"/>' % a for a in (0, 90, 180, 270))
  + '<circle r="44" stroke-width="2.4" stroke-opacity=".55"/>'
  + ''.join('<use href="#p" transform="rotate(%d)"/>' % (k * 45) for k in range(8))
  + '<circle r="7" stroke-width="2" stroke-opacity=".5"/><circle r="2.5" fill="black" fill-opacity=".45"/>'
  + '</g>')
doc_mega_body = ('<use href="#m" transform="translate(200 215) rotate(12) scale(1.04)"/>'
  '<use href="#m" transform="translate(462 438) rotate(-22) scale(.86)"/>'
  '<use href="#p" opacity=".9" transform="translate(468 148) scale(1.9) rotate(30)"/>'
  '<use href="#p" opacity=".85" transform="translate(128 520) scale(1.6) rotate(-60)"/>'
  '<path stroke-width="2.4" stroke-opacity=".55" d="M96 372c14-16 40-14 50 2 8 14-4 30-22 28-14-2-20-16-12-26"/>'
  '<path stroke-width="2.4" stroke-opacity=".52" d="M486 268c-12-14-34-12-42 2-7 12 3 26 19 24 12-2 17-14 10-22"/>')

# ---------- VIET FINE 144 ----------
rows = []
variants = [(6, 30, 6, 24, 15, 24), (6, 30, 7, 23, 16, 25), (5.5, 30, 6.5, 24.5, 14.5, 23.5), (6.5, 29.5, 5.5, 23.5, 15.5, 24.5)]
def unit(x1, x2, top, bot, hook, b, y0, o, mirror):
    m = (lambda x: 36 - x) if mirror else (lambda x: x)
    return 'M%g %gV%gH%gV%gH%gV%gH%g' % (
        m(x1) + o, b, y0 + top, m(x2) + o, y0 + bot,
        m(x1 + 12) + o, y0 + hook, m(x1 + 18) + o)
for k in range(4):
    y0 = 36 * k
    b = y0 + 30
    x1, x2, top, bot, hook, hy = variants[k]
    rows.append('<path stroke-width="1.4" stroke-opacity=".5" d="M0 %gH144"/>' % b)
    off = 18 if k % 2 else 0          # odd rows shift half a cell for hand-laid stagger
    for j in range(4):
        o = off + 36 * j
        mir = ((j + k) % 2 == 1)
        op = 0.44 + 0.03 * (k % 2) + 0.02 * (j % 2)
        offs = [o]
        if o + 30 > 144:   # cell straddles right edge -> also draw wrapped at left
            offs.append(o - 144)
        if o + 6 < 0:      # (never with off>=0, kept for clarity)
            offs.append(o + 144)
        for oo in offs:
            d = unit(x1, x2, top, bot, hook, b, y0, oo, mir)
            rows.append('<path stroke-width="1.3" stroke-opacity="%.2f" d="%s"/>' % (op, d))
viet_fine_body = (''.join(rows)
  + '<path stroke-width="1.2" stroke-opacity=".36" stroke-dasharray="18 7 9 14" d="M0 3H144"/>'
  + '<path stroke-width="1.1" stroke-opacity=".35" stroke-dasharray="11 13 19 5" d="M0 141H144"/>')

# ---------- VIET MEGA 640 ----------
# spindle envelope: center bristle longest, y-offsets pinch toward both ends
brs = ''
bristles = [(-17, 130, 3.1, .62), (-11, 168, 2.9, .52), (-5.5, 186, 3.2, .7),
            (0, 192, 3.0, .74), (6, 180, 2.9, .58), (12, 158, 3.1, .52), (18, 124, 3.0, .5)]
for dy, L, sw, op in bristles:
    d = 'M%.0f %.1fC%.0f %.1f %.0f %.1f %.0f %.1f' % (
        -L, dy * .3, -L * .38, dy * 1.08, L * .34, dy * 1.0, L, dy * .22)
    brs += '<path stroke-width="%.1f" stroke-opacity="%.2f" d="%s"/>' % (sw, op, d)
brs += ('<path stroke-width="3" stroke-opacity=".5" stroke-dasharray="26 14 44 10" d="M-160-26C-56-38 60-34 152-22"/>'
        '<path stroke-width="2.9" stroke-opacity=".5" stroke-dasharray="18 22 30 16" d="M-104 30C-26 27 52 30 98 37"/>')
DEFS_VIET_MEGA = '<g id="b">' + brs + '</g>'
viet_mega_body = ('<use href="#b" transform="translate(322 296) rotate(-27) scale(1.14)"/>'
  '<use href="#b" transform="translate(438 498) rotate(16) scale(.78)"/>'
  '<use href="#b" transform="translate(146 138) rotate(-44) scale(.7)"/>')

# ---------- NOI FINE 144 ----------
DEFS_NOI_FINE = ('<g id="c">'
  '<circle r="20" stroke-width="1" stroke-opacity=".36"/>'
  '<circle r="13" stroke-width="1.1" stroke-opacity=".44"/>'
  '<circle r="6" stroke-width="1.3" stroke-opacity=".52"/>'
  '<circle r="1.6" fill="black" fill-opacity=".45"/></g>')
ops = [.85, .7, .78, .62, .9, .66, .74, .8, .6]
scales = [1, 0.97, 1.03, 1.02, 0.96, 1.01, 0.98, 1.04, 0.99]
uses = ''
i = 0
for yy in (24, 72, 120):
    for xx in (24, 72, 120):
        uses += '<use href="#c" opacity="%.2f" transform="translate(%d %d) scale(%.2f)"/>' % (ops[i], xx, yy, scales[i])
        i += 1

def zigrow(y):
    d = 'M0 %g' % y
    up = True
    x = 0
    while x < 144:
        d += 'l8 ' + ('-6' if up else '6')
        x += 8
        up = not up
    return '<path stroke-width="1.2" stroke-opacity=".38" d="%s"/>' % d

# zigzag centers at y=0/48/96; the center-0 row straddles the seam, so it is
# drawn twice (3 and 147) to duplicate its clipped half at the opposite edge
noi_fine_body = uses + zigrow(3) + zigrow(51) + zigrow(99) + zigrow(147)

# ---------- NOI MEGA 640 ----------
DEFS_NOI_MEGA = ('<g id="s">'
  '<circle r="118" stroke-width="3.4" stroke-opacity=".52"/>'
  '<path stroke-width="2.4" stroke-opacity=".52" d="' + star(18, 112, 103) + '"/>'
  '<circle r="97" stroke-width="2.2" stroke-opacity=".5"/>'
  '<circle r="64" stroke-width="2.2" stroke-opacity=".5"/>'
  '<path stroke-width="3" stroke-opacity=".55" d="' + rays(16, 34, 58, [0, 3, -2, 4, 0, -3, 2, -4, 1, 3, -2, 0, 4, -1, 2, -3]) + '"/>'
  '<circle r="30" stroke-width="2.6" stroke-opacity=".5"/>'
  '<circle r="16" stroke-width="2" stroke-opacity=".5"/>'
  '<circle r="7" fill="black" fill-opacity=".5"/></g>'
  '<path id="bd" d="M0 0l15-9-3 7 17-5-11 10 11 5-17-1-4 9-4-11-15 4 9-9z"/>')
bird = '<g fill="black" fill-opacity=".5" stroke="none">'
for bx in (126, 196, 266):
    bird += '<use href="#bd" transform="translate(%d 540)"/>' % bx
bird += '</g><path stroke-width="2.2" stroke-opacity=".5" d="M104 560H296"/>'
noi_mega_body = ('<use href="#s" transform="translate(210 230) rotate(6)"/>'
  '<use href="#s" transform="translate(478 452) rotate(-16) scale(.62)"/>' + bird)

tiles = {
    'doc_fine': (144, DEFS_DOC_FINE, doc_fine_body),
    'doc_mega': (640, DEFS_DOC_MEGA, doc_mega_body),
    'viet_fine': (144, '', viet_fine_body),
    'viet_mega': (640, DEFS_VIET_MEGA, viet_mega_body),
    'noi_fine': (144, DEFS_NOI_FINE, noi_fine_body),
    'noi_mega': (640, DEFS_NOI_MEGA, noi_mega_body),
}
bad = re.compile(r'(fill|stroke)="(?!none)[^"]*#[^"]*"|#[0-9a-fA-F]{3}|rgba|<text|<image|<script|xlink|<tspan|style=|stroke:|fill:', re.I)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for name, (sz, defs, body) in tiles.items():
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
         '<defs>%s%s</defs><g filter="url(#r)" fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
         ) % (sz, sz, sz, sz, filt(sz, sz), defs, body)
    probs = []
    if len(s) > 6000:
        probs.append('LEN %d' % len(s))
    m = bad.search(s)
    if m:
        probs.append('BAD:' + m.group(0))
    fine = sz == 144
    lo_w, hi_w = (1.0, 1.6) if fine else (2.0, 4.0)
    lo_o, hi_o = (0.35, 0.7) if fine else (0.5, 0.9)
    for tag in re.findall(r'<(?:path|circle|polyline|line)[^>]*>', s):
        wm = re.search(r'stroke-width="([\d.]+)"', tag)
        if not wm:
            continue
        w = float(wm.group(1))
        if not (lo_w <= w <= hi_w):
            probs.append('SW %g' % w)
        om = re.search(r'stroke-opacity="([\d.]+)"', tag)
        if not om:
            probs.append('NO-SOP')
        else:
            o = float(om.group(1))
            if not (lo_o <= o <= hi_o):
                probs.append('SOP %g' % o)
    print(name, len(s), 'OK' if not probs else probs)
    open(name + '.svg', 'w', encoding='utf-8').write(s)
