# TruncatablePrimes

切り捨て可能な素数をさがす。

切り捨て可能な素数とは、上から順に1桁ずつ削っていっても素数でありつづける数である。

[](https://gyazo.com/f7579232b43d580e0900c4f0b7d5cd17)

https://community.wolfram.com/groups/-/m/t/1569707/


```python
from sympy.ntheory.primetest import isprime
queue = []

def CutOffPrime(n, digits):
    for i in range(1,10):
        x = i*10**digits + n
        if isprime(x):
            queue.append([x, digits+1])

CutOffPrime(0,0)
while len(queue) >0:
    x, d = queue.pop(0)
    print(x,d)
    CutOffPrime(x,d)
```

0を許さない場合、鉛筆に刻んである数が上限のようだ。

10進数以外の数だともっと大きな数になりえるのだろうか。



やってみた。それぞれの進数での、最大の切り捨て可能な素数である。

10進数以上の数はA,B,C,D,E,F,G,...をそれぞれ11、12、13、に読みかえる。

table:切り捨て可能な素数


* base	in decimal number	in n-ary number
3	23	212
4	4091	333323
5	7817	222232
6	4836525320399	14141511414451435
7	817337	6642623
8	14005650767869	313636165537775
9	977306389	2462868287
10	357686312646216567629137	357686312646216567629137
11	2276005673	A68822827
12		471A34A164259BA16B324AB8A32B7817
13	812751503	CC4C8C65
14	559569749583683009212625338471	C6143392CCBB3D11AC22CC5543
15	34068645705927662447286191	6C6C2CE2CEEEA4826E642B
16	1088303707153521644968345559987	DBC7FBA24FE6AEC462ABF63B3
17	13563641583101	6C66CC4CC83
18		AF93E41A586HE75A7HHAAB7HE12FG79992GA7741B3D
19	546207129080421139	CIEG86GCEA2C6H
20		FC777G3CG1FIDI9I31IE5FFB379C7A3F6EFID

4進数と5進数は面白い数字がでてくるね。

14、16進数の場合は10進数よりも数値は大きいが、それぞれの進数での表記での桁数は10進数のほうが大きくなる。



ということで、長い鉛筆を作る場合には18進数がおすすめ。

[python](python.md) [software](software.md) [雑記](雑記.md)

[2019-01-25](2019-01-25.md) [vitroid](vitroid.md).icon][vitroid](vitroid.md).icon.md)





----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/TruncatablePrimes.md)
