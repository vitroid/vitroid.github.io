import svgwrite as sw
from math import *
import numpy as np


def rotmat(x,y,z):
    """
    3Dプリンタ用の造形言語やソフトウェアでよくある、x,y,zの順の回転を実現する。
    ただし、角度はラジアン。
    行列を横ベクトルの後ろから掛ける記法を採用しているので、行列の順はz,y,xとなる。
    """
    Rz = np.array([[cos(z), -sin(z), 0.0],
                   [sin(z), cos(z), 0.0],
                   [0,      0,      1.0]])
    Rx = np.array([[1,      0,      0],
                   [0.0, cos(x), -sin(x)],
                   [0.0, sin(x), cos(x)]])
    Ry = np.array([[cos(y), 0.0, sin(y)],
                   [0,      1,      0],
                   [-sin(y), 0.0, cos(y)]])
    return np.dot(Rx, np.dot(Ry, Rz))


def depth(a,c):
    """
    簡易なパースペクティブ変換
    """
    zoom = exp(a[2]/c)
    return np.array([a[0]*zoom,a[1]*zoom,a[2]])


def draw_poly(svg, vs, **attr):
    """
    SVG直打ちでポリゴンを描く
    """
    group = svg.add( svg.g( id="test" ) )
    p = []
    p.append(["M", vs[0][0], vs[0][1]])
    for v in vs[1:]:
        p.append(["L", v[0], v[1]])
    p.append(["Z"])
    path = sw.path.Path(d=p, **attr)
    group.add(path)


class Prim():
    """
    ポリゴンなどのPrimitiveのクラス。
    verticesは並進も回転も行わない。(最後にまとめて実施)
    """
    def __init__(self, typ, center, vertices=None, **kwargs):
        self.typ = typ
        self.center = center
        self.attr = kwargs
        self.vertices = vertices
        self.rotmat = np.identity(3)
    def rotate(self, x,y,z):
        R = rotmat(x,y,z)
        self.rotmat = np.dot(self.rotmat, R)
        self.center = np.dot(self.center, R)
    def translate(self, X):
        self.center += X
    def draw_svg(self, svg, d, offset=(0,0), zoom=1):
        if self.typ == "p":
            vs = []
            for v in prim.vertices:
                v = np.dot(v, prim.rotmat)
                v += prim.center
                v = depth(v, d)
                v *= zoom
                v += np.array([offset[0], offset[1], 0.0])
                vs.append(v)
            draw_poly(svg, vs, **self.attr)
        elif self.typ == "@":
            v = depth(prim.center, d)
            v *= zoom
            v += np.array([offset[0], offset[1], 0.0])
            svg.add(sw.shapes.Ellipse(center=v[:2], r=[6,6], **self.attr))




def hextube(r,n,m, **kwargs):
    """
    六角形でおおわれたチューブを描く。
    r: 半径
    n: 周上の六角形の数(チューブの太さ)
    m: 長手方向の六角形の数(チューブの太さ)
    """
    l = r*sin(pi/n)/sqrt(3.0)*2
    hexagons = []
    for ix in range(m):
        for ith in range(n):
            c = r*cos(2*pi*ith/n)
            s = r*sin(2*pi*ith/n)
            ch = r*cos(pi*(2*ith+1)/n)
            sh = r*sin(pi*(2*ith+1)/n)
            c1 = r*cos(pi*(2*ith+2)/n)
            s1 = r*sin(pi*(2*ith+2)/n)
            c1h = r*cos(pi*(2*ith+3)/n)
            s1h = r*sin(pi*(2*ith+3)/n)
            hexagon = np.array([
                (l*(ix*3), c, s),
                (l*(ix*3+1), c, s),
                (l*(ix*3+1.5), ch, sh),
                (l*(ix*3+1), c1, s1),
                (l*(ix*3), c1, s1),
                (l*(ix*3-0.5), ch, sh),])
            com = np.sum(hexagon, axis=0) / hexagon.shape[0]
            hexagon -= com
            hexagons.append(Prim("p", center=com, vertices=hexagon, **kwargs))
            hexagon = np.array([
                (l*(ix*3+1.5), ch, sh),
                (l*(ix*3+2.5), ch, sh),
                (l*(ix*3+3.0), c1, s1),
                (l*(ix*3+2.5), c1h, s1h),
                (l*(ix*3+1.5), c1h, s1h),
                (l*(ix*3+1.0), c1, s1),])
            com = np.sum(hexagon, axis=0) / hexagon.shape[0]
            hexagon -= com
            hexagons.append(Prim("p", center=com, vertices=hexagon, **kwargs))
    return hexagons

def squaretube(r,n,m, **kwargs):
    l = 2*r*sin(pi/n)
    squares = []
    for ix in range(m):
        for ith in range(n):
            c = r*cos(2*pi*ith/n)
            s = r*sin(2*pi*ith/n)
            c1 = r*cos(pi*(2*ith+2)/n)
            s1 = r*sin(pi*(2*ith+2)/n)
            square = np.array([
                (l*(ix), c, s),
                (l*(ix+1), c, s),
                (l*(ix+1), c1, s1),
                (l*(ix), c1, s1),])
            com = np.sum(square, axis=0) / square.shape[0]
            square -= com
            squares.append(Prim("p", center=com, vertices=square, **kwargs))
#    for ix in range(m+1):
#        for ith in range(n):
#            c = r*cos(2*pi*ith/n)
#            s = r*sin(2*pi*ith/n)
#            com = np.array((l*(ix), c, s))
#            squares.append(Prim("@", center=com, **kwargs))
    return squares



# ナノチューブの準備
r=12.8/2
n = 16
hexagons = hextube(r,n,9,
                   stroke_width=1, fill="#fff", stroke="#000", fill_opacity=0.7)
r = 2.75
n = 6
squares  = squaretube(r,n,17,
                      stroke_width=2, fill="#fff", stroke="#000", fill_opacity=0.7)

   	# 表示方法
theta = 1.3      #ANGLE
d = 50.0         #PERSPECTIVE
offsx = 100
offsy = 150

# SVGの準備
svg = sw.Drawing()

# すべてのプリミティブを原点中心で回転する
prims = hexagons + squares
for prim in prims:
    prim.rotate(theta, theta, 0)

# 回転したあとで、重心でソートし、遠い順に描く。
for prim in sorted(hexagons + squares, key=lambda x: x.center[2]):
    prim.draw_svg(svg, d, zoom=10, offset=(offsx, offsy))

# 標準出力
print(svg.tostring())
