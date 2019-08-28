---
title: Sierpinski noise
---
[fractal](/fractal) noise



シェルピンスキーSierpinskiのオートマトンの各世代の1のビットの数を音にしたものです。



シェルピンスキーガスケットSierpinski Gasketは一次元セルオートマトンの一種で、以下のようなルールで作られます。

```
x(n+1, i) = x(n, i) xor x(n,i-1)
```
ただし、nは世代、iは座標です。このルールにより、以下のようなパターンが形成されます。

```
 10000000
 11000000
 10100000
 11110000
 10001000
 11001100
 10101010
 11111111
```
各世代の"1"の数は1,2,2,4,2,4,4,8...という風に徐々に増加します。これを直接音圧に変換します。



* [](sierpinski.aiff) Sierpinski Noise.
* [](sierpinski.c) C source.
* [](Makefile.sierpinski) Makefile.




## Linked from

* [Pink noise](/Pink noise)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Sierpinski noise.md)

