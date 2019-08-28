


#1つの三角形の表側にnodeがあるかどうかを判定する。
def thisside(tri, nodes, node):
    d1 = [0.0] * 3
    d2 = [0.0] * 3
    d3 = [0.0] * 3
    for i in range(3):
        d1[i] = nodes[tri[1]][i] - nodes[tri[0]][i] 
        d2[i] = nodes[tri[2]][i] - nodes[tri[0]][i] 
        d3[i] = node[i]          - nodes[tri[0]][i]
    d12 = [0.0]*3
    d12[0] = d1[1]*d2[2] - d1[2]*d2[1]
    d12[1] = d1[2]*d2[0] - d1[0]*d2[2]
    d12[2] = d1[0]*d2[1] - d1[1]*d2[0]
    if d12[2]<0.0:
        for i in range(3):
            d12[i] = -d12[i]
    sum = 0.0
    for i in range(3):
        sum += d12[i] * d3[i]
    return sum < 0.0



#すべての三角形の中で、node側を向いているものを列挙する。
def frontfaces(triangles, nodes, node):
    front = []
    for tri in triangles:
        if thisside(tri, nodes, node):
            front.append(tri)
    return front





#点の順序を整える。
def order(x,y):
    if x>y:
        return y,x
    return x,y




#各エッジを共有する三角形のリストを作る。
def edgeowners( triangles ):
    edges = dict()
    #三角形の集合の周縁を求める。
    for i in range(len(triangles)):
        tri = triangles[i]
        #辺AB
        e = order(tri[0],tri[1])
        if not edges.has_key(e):
            edges[e] = []
        edges[e].append(i)
        #辺AC
        e = order(tri[0],tri[2])
        if not edges.has_key(e):
            edges[e] = []
        edges[e].append(i)
        #辺BC
        e = order(tri[1],tri[2])
        if not edges.has_key(e):
            edges[e] = []
        edges[e].append(i)
    return edges

#点を追加する。
def add(triangles, nodes, node):
    label = len(nodes)
    nodes.append(node)
    #表側にnodeが来るような三角形を列挙する。
    front = frontfaces(triangles, nodes, node)
    if len(front):
        edges = edgeowners( front )
        #1回しかカウントされなかった辺が周縁。周縁とnodeで三角形を新設する。
        for edge in edges.keys():
            if len(edges[edge]) == 1:
                triangles.append((edge[0],edge[1],label))
        #frontの三角形は全部抹消する。
        for tri in front:
            triangles.remove(tri)

#1つの三角形の外心を求める。
def circumcenter( triangle, nodes ):
    a = nodes[triangle[0]]
    b = nodes[triangle[1]]
    c = nodes[triangle[2]]
    d = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
    cx = ((a[1]**2+a[0]**2)*(b[1]-c[1])+
          (b[1]**2+b[0]**2)*(c[1]-a[1])+
          (c[1]**2+c[0]**2)*(a[1]-b[1]))/d
    cy = ((a[1]**2+a[0]**2)*(c[0]-b[0])+
          (b[1]**2+b[0]**2)*(a[0]-c[0])+
          (c[1]**2+c[0]**2)*(b[0]-a[0]))/d
    return cx,cy

    
#三角形描画
def show(triangles,nodes):
    stroke(0)
    for tri in triangles:
        #print tri
        for i in range(-1,2):
            line(nodes[tri[i]][0],nodes[tri[i]][1],
                nodes[tri[i+1]][0],nodes[tri[i+1]][1])
    #ついでにvoronoi分割も描く(赤)
    #1つの辺は2つの三角形に共有されている。
    edges = edgeowners( triangles )
    circ  = []
    #各三角形の外心を求めておく。
    for tri in triangles:
        circ.append(circumcenter(tri,nodes))
    #fill(0)
    #for i in range(len(triangles)):
    #    text("%s" % i, circ[i][0],circ[i][1])
    #for i in range(len(nodes)):
    #    text("%s" % i, nodes[i][0],nodes[i][1])
    #print edges
    stroke(color(1,0,0))
    #それぞれの辺について
    for edge in edges.values():
        #2つの三角形に共有されているなら
        if len(edge)==2:
            i,j = edge
            line(circ[i][0],circ[i][1],
                circ[j][0],circ[j][1])
    




#2次元の点を3次元に持ちあげる。
def newnode(x,y):
    return x,y,x**2+y**2



size(400,400)

triangles = [(0,1,2),(0,2,3)]
nodes = []
#処理が面倒なので、最初の点は十分遠くにとっておく。
#あとの点はこの内部におくことにする。
nodes.append( newnode(0.0, 0.0) )
nodes.append( newnode(400.0, 0.0) )
nodes.append( newnode(400.0, 400.0) )
nodes.append( newnode(0.0, 400.0) )


#speed(3)

#NoteBoxのアニメーション用関数。毎秒30回呼ばれる。
def draw():
    for i in range(20):
        x = random()*400.0  
        y = random()*400.0  
        if ( (x-200)**2 + (y-200)**2 < 200**2 ):
            add(triangles,nodes,newnode(x,y))
    show(triangles,nodes)

draw()