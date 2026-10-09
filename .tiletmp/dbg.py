import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = svg2rlg('noi_fine.svg')
if abs(d.width - 144) > 1:
    d.scale(144.0 / d.width)
    d.width = d.height = 144
buf = io.BytesIO()
renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
buf.seek(0)
g = Image.open(buf).convert('L').point(lambda v: 255 - v)
px = g.load()
print('tile size', g.size)
for y in (0, 1, 2, 3, 141, 142, 143):
    row = [px[x, y] for x in range(144)]
    ink = [x for x, v in enumerate(row) if v > 30]
    print('row %3d: ink_cols=%d  first10=%s sum=%d' % (y, len(ink), ink[:10], sum(row)))
# compare profile row143 vs row0 shifted: where do they disagree?
r0 = [px[x, 0] for x in range(144)]
r143 = [px[x, 143] for x in range(144)]
r142 = [px[x, 142] for x in range(144)]
diff0143 = sum(abs(r0[x] - r143[x]) for x in range(144)) / 144.0
diff0142 = sum(abs(r0[x] - r142[x]) for x in range(144)) / 144.0
diff_143_142 = sum(abs(r143[x] - r142[x]) for x in range(144)) / 144.0
print('mean|row0-row143|=%.1f  mean|row0-row142|=%.1f  mean|row143-row142|=%.1f' % (diff0143, diff0142, diff_143_142))
# print profiles compactly
def prof(r):
    return ''.join('#' if v > 120 else ('+' if v > 40 else ('.' if v > 8 else ' ')) for v in r)
print('row0  |' + prof(r0) + '|')
print('row143|' + prof(r143) + '|')
print('row142|' + prof(r142) + '|')
print('row1  |' + prof([px[x,1] for x in range(144)]) + '|')
