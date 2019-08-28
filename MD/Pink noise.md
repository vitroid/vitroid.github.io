#fractal noise



ピンクノイズPink noiseは1/fノイズとも呼ばれます。一般には、パワースペクトルの関数形が周波数fに対して1/f^^α^^になるようなノイズを広義のPink noiseと総称します。



* α=0の場合、周波数に関係なくパワースペクトルが一定値となります。これをWhite noiseと呼びます。チューニングのあわないラジオの音に似ています。Whiteの由来は、白色光(すべての可視光波長を含む)から来るようです。耳障りな音です。
* 0<α<2の場合を狭義のPink noiseと呼びます。ジェット機のエンジン音や滝の音に似ています。ピンクノイズの振幅波形はフラクタルな形状になっています。白色雑音に比べて、長波長成分(可視光でいえば赤色成分)が多いことから、このように呼ぶようです。さらに狭義には、α=1の場合のみを指す場合もあるようです。この場合、周波数が倍になると波のエネルギーが半分(振幅が0.7倍)になります。
* α=2の場合、音の振幅の運動がちょうど一次元のランダムウォーク（ブラウン運動Brownian motion）になります。これをBrown noiseと呼びます。退屈な雑音です。(White-Pinkと来たので、しゃれでBrownと命名したんでしょうね。ブラウン運動のRobert Brownは植物学者で、007シリーズの脇役俳優やキリンシーグラムのお酒と同姓同名です。)


非圧縮aiff形式になっています。iPod等で使用(スピーカーのテストなど)する場合は、lossless圧縮して下さい。参考のためAACフォーマットの圧縮ファイルも置いてありますが、明らかに音がちがいます。



* [](white.aiff) α=0, While noise (aiff format) / ([](white.m4a) AAC 128kbps)
* [](pink1.0.aiff) α=1.0, Pink noise (aiff format) / ([](pink1.0.m4a) AAC 128kbps)
* [](pink1.3.aiff) α=1.3, Pink noise (aiff format)
* [](pink1.6.aiff) α=1.6, Pink noise (aiff format)
* [](brown.aiff) α=2, Brown noise (aiff format) / ([](brown.m4a) AAC 128kbps)
* [](sound.c) C source.
* [](Makefile.sound) Makefile.


純粋なピンクノイズを作る方法はいろいろあります。ここでは、1/f型のパワースペクトルの各周波数にランダムな位相を与え、それを逆フーリエ変換して波形を得ています。



純粋なホワイトノイズを実際に耳にすることはあまりないと思います。乱流が生みだす自然の雑音源がおしなべて1/f型であるということもありますが、空気中を音が伝搬する際に高周波数のほうが速く減衰してしまうため、音源がホワイトでも耳に届くまでにマイルドになっているのかもしれません*http://www.yamaha.co.jp/acoust/technologies/scale-model/basic2.html


### 関連ネタ

* Sierpinski noise
* Cantor noise
* Water noise
* 七五調フラクタル
----

* 44100kHz/16bitで出力するようにソースを変更しました。 - matto 
* Brown noiseはブラウン運動から名付けられたので、色とは関係がないです。色と関係のある別名として、Red noiseがあります。ちなみに、Pink noiseのPinkや、Red noiseのRedなどの名前は、光からきているそうです。 - 名無しさん 
* 情報ありがとうございます。Brown noiseはpink noiseの中でも特に低波数成分が強いので、red noiseと呼ぶみたいですね。 - matto 
<!--  -->




