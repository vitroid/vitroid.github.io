#x,yが直線a→bの右側にあればTrueを返す。
def isright(a, b, x, y):
    dx1 = b[0] - a[0]
    dy1 = b[1] - a[1]
    dx2 = x - a[0]
    dy2 = y - a[1]
    return (dx1*dy2 - dx2*dy1) > 0.0



#周縁上の線分のうち、点x,yを右に望むもの(先頭と末尾)を返す。
def kukan(perimeter,nodes,x,y,start):
    i = start
    head = -1
    tail = -1
    backscan = False
    while True:
        j = i+1
        if j == len(perimeter):
            j = 0
        a = isright(nodes[perimeter[i]], nodes[perimeter[j]], x,y )
        #print i,j,a
        if 0 <= head and not a:
            tail = i
            break
        if head<0 and a:
            head = i
            if i==0:
                backscan = 1
        i = i+1
        if i == len(perimeter):
            i = 0
            if head < 0:
                break
    if head < 0:
        return None
    #print head,tail
    if backscan:
        i = start
        while True:
            j = i-1
            a = isright(nodes[perimeter[j]], nodes[perimeter[i]], x,y )

            if a:
                head = j
            else:
                break
            i -= 1
    return head,tail



#kukanで得られた周縁の区間を取りのぞいて、新たにnewnodeを周縁に追加する。
def arrange( perimeter, head, tail, newnode ):
    i = (head + 1) % len(perimeter)
    while i != tail:
        perimeter[i] = -1
        i = (i+1) % len(perimeter)
    perimeter.insert((head+1)%len(perimeter),newnode)
    #print perimeter
    i = 0
    while i < len(perimeter):
        if perimeter[i] < 0:
            perimeter.pop(i)
        else:
            i += 1
    #print perimeter



#逐次追加法で点を追加する。
def add(perimeter,nodes,x,y):
    newnode = len(nodes)
    nodes.append((x,y))
    result = kukan(perimeter,nodes,x,y,0)
    if result != None:
        i,j = result
        arrange( perimeter, i,j, newnode )


    
#描画
def show(perimeter, nodes):
    fill(0)
    nostroke()
    for i in nodes:
        oval(i[0]-2,i[1]-2,4,4)
    nofill()
    stroke(0)
    for k in range(-1,len(perimeter)-1):
        i = perimeter[k]
        j = perimeter[k+1]
        line(nodes[i][0],nodes[i][1],
             nodes[j][0],nodes[j][1])
        


from math import *

#最初の2点だけはあらかじめ設定しておく。
perimeter = [0,1]
nodes = [(200.0,200.0),(200.0,240.0)]

size(400,400)
speed(30)

#NoteBoxのアニメーション用関数。毎秒30回呼ばれる。
def draw():
    for i in range(100):
        x = random()*400.0  
        y = random()*400.0  
        if ( (x-200)**2 + (y-200)**2 < 200**2 ):
            add(perimeter,nodes,x,y)
    show(perimeter,nodes)
