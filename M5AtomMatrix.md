---
title: M5AtomMatrix
---
# M5Atom Matrix
M5Stack兄弟の一番小さい弟、Atomが届いた。

## 印象

![](https://i.gyazo.com/b1f741840a70eba81a8a2afbd7e07f85.jpg)

* とにかく小さい。幅と高さは[M5Stick](/M5Stick)Cと同じ。
* これまでのM5Stackシリーズと違い、開腹される前提になってない。認証シールがケーシングの上箱と下箱にまたがって貼ってあるし、ネジでなくプラスチックの嵌合になってる。でも開けるのは簡単。
* 5x5 LED面自体が押しボタンになっている。出荷時にインストールされているソフトウェアでは、ボタンを押すとLEDの色が変化する。いままでにない使い心地。
* バッテリなし! でも、底面のピンを使って連結するバッテリモジュールがすぐに出てくるだろう。自分でバッテリケースを作るのも良いかもしれない。
* 磁石がない。姿勢センサーMPU6886は磁気センサーを内蔵してないので、磁石がついてても不都合はないはず(逆に言えば[M5Stack Gray](/M5Stack Gray)に磁石を内蔵してたのは謎)だが。これも自分で接着しちゃえばいいか。
* まだコードは書いていないけど、無線(Wifi/BT)があり、姿勢センサーがあるので、[M5Stick](/M5Stick)Cに近い使い方ができると思う。
* そういやパッケージには本体しか入ってなかった。USB-Cのケーブルは別に調達する必要がある。

## 開発

* Arduino IDE用のライブラリは "M5Atom" という名前だった。つまり、M5Stack Atom Matrixではなく、M5Atom Matrixが正しい名前らしい。
* BoardのTypeは[ESP32](/ESP32) Pico Kitを選択。( [https://www.youtube.com/watch?v=2f4biAfvC_M](https://www.youtube.com/watch?v=2f4biAfvC_M) )
* 通信のビットレートを115200に。
* FastLEDライブラリを読みこむ。
* M5Atom用サンプル "button" をコンパイル。無事に動いた(出荷時の状態に戻った?)
* 同 "MPU6886" をコンパイル。IMUと温度計が動いていることを確認。

## 展望

* バッテリがないので、ケーブルにつなげて使わざるをえないけど、つないでいると向きを自由に変えられない。何かもっと大きくて重いものにはりつけて使うと便利な気がする。

[2020-04-14](/2020-04-14)
[IoT](/IoT)
[M5Stack](/M5Stack)
[M5Atom](/M5Atom)
[AtomMatrix](/AtomMatrix)
----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/M5AtomMatrix.md)

