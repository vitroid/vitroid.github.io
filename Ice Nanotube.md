# Ice Nanotube

[](https://gyazo.com/d89a80878e507ca0aae1afce8c4e75c8)



[python](python.md) [code](code.md) [NodeBox](NodeBox.md) [nanotube](nanotube.md) [visualization](visualization.md)

シンプルにしたが、頂点に○が書けなくなった。頂点・面・辺の描き順はいい解決策がない。

キラルなナノチューブも自在に描けると便利かな。

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
                       stroke_width=1, fill="[fff",](fff",.md) stroke="[000",](000",.md) fill_opacity=0.7)
    r = 2.75
    n = 6
    squares  = squaretube(r,n,17,
                          stroke_width=2, fill="[fff",](fff",.md) stroke="[000",](000",.md) fill_opacity=0.7)
    
   	# 表示方法 
    theta = 1.3      [ANGLE](ANGLE.md)     d = 50.0         [PERSPECTIVE](PERSPECTIVE.md)     offsx = 100
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

svgwriteを使ってpythonでsvgを出力するように変更。

ポリゴンを3次元座標変換してsvgにする汎用ライブラリが欲しい。

    import svgwrite as sw
    from math import *
    import numpy as np
    
    def hextube(r,n,m):
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
                hexagon = []
                hexagon.append((l*(ix*3), c, s))
                hexagon.append((l*(ix*3+1), c, s))
                hexagon.append((l*(ix*3+1.5), ch, sh))
                hexagon.append((l*(ix*3+1), c1, s1))
                hexagon.append((l*(ix*3), c1, s1))
                hexagon.append((l*(ix*3-0.5), ch, sh))
                hexagons.append(hexagon)
                hexagon = []
                hexagon.append((l*(ix*3+1.5), ch, sh))
                hexagon.append((l*(ix*3+2.5), ch, sh))
                hexagon.append((l*(ix*3+3.0), c1, s1))
                hexagon.append((l*(ix*3+2.5), c1h, s1h))
                hexagon.append((l*(ix*3+1.5), c1h, s1h))
                hexagon.append((l*(ix*3+1.0), c1, s1))
                hexagons.append(hexagon)
        return hexagons
    
    def squaretube(r,n,m):
        l = 2*r*sin(pi/n)
        squares = []
        for ix in range(m):
            for ith in range(n):
                c = r*cos(2*pi*ith/n)
                s = r*sin(2*pi*ith/n)
                c1 = r*cos(pi*(2*ith+2)/n)
                s1 = r*sin(pi*(2*ith+2)/n)
                square = []
                square.append((l*(ix), c, s))
                square.append((l*(ix+1), c, s))
                square.append((l*(ix+1), c1, s1))
                square.append((l*(ix), c1, s1))
                squares.append(square)
        return squares
    
    
    def outprod(a,b):
        return (a[1]*b[2]-a[2]*b[1],
                a[2]*b[0]-a[0]*b[2],
                a[0]*b[1]-a[1]*b[0])
    
    
    def normal(polygon):
        [print](print.md) polygon
        vec = [0.0] * 3
        for i in range(len(polygon)):
            op = outprod(polygon[i-1],polygon[i])
            for i in range(3):
                vec[i] += op[i]
        return vec
    
    
    def rotatey(a,th):
        c = cos(th)
        s = sin(th)
        return (a[0]*c-a[2]*s,a[1],a[0]*s+a[2]*c)
    
    def rotatex(a,th):
        c = cos(th)
        s = sin(th)
        return (a[0], a[1]*c-a[2]*s, a[1]*s+a[2]*c)
    
    def depth(a,c):
        zoom = exp(a[2]/c)
        return (a[0]*zoom,a[1]*zoom,a[2])
    
    
    [pos](pos.md) = []
    [file](file.md) = open("001.q.xyz","r")
    [lin](lin.md) = file.readline()
    [lin](lin.md) = file.readline()
    [for](for.md) lin in file:
    #    elem,x,y,z = lin.split()
    #    if elem == "O":
    #        pos.append((float(x),float(y),float(z)))
    #
    [bonds](bonds.md) = []
    [for](for.md) i in range(len(pos)):
    #    xi,yi,zi = pos[i]
    #    for j in range(i+1,len(pos)):
    #        xj,yj,zj = pos[j]
    #        d = (xi-xj)**2 + (yi-yj)**2 + (zi-zj)**2
    #        if d < 10:
    #            bonds.append((pos[i],pos[j]))
                
    # size(600,300)
    r=12.8/2
    n = 16
    hexagons = hextube(r,n,9)
    r = 2.75
    n = 6
    squares  = squaretube(r,n,17)
    
    theta = 1.3      [ANGLE](ANGLE.md)     d = 50.0         [PARSE](PARSE.md)     offsx = 100
    offsy = 150
    
    [backside](backside.md) hexagons
    fill = (1,1,1,0.7)
    stroke = "[000"](000".md)     stroke_width = 1
    svg = sw.Drawing()
    group = svg.add( svg.g( id="test" ) )
    for hexagon in hexagons:
        projected = []
        for vertex in hexagon:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            p = []
            p.append(["M", projected[0][0]*10+offsx, projected[0][1]*10+offsy])
            for vertex in projected:
                p.append(["L", vertex[0]*10+offsx, vertex[1]*10+offsy])
            p.append(["Z"])
            path = sw.path.Path(d=p, stroke_width=stroke_width, fill="[fff",](fff",.md) stroke=stroke)
            group.add(path)
    [strokewidth(2)](strokewidth(2).md)     [for](for.md) v0,v1 in bonds:
    #    p0 = depth(rotatey(rotatex(v0,theta),theta),d)
    #    p1 = depth(rotatey(rotatex(v1,theta),theta),d)
    #    line(p0[0]*10+offsx, p0[1]*10+offsy,
    #         p1[0]*10+offsx, p1[1]*10+offsy)
    [fill(0)](fill(0).md)     [nostroke()](nostroke().md)     [for](for.md) v0,v1 in bonds:
    #    p0 = depth(rotatey(rotatex(v0,theta),theta),d)
    #    p1 = depth(rotatey(rotatex(v1,theta),theta),d)
    #    oval(p0[0]*10+offsx-4, p0[1]*10+offsy-4,8,8)
    #    oval(p1[0]*10+offsx-4, p1[1]*10+offsy-4,8,8)
    
    
    [backside](backside.md) squares
    fill = 1,1,1,0.7
    stroke = "[000"](000".md)     stroke_width = 2
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            p = []
            p.append(["M", projected[0][0]*10+offsx, projected[0][1]*10+offsy])
            for vertex in projected:
                p.append(["L", vertex[0]*10+offsx, vertex[1]*10+offsy])
            p.append("Z")
            path = sw.path.Path(d=p, stroke_width=stroke_width, fill="[fff",](fff",.md) stroke=stroke, fill_opacity=0.7)
            group.add(path)
            
    [backside](backside.md) atoms
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            for vertex in projected:
                u = sw.shapes.Ellipse(center=(vertex[0]*10+offsx, vertex[1]*10+offsy), r=(3,3),
                                     stroke_width=stroke_width, stroke=stroke, fill="[fff",](fff",.md) fill_opacity=0.7)
                group.add(u)
    
    [frontside](frontside.md) squares
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            p = []
            p.append(["M", projected[0][0]*10+offsx, projected[0][1]*10+offsy])
            for vertex in projected:
                p.append(["L", vertex[0]*10+offsx, vertex[1]*10+offsy])
            p.append("Z")
            path = sw.path.Path(d=p, stroke_width=stroke_width, fill="[fff",](fff",.md) stroke=stroke, fill_opacity=0.7)
            group.add(path)
    
    [frontside](frontside.md) atoms
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            for vertex in projected:
                u = sw.shapes.Ellipse(center=(vertex[0]*10+offsx, vertex[1]*10+offsy), r=(3,3),
                                      stroke_width=stroke_width, stroke=stroke, fill="[fff",](fff",.md)                                       fill_opacity=0.7)
                group.add(u)
    
    [frontside](frontside.md) hexagons
    fill = (1,1,1,0.7)
    stroke = "[000"](000".md)     stroke_width = 1
    for hexagon in hexagons:
        projected = []
        for vertex in hexagon:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            p = []
            p.append(["M", projected[0][0]*10+offsx, projected[0][1]*10+offsy])
            for vertex in projected:
                p.append(["L", vertex[0]*10+offsx, vertex[1]*10+offsy])
            p.append("Z")
            path = sw.path.Path(d=p, stroke_width=stroke_width, fill="[fff",](fff",.md) stroke=stroke, fill_opacity=0.7)
            group.add(path)
    
    print(svg.tostring())
    
    
   [NodeBox]用の古いコード。numpyとSVGで書きなおしたいね。
    def hextube(r,n,m):
        l = r*sin(pi/n)/sqrt(3.0)*2
        print l
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
                hexagon = []
                hexagon.append((l*(ix*3), c, s))
                hexagon.append((l*(ix*3+1), c, s))
                hexagon.append((l*(ix*3+1.5), ch, sh))
                hexagon.append((l*(ix*3+1), c1, s1))
                hexagon.append((l*(ix*3), c1, s1))
                hexagon.append((l*(ix*3-0.5), ch, sh))
                hexagons.append(hexagon)
                hexagon = []
                hexagon.append((l*(ix*3+1.5), ch, sh))
                hexagon.append((l*(ix*3+2.5), ch, sh))
                hexagon.append((l*(ix*3+3.0), c1, s1))
                hexagon.append((l*(ix*3+2.5), c1h, s1h))
                hexagon.append((l*(ix*3+1.5), c1h, s1h))
                hexagon.append((l*(ix*3+1.0), c1, s1))
                hexagons.append(hexagon)
        return hexagons
    
    def squaretube(r,n,m):
        l = 2*r*sin(pi/n)
        print l
        squares = []
        for ix in range(m):
            for ith in range(n):
                c = r*cos(2*pi*ith/n)
                s = r*sin(2*pi*ith/n)
                c1 = r*cos(pi*(2*ith+2)/n)
                s1 = r*sin(pi*(2*ith+2)/n)
                square = []
                square.append((l*(ix), c, s))
                square.append((l*(ix+1), c, s))
                square.append((l*(ix+1), c1, s1))
                square.append((l*(ix), c1, s1))
                squares.append(square)
        return squares
    
    
    def outprod(a,b):
        return (a[1]*b[2]-a[2]*b[1],
                a[2]*b[0]-a[0]*b[2],
                a[0]*b[1]-a[1]*b[0])
    
    
    def normal(polygon):
        [print](print.md) polygon
        vec = [0.0] * 3
        for i in range(len(polygon)):
            op = outprod(polygon[i-1],polygon[i])
            for i in range(3):
                vec[i] += op[i]
        return vec
    
    
    def rotatey(a,th):
        c = cos(th)
        s = sin(th)
        return (a[0]*c-a[2]*s,a[1],a[0]*s+a[2]*c)
    
    def rotatex(a,th):
        c = cos(th)
        s = sin(th)
        return (a[0], a[1]*c-a[2]*s, a[1]*s+a[2]*c)
    
    def depth(a,c):
        zoom = exp(a[2]/c)
        return (a[0]*zoom,a[1]*zoom,a[2])
    
    
    [pos](pos.md) = []
    [file](file.md) = open("001.q.xyz","r")
    [lin](lin.md) = file.readline()
    [lin](lin.md) = file.readline()
    [for](for.md) lin in file:
    #    elem,x,y,z = lin.split()
    #    if elem == "O":
    #        pos.append((float(x),float(y),float(z)))
    #
    [bonds](bonds.md) = []
    [for](for.md) i in range(len(pos)):
    #    xi,yi,zi = pos[i]
    #    for j in range(i+1,len(pos)):
    #        xj,yj,zj = pos[j]
    #        d = (xi-xj)**2 + (yi-yj)**2 + (zi-zj)**2
    #        if d < 10:
    #            bonds.append((pos[i],pos[j]))
                
    size(600,300)
    from math import *
    r=12.8/2
    n = 16
    hexagons = hextube(r,n,9)
    r = 2.75
    n = 6
    squares  = squaretube(r,n,17)
    
    theta = 1.3      [ANGLE](ANGLE.md)     d = 50.0         [PARSE](PARSE.md)     offsx = 100
    offsy = 150
    
    [backside](backside.md) hexagons
    fill(1,1,1,0.7)
    stroke(0)
    strokewidth(1)
    for hexagon in hexagons:
        projected = []
        for vertex in hexagon:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            beginpath(projected[0][0]*10+offsx, projected[0][1]*10+offsy)
            for vertex in projected:
                lineto(vertex[0]*10+offsx, vertex[1]*10+offsy)
            endpath()
    [strokewidth(2)](strokewidth(2).md)     [for](for.md) v0,v1 in bonds:
    #    p0 = depth(rotatey(rotatex(v0,theta),theta),d)
    #    p1 = depth(rotatey(rotatex(v1,theta),theta),d)
    #    line(p0[0]*10+offsx, p0[1]*10+offsy,
    #         p1[0]*10+offsx, p1[1]*10+offsy)
    [fill(0)](fill(0).md)     [nostroke()](nostroke().md)     [for](for.md) v0,v1 in bonds:
    #    p0 = depth(rotatey(rotatex(v0,theta),theta),d)
    #    p1 = depth(rotatey(rotatex(v1,theta),theta),d)
    #    oval(p0[0]*10+offsx-4, p0[1]*10+offsy-4,8,8)
    #    oval(p1[0]*10+offsx-4, p1[1]*10+offsy-4,8,8)
    
    
    [backside](backside.md) squares
    fill(1,1,1,0.7)
    stroke(0)
    strokewidth(2)
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            beginpath(projected[0][0]*10+offsx, projected[0][1]*10+offsy)
            for vertex in projected:
                lineto(vertex[0]*10+offsx, vertex[1]*10+offsy)
            endpath()
    [backside](backside.md) atoms
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] > 0:
            for vertex in projected:
                oval(vertex[0]*10+offsx-3, vertex[1]*10+offsy-3,6,6)
    [frontside](frontside.md) squares
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            beginpath(projected[0][0]*10+offsx, projected[0][1]*10+offsy)
            for vertex in projected:
                lineto(vertex[0]*10+offsx, vertex[1]*10+offsy)
            endpath()
    [frontside](frontside.md) atoms
    for square in squares:
        projected = []
        for vertex in square:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            for vertex in projected:
                oval(vertex[0]*10+offsx-3, vertex[1]*10+offsy-3,6,6)
    
    [frontside](frontside.md) hexagons
    fill(1,1,1,0.7)
    stroke(0)
    strokewidth(1)
    for hexagon in hexagons:
        projected = []
        for vertex in hexagon:
            projected.append(depth(rotatey(rotatex(vertex,theta),theta),d))
        n = normal(projected)
        if n[2] < 0:
            beginpath(projected[0][0]*10+offsx, projected[0][1]*10+offsy)
            for vertex in projected:
                lineto(vertex[0]*10+offsx, vertex[1]*10+offsy)
            endpath()
    



----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Ice Nanotube.md)
