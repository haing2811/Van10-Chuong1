import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def rows_of(img):
    px = img.load()
    out = []
    for y in (0, 1, 2, 3, 141, 142, 143):
        if y >= img.size[1]:
            continue
        row = [px[x, y] for x in range(img.size[0])]
        out.append((y, sum(1 for v in row if v > 30), sum(row)))
    return out

# path A: scale only when mismatched (render.py style)
d = svg2rlg('noi_fine.svg')
print('d.width =', d.width, 'd.height =', d.height)
s = 144.0 / d.width
d.width = d.height = 144
d.scale(s, s)
buf = io.BytesIO()
renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
buf.seek(0)
a = Image.open(buf).convert('L').point(lambda v: 255 - v)
print('pathA size', a.size, rows_of(a))

# path B: fresh drawing, scale only
d2 = svg2rlg('noi_fine.svg')
d2.scale(144.0 / d2.width)
buf = io.BytesIO()
renderPM.drawToFile(d2, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
buf.seek(0)
b = Image.open(buf).convert('L').point(lambda v: 255 - v)
print('pathB size', b.size, rows_of(b))

# path C: no scale at all
d3 = svg2rlg('noi_fine.svg')
buf = io.BytesIO()
renderPM.drawToFile(d3, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
buf.seek(0)
c = Image.open(buf).convert('L').point(lambda v: 255 - v)
print('pathC size', c.size, rows_of(c) if c.size[0] >= 144 else 'too small', 'ink rows summary:')
px = c.split()[3].load()
for y in range(0, c.size[1]):
    row = [px[x, y] for x in range(c.size[0])]
    ink = sum(1 for v in row if v > 30)
    if y < 6 or y > c.size[1] - 7:
        print('   C row %3d ink=%d' % (y, ink))
