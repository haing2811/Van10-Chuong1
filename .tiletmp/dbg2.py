import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))

d = svg2rlg('noi_fine.svg')
s = 144.0 / d.width
d.width = d.height = 144
d.scale(s, s)
buf = io.BytesIO()
renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
buf.seek(0)
g = Image.open(buf).convert('L').point(lambda v: 255 - v)
px = g.load()

def prof(y):
    return ''.join('#' if px[x, y] > 120 else ('+' if px[x, y] > 40 else ('.' if px[x, y] > 8 else ' ')) for x in range(144))

for y in (0, 1, 2, 3, 141, 142, 143):
    row = [px[x, y] for x in range(144)]
    print('row %3d ink=%2d sum=%5d' % (y, sum(1 for v in row if v > 30), sum(row)))
print('row0  |' + prof(0) + '|')
print('row1  |' + prof(1) + '|')
print('row143|' + prof(143) + '|')
print('row142|' + prof(142) + '|')
# interior reference: rows 50/51 around zigrow(51) top
print('row50 |' + prof(50) + '|')
print('row51 |' + prof(51) + '|')
print('row52 |' + prof(52) + '|')
# per-column diff stats
def meandiff(y1, y2):
    return sum(abs(px[x, y1] - px[x, y2]) for x in range(144)) / 144.0
print('mean|row143-row0| =', meandiff(143, 0))
print('mean|row51-row50| =', meandiff(51, 50))
print('mean|row52-row51| =', meandiff(52, 51))
print('mean|row51-row49| =', meandiff(51, 49))
