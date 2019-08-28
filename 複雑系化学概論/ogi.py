def mygroup(x,group):
    while group[x] >= 0:
        x = group[x]
    return x


def mergegroups(x,y,group):
    xg = mygroup(x,group)
    yg = mygroup(y,group)
    if xg != yg:
        group[yg]   += group[xg]
        group[xg] = yg

group = dict()

coins = []


speed(1000)
size(400,400)
def addone():
    x = random(400)
    y = random(400)
    coins.append((x,y))
    me = len(coins)-1
    group[me] = -1

    for i in range(len(coins)-1):
        dx = coins[i][0] - x
        dy = coins[i][1] - y
        dd = dx**2 + dy**2
        if dd < 10**2:
            mergegroups(me,i,group)


n = 0
#lastsize = 0
def draw():
    global n#,lastsize
    for i in range(10):
        addone()
    n += 10
    maxsize = -1
    maxgroup = 0
    for i in range(len(coins)):
        g = mygroup(i,group)
        if group[g] < maxsize:
            maxsize = group[g]
            maxgroup = g
    #if lastsize != maxsize:
    #    print n,-maxsize
    #lastsize=maxsize
    for i in range(len(coins)):
        x = coins[i][0]
        y = coins[i][1]
        if mygroup(i,group) == maxgroup:
            stroke(0)
            fill(1,0,0)
        else:
            nostroke()
            fill(1,0.8,0)
        oval(x-5,y-5,10,10)
    fill(0)
    nostroke()
    fontsize(40)
    text("%s" % n,20,40)
