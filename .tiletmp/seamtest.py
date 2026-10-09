import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def alpha_tile(name, size):
    d = svg2rlg(name + '.svg')
    if abs(d.width - size) > 1:
        s = size / float(d.width)
        d.width, d.height = size, size
        d.scale(s, s)
    buf = io.BytesIO()
    renderPM.drawToFile(d, buf, fmt='PNG', bg=0xFFFFFF, alpha=1)
    buf.seek(0)
    g = Image.open(buf).convert('L')
    if g.size != (size, size):
        g = g.resize((size, size))
    return g.point(lambda v: 255 - v)

print('Seam test: diff ACROSS the seam vs CONTENT-MATCHED interior adjacent-pair diffs.')
print('(seam pair compared only with interior pairs of similar ink level; ratio near 1 = join as smooth as same-zone interior)')
for name, size in [('doc_fine',144),('viet_fine',144),('noi_fine',144),
                   ('doc_mega',640),('viet_mega',640),('noi_mega',640)]:
    a = alpha_tile(name, size)
    W = size * 3
    big = Image.new('L', (W, W), 0)
    for i in range(3):
        for j in range(3):
            big.paste(a, (i * size, j * size))
    bp = big.load()
    W = size * 3
    # interior adjacent-pair stats: (diff, mean ink of the two lines)
    def colpair(x):
        d = 0.0
        ink = 0.0
        for y in range(W):
            va, vb = bp[x-1, y], bp[x, y]
            d += abs(va - vb)
            ink += va + vb
        return d / float(W), ink / (2.0 * W)
    def rowpair(y):
        d = 0.0
        ink = 0.0
        for x in range(W):
            va, vb = bp[x, y-1], bp[x, y]
            d += abs(va - vb)
            ink += va + vb
        return d / float(W), ink / (2.0 * W)
    inner_c = [colpair(x) for x in range(1, W) if x % size != 0]
    inner_r = [rowpair(y) for y in range(1, W) if y % size != 0]
    def report(label, seams, inner):
        for si, (sd, sink) in enumerate(seams):
            matches = [d for d, ink in inner if abs(ink - sink) <= max(0.35 * sink, 2.0)]
            if not matches:
                matches = sorted(inner, key=lambda t: abs(t[1] - sink))[:max(8, len(inner)//20)]
                matches = [d for d, _ in matches]
            med = sorted(matches)[len(matches) // 2]
            print('  %s seam#%d diff=%6.2f ink=%5.2f | matched interior n=%d median=%6.2f ratio=x%.2f'
                  % (label, si, sd, sink, len(matches), med, sd / max(med, .01)))
    seam_c = [colpair(k * size) for k in (1, 2)]
    seam_r = [rowpair(k * size) for k in (1, 2)]
    print(name)
    report('vert', seam_c, inner_c)
    report('horz', seam_r, inner_r)
