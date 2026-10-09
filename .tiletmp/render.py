import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def render_tile(name, size):
    d = svg2rlg(name + '.svg')
    if d is None:
        print('PARSE FAIL', name)
        return None
    if abs(d.width - size) > 1:
        s = size / float(d.width)
        d.width, d.height = size, size
        d.scale(s, s)
    buf = io.BytesIO()
    renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
    buf.seek(0)
    gray = Image.open(buf).convert('L')
    # black shapes on white -> alpha mask
    alpha = gray.point(lambda v: 255 - v)
    im = Image.new('RGBA', gray.size, (0, 0, 0, 255))
    im.putalpha(alpha)
    return im

def tile_canvas(im, cols, rows):
    w, h = im.size
    c = Image.new('RGBA', (w * cols, h * rows), (0, 0, 0, 0))
    for i in range(cols):
        for j in range(rows):
            c.alpha_composite(im, (i * w, j * h))
    return c

def desk(w, h, dark=False):
    top = (26, 21, 13) if dark else (107, 84, 58)
    mid = (20, 16, 10) if dark else (74, 58, 39)
    bot = (12, 10, 6) if dark else (51, 40, 23)
    px = []
    for y in range(h):
        t = y / (h - 1.0)
        if t < 0.55:
            k = t / 0.55
            col = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            col = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
        px.append(col)
    im = Image.new('RGB', (w, h))
    d = ImageDraw = None
    from PIL import ImageDraw as ID
    dr = ID.Draw(im)
    for y, col in enumerate(px):
        dr.line([(0, y), (w, y)], fill=col)
    return im.convert('RGBA')

def insitu(seam, ink_rgb, ink_a, dark, boost=5):
    w, h = seam.size
    bg = desk(w, h, dark)
    a = seam.split()[3]
    if boost != 1:
        a = a.point(lambda v: min(255, v * boost))
    outa = bytes((ma * ink_a) // 255 for ma in a.getdata())
    layer = Image.new('RGBA', (w, h), ink_rgb + (255,))
    layer.putalpha(Image.frombytes('L', (w, h), outa))
    bg.alpha_composite(layer)
    return bg.convert('RGB')

tiles = [('doc_fine', 144), ('viet_fine', 144), ('noi_fine', 144),
         ('doc_mega', 640), ('viet_mega', 640), ('noi_mega', 640)]

for name, size in tiles:
    im = render_tile(name, size)
    if im is None:
        continue
    im.save(name + '_raw.png')
    if size == 144:
        seam = tile_canvas(im, 4, 4)
    else:
        seam = tile_canvas(im, 2, 2)
    geo = Image.new('RGBA', seam.size, (255, 255, 255, 255))
    geo.alpha_composite(seam)
    geo.convert('RGB').save(name + '_geo.png')
    fine = 'fine' in name
    for theme, dark in (('light', False), ('dark', True)):
        if fine:
            ink = (242, 231, 201) if not dark else (200, 171, 99)
            ia = 55 if not dark else 50
        else:
            ink = (233, 216, 176) if not dark else (200, 171, 99)
            ia = 80 if not dark else 75
        insitu(seam, ink, ia, dark, boost=5).save('%s_%s.png' % (name, theme))
    print('ok', name, seam.size)
