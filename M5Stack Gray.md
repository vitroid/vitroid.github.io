---
title: M5Stack Gray
---
# [M5Stack Gray](/M5Stack Gray)

M5StickVの問題がまったく解決しないので、とりあえず放置することにし、[M5Stack Gray](/M5Stack Gray)を手に入れた。ゆくゆくは回転式スイッチ(本体の向きによって操作するリモコンスイッチにする予定。

巷では、M5Stackの[開発環境](/開発環境)はM5UI.Flowに移行しつつあるようなので、version 1.3.2を入れてみたものの、GrayのGyroをどうやって読み取るのかがわからないので、当面はArduinoのFirmwareを入れて使うしかないかな、と思いきや、 [http://www.openspc2.org/reibun/M5/UI-Flow/1.2.3/](http://www.openspc2.org/reibun/M5/UI-Flow/1.2.3/)さんのところで、角度の検出方法も説明されていた。ありがとう!

## 手順

それぞれさらっと1行で書いているが、けっこうわけわからなくてはまる。とにかく、Arduino的に操作するためのfirmwareとか、micropythonで操作するためのfirmwareとか、UI.Flow用のファームウェアとかが素人には判別できないので、firmwareを自分でダウンロードして、ということは考えず、まずBurnerを本家から手にいれるべき。

1. [M5Stack Gray](/M5Stack Gray)をUSBでMacに接続
	* かってに電源が入り、何かが実行され、音がでる。かなり迷惑。
2. M5 Burner for Macをダウンロードして実行
   * 参考 [https://m5stack.com/pages/download](https://m5stack.com/pages/download)
3. その中で、UIFlow-1.3.2をダウンロード(けっこう時間かかる)
	* 出先で作業していたので、回線が遅いのか、アプリがhaltしているのか判別できずやきもきする。	
4. Burnボタンを押してfirmwareを書き込み。(USBtoUARTはすでにインストールされているものとする)
5. M5StackをCボタンを押しながら再起動し、手近のWifiネットワークに接続。
   * ボタンを押さないで起動すると、デモの無限ループに入ってしまう。
   * パソコンから、M5Stack自身が作るローカルWifiに接続し、ウェブ上でWifiアクセスポイントのSSIDとパスワードを入力する。
      * この時、SSIDに空白が入っていると空白が勝手に"+"におきかえられて正常に接続できない。
      * その場合には、以下のURLを直接たたく。SSIDの部分には、接続したいネットワークのSSID、ただし空白は'%20'と記述する。
         * http://192.168.4.1/configure?ssid=SSID&password=パスワード
      * 正常に接続できれば、M5Stackの画面にはAPI keyとQRコード、画面右上に緑のドットが表示される。
6. Mac側では、[http://flow.m5stack.com](http://flow.m5stack.com) にアクセス。IDEが表示される。
7. M5Stack側に表示された[API](/API) keyをMacのIDEに入力し、M5Stackと接続。
   * この接続が不安定でなかなか思うようにいかない。
8. てきとうにコードを組んで、IDE上で実行ボタン(右上の三角)を押すと、M5上で実行される。
   * Block programmingは自動的にMicroPythonに翻訳される。これはありがたい。
9. 最後にUploadボタン(画面左下のアイコン列の一番右)を押すとM5のフラッシュに書きこまれ、リセット後もそれが実行されるようになる。
10. プログラムを書換える場合は、一旦リセットし、setupに入ってwifiにつなぎなおす。

一旦準備がととのえば、8〜10を往復するだけでどんどんプログラムを改良していけるので楽。また、[Obniz](/Obniz)と比べると、Flashとバッテリーをもっているおかげで、オフラインでも使えるし電源なしでも使えるのがありがたい。

## [Obniz](/Obniz)との比較

* UI.FlowのIDEは、[Obniz](/Obniz)のIDEのようにCloud化されてはいない。すなわち、[API](/API) Keyを入力すれば、どこからでも現在のプログラムが表示され、編集できる、というわけではなく、自分でコードを保管する必要がある。
* [Obniz](/Obniz)だと、二人で同時プログラムすることさえできてしまうが、UI.Flowのほうは逆に、2つのIDEが同じ[API](/API) Keyを指定していると、片方しかアクセスできない(もう片方はロックアウトされる)ので、うかつにコードを編集したまま離席して、喫茶店でコーディングしようとした時にはまる?
* 反面、一旦書き込んでしまえば、実行時にはネットにつながっている必要がない。[Obniz](/Obniz)だと、クラウドに常時接続でないと使えない。(書き込む、という操作自体がない)

## [感想](/感想)

* Wifi APを切り替えるのに、いちいちPCで設定する必要があるのか?起動時メニューでAPのリストは表示されるが、指定できるわけではなさそう。
* 開発はCloud経由でもいいのだが、実行時には外のネットワークとつながっていない、ローカルネット上で動かしたい、という場合。Flashに書きこむ瞬間はグローバルネットにつながっていなければいけないのだが、書きこんだあとで、APだけ切り替える方法がわからない。
* なぜかM5からサーバ(flow.m5stack.com)につながらない場合が多く、その間開発が中断するのが最大のストレス。今開発しているコードに関しては、MicroPythonは使えそうにないのでArduino IDEに戻る。

## とりあえずコーディング

デバイスの角度にあわせて画像を動かしたかったのだが、gyroの値は角度ではなくどうも角加速度のようなので、よっぽど精密に積分しないと角度を得ることは難しそうだ。重力加速度の方向もつかって補正すればなんとかなるかもしれないが、いまはとりあえず重力の方向だけでも表示してみよう。

```python
from m5stack import *
from m5ui import *
from uiflow import *
import imu

setScreenColor(0x111111)

imu0 = imu.IMU()

import math

w,h = lcd.screensize()

while True:
  lcd.clear()
  x,y,z = imu0.acceleration
  r = (x*x + y*y + z*z)**0.5
  x /= r
  y /= r
  z /= r
  cx = w/2
  cy = h/2
  R = 20*math.exp(-z/2)
  LR = R*5
  L = LR-R
  if z > 0:
    lcd.circle(int(cx-x*LR),int(cy+y*LR),int(R),fillcolor=0xff0000)
  lcd.line(int(cx), int(cy), int(cx-x*L), int(cy+y*L), 0xffffff)
  if z < 0:
    lcd.circle(int(cx-x*LR),int(cy+y*LR),int(R),fillcolor=0x0000ff)
  wait_ms(2)
```
コードは[github](https://github.com/vitroid/M5Stack)に置きます。

これを改良し、重しをゴムにしたもの。

```python
from m5stack import *
from m5ui import *
from uiflow import *
import imu

setScreenColor(0x111111)

imu0 = imu.IMU()

import math

w,h = lcd.screensize()
cx = w//2
cy = h//2

def draw(x,y,z,r):
  scale = math.exp(-z/200)
  r = int(r*scale)
  x = int(x*scale)
  y = int(y*scale)
  if z > 0:
    lcd.circle(cx-x, cy+y, r, fillcolor=0xff0000)
  lcd.line(cx, cy, cx-x, cy+y, 0xffffff)
  if z < 0:
    lcd.circle(cx-x, cy+y, r, fillcolor=0x0000ff)
  

x,y,z = 0,10,0
vx,vy,vz = 0,0,0
eL = 100
# k / m
km = 0.01
dump = 0.01
import utime
last = utime.ticks_ms()

while True:
  now = utime.ticks_ms()
  dt = (now - last)/10
  last = now
  
  ax,ay,az = imu0.acceleration
  L = (x**2+y**2+z**2)**0.5
  ax -= vx*dump
  ay -= vy*dump
  az -= vz*dump
  if L > eL:
    F = -km*(L-eL) / L
    ax += x*F
    ay += y*F
    az += z*F
  vx += ax*dt
  vy += ay*dt
  vz += az*dt
  x += vx*dt
  y += vy*dt
  z += vz*dt
  lcd.clear()
  draw(x,y,z,20)
  wait_ms(2)
```

もうちょっとがんばって、Attitude indicator (航空機の姿勢表示器)を作ってみた。

```python
from m5stack import *
from m5ui import *
from uiflow import *
import imu

setScreenColor(0x111111)

sevenseg = [0b1110111, 0b0010010, 0b1011101, 0b1011011, 0b0111010, 0b1101011,0b0101111,0b1010010,0b1111111,0b1111010]

imu0 = imu.IMU()

def letter(L,x,y,dx,dy,c):
  if L & 0b1000000:
    lcd.line(x+dy,y-dx,x+dx+dy,y+dy-dx,c)
  if L & 0b0100000:
    lcd.line(x,y,x+dy,y-dx,c)
  if L & 0b0010000:
    lcd.line(x+dx+dy,y+dy-dx,x+dx,y+dy,c)
  if L & 0b0001000:
    lcd.line(x,y,x+dx,y+dy,c)
  if L & 0b0000100:
    lcd.line(x,y,x-dy,y+dx,c)
  if L & 0b0000010:
    lcd.line(x+dx,y+dy,x+dx-dy,y+dy+dx,c)
  if L & 0b0000001:
    lcd.line(x-dy,y+dx,x+dx-dy,y+dy+dx,c)
    
def number(v,x,y,dx,dy,c):
  x0, y0 = x,y
  for L in str(v):
    letter(sevenseg[int(L)], x0,y0,dx,dy,c)
    x0 += dx*3//2
    y0 += dy
    
import math

w,h = lcd.screensize()
cx, cy = w//2, h//2
hist = []
sx, sy, sz = 0,0,0
while True:
  x,y,z = imu0.acceleration
  hist.append((x,y,z))
  sx, sy, sz = sx+x, sy+y, sz+z
  if len(hist)>3:
    x,y,z = hist.pop(0)
    sx, sy, sz = sx-x, sy-y, sz-z
  # bank = math.atan(x,y)
  # average
  x,y,z = sx/3, sy/3, sz/3
  br = (x**2+y**2)**0.5
  bx = int(x/br*100)
  by = int(y/br*100)
  ba = math.atan2(x,y)
  pitch = math.atan2(z,y)*180/3.14
  r = h/2 - 20
  L = 10
  lcd.clear()
  for a,l in ((-60,2),(-45,1),(-30,2),(-20,1),(-10,1),(0,2),(10,1),(20,1),(30,2),(45,1),(60,2)):
    aa = ba + a*3.14/180
    c,s = math.cos(aa),math.sin(aa)
    l = l*L+r
    lcd.line(cx+int(r*s),cy-int(r*c),cx+int(l*s), cy-int(l*c), 0x008000)
  lcd.line(cx-100,cy,cx-20,cy,0x808080)
  lcd.line(cx+20,cy,cx+100,cy,0x808080)
  lcd.line(cx,20,cx+10,40,0x808080)
  lcd.line(cx,20,cx-10,40,0x808080)
  
  lcd.line(cx-by*2,cy-bx*2,cx+by*2,cy+bx*2,0x008000)
  for i in range(-3,4):
    px = int(x/br*(pitch+i*10)*3)
    py = int(y/br*(pitch+i*10)*3)
    scale = abs(i) + 1
    lcd.line(cx-by*scale//6+px,cy-bx*scale//6-py,cx+by*scale//6+px,cy+bx*scale//6-py,0x008000)
    number(abs(i*10), cx+by*(scale+1)//6+px, cy+bx*(scale+1)//6-py, by//12, bx//12, 0x008000)
    number(abs(i*10), cx-by*(scale+2)//6+px, cy-bx*(scale+2)//6-py, by//12, bx//12, 0x008000)
  wait_ms(1)
```

## Arduino

MicroPythonで幸せになれるかと思ったが、やはり遅い。特に、グラフィックスライブラリの遅さをごまかしきれない(バッファーに描けないので)。

以下のサイトの説明に従いfirmwareとlibraryをインストール。

* [https://docs.m5stack.com/#/ja/quick_start/m5core/m5stack_core_get_started_Arduino_MacOS](https://docs.m5stack.com/#/ja/quick_start/m5core/m5stack_core_get_started_Arduino_MacOS)

...

画面がちらちらするのは、Spriteを使ってダブルバッファーに作画すればいいことがわかった。

いろいろ苦労した結果、一応姿勢表示器らしいものが作れた。

![](https://i.gyazo.com/9686054845975ac83b1459cb4494ee55.jpg)

コードは[こちら](https://github.com/vitroid/M5Stack/tree/master/Gray/AttitudeIndicatorArd)。


[M5Stack](/M5Stack)
[2019夏の自由研究](/2019夏の自由研究)
[IoT](/IoT)
[雑記](/雑記)


## Linked from

* [M5Stack Gray](/M5Stack Gray)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/M5Stack Gray.md)

