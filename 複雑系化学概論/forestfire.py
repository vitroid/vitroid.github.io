import random

random.seed(1234)
size(400,400)
colormode(HSB)
green = color(0.33, 0.8, 0.5)
brown = color(0.1,0.35,0.7)
red = color(1,1,1)
black = color(0,0,0)
speed(10)

class Map:
    #
    #mapの初期値を設定する。
    #森林火災の場合: xは木の密度。
    #
    def __init__(self,size,density):
        self.size = size
        self.density = density
        self.m = [[]] * size
        for x in range(0,size):
            self.m[x] = [0] * size
            for y in range(0,size):
                r = random.random()
                #print x,y,r
                if r < density:
                    self.m[x][y] = 1
                else:
                    self.m[x][y] = 0

    #現状を表示する。
    def draw(self):
        size = self.size
        radius = WIDTH / size
        for x in range(0,size):
            for y in range(0,size):
                if self.m[x][y] == 0:
                    fill(brown)
                elif self.m[x][y] == 1:
                    fill(green)
                elif self.m[x][y] == 2:
                    fill(red)
                elif self.m[x][y] == 3:
                    fill(black)
                #print map[x][y],
                oval(x*radius,y*radius,radius,radius)
        fill(black)
        text(str(self.density), 10,HEIGHT-10)
    
    #次のステップを計算する。
    def next(self):
        size = self.size
        newm = [[]] * size
        changed = False
        for x in range(-1,size-1):
            newm[x] = [0] * size
            for y in range(-1,size-1):
                #地面(0)または焼け跡(3)は変化しない。
                if self.m[x][y] == 0 or self.m[x][y] == 3:
                    newm[x][y] = self.m[x][y]
                elif self.m[x][y] == 1:
                    if self.m[x-1][y] == 2 or self.m[x+1][y] == 2 or self.m[x][y-1] == 2 or self.m[x][y+1] == 2:
                        newm[x][y] = 2
                        changed = True
                    else:
                        newm[x][y] = 1
                elif self.m[x][y] == 2:
                    newm[x][y] = 3
                    changed = True
        self.m = newm
        return changed
        
    def ignite(self):
        changed = False
        if mousedown:
            size = self.size
            x = int(MOUSEX / WIDTH * size)
            y = int(MOUSEY / WIDTH * size)
            if x<size and y<size:
                if self.m[x][y]==1:
                    self.m[x][y] = 2
                    changed = True
        return changed

    def autoignite(self):
        changed = False
        while not changed:
            size = self.size
            x = int(random.random() * size)
            y = int(random.random() * size)
            if self.m[x][y]==1:
                self.m[x][y] = 2
                changed = True
        return changed


def setup():
    global map
    map = Map( 100, 0.59 )
    map.autoignite()

def draw():
    global map
    if map.next():
    #map.ignite()
        map.draw()




