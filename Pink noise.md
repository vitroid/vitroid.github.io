---
title: Pink noise
---
ピンクノイズ[Pink noise](/Pink noise)は1/fノイズとも呼ばれます。一般には、パワースペクトルの関数形が[周波数](/周波数)fに対して1/f^^α^^になるようなノイズを広義の[Pink noise](/Pink noise)と総称します。

* α=0の場合、[周波数](/周波数)に関係なくパワースペクトルが一定値となります。これをWhite noiseと呼びます。チューニングのあわないラジオの音に似ています。Whiteの由来は、白色光(すべての可視光波長を含む)から来るようです。耳障りな音です。
* 0<α<2の場合を狭義の[Pink noise](/Pink noise)と呼びます。ジェット機のエンジン音や滝の音に似ています。ピンクノイズの振幅波形はフラクタルな形状になっています。白色雑音に比べて、長波長成分(可視光でいえば赤色成分)が多いことから、このように呼ぶようです。さらに狭義には、α=1の場合のみを指す場合もあるようです。この場合、[周波数](/周波数)が倍になると波のエネルギーが半分(振幅が0.7倍)になります。
* α=2の場合、音の振幅の運動がちょうど一次元のランダムウォーク（ブラウン運動Brownian motion）になります。これをBrown noiseと呼びます。退屈な雑音です。(White-Pinkと来たので、しゃれでBrownと命名したんでしょうね。ブラウン運動のRobert Brownは植物学者で、007シリーズの脇役俳優やキリンシーグラムのお酒と同姓同名です。)


非圧縮aiff形式になっています。iPod等で使用(スピーカーのテストなど)する場合は、lossless圧縮して下さい。参考のためAACフォーマットの圧縮ファイルも置いてありますが、明らかに音がちがいます。



* [α=0, While noise (aiff format)](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/white.aiff)
* [α=1.0, Pink noise (aiff format)](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/pink1.0.aiff)
* [α=1.3, Pink noise (aiff format)](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/pink1.3.aiff) 
* [α=1.6, Pink noise (aiff format)](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/pink1.6.aiff) 
* [α=2, Brown noise (aiff format)](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/brown.aiff)
* [C source](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/sound.c)
* [Makefile](http://theochem.chem.okayama-u.ac.jp/vitroid/Pink noise/Makefile.sound)


純粋なピンクノイズを作る方法はいろいろあります。ここでは、1/f型のパワースペクトルの各[周波数](/周波数)にランダムな位相を与え、それを逆フーリエ変換して波形を得ています。



純粋なホワイトノイズを実際に耳にすることはあまりないと思います。乱流が生みだす自然の雑音源がおしなべて1/f型であるということもありますが、空気中を音が伝搬する際に高[周波数](/周波数)のほうが速く減衰してしまうため、音源がホワイトでも耳に届くまでにマイルドになっているのかもしれません

* [http://www.yamaha.co.jp/acoust/technologies/scale-model/basic2.html](http://www.yamaha.co.jp/acoust/technologies/scale-model/basic2.html)


### 関連ネタ

* [Sierpinski noise](/Sierpinski noise)
* [Cantor noise](/Cantor noise)
* [Water noise](/Water noise)
* [七五調フラクタル](/七五調フラクタル)
----

* 44100kHz/16bitで出力するようにソースを変更しました。 - [matto](/matto) 
* Brown noiseはブラウン運動から名付けられたので、色とは関係がないです。色と関係のある別名として、Red noiseがあります。ちなみに、[Pink noise](/Pink noise)のPinkや、Red noiseのRedなどの名前は、光からきているそうです。 - 名無しさん 
* 情報ありがとうございます。Brown noiseはpink noiseの中でも特に低波数成分が強いので、red noiseと呼ぶみたいですね。 - [matto](/matto) 
<!--  -->






## Linked from

* [Pink noise](/Pink noise)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Pink noise.md)

