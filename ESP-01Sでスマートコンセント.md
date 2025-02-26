---
title: ESP-01Sでスマートコンセント
---
[IoT](/IoT) [ESP](/ESP) [ESP-01S](/ESP-01S)

## デバイス

ESP-01S 用のリレーが余っていたので、ESP-01S 本体とライターのセットをアマゾンで手配 → 翌日到着

- [amzn:08OzKdv](http://amzn.asia/d/08OzKdv)
- [amzn:0DYj7eJ](http://amzn.asia/d/0DYj7eJ)

## コーディング

Mac 上の Arduino IDE で、サンプルコードをちょっと加工して作成。

- [https://github.com/vitroid/IoT/tree/main/Arduino/OpenSmartSocket](https://github.com/vitroid/IoT/tree/main/Arduino/OpenSmartSocket)
- mDNS に対応し、IP がわからなくても同じネットワーク内からなら URL は固定
- URL にアクセスがあると On/Off される。
- その URL を QR コードにする。これで、スマホで QR コードを撮影するとすぐにスイッチが作動する。
- NTP で時刻あわせ、夜 10 時と深夜 2 時に強制電源 OFF

## 電工

- 電源は、使っていない USB 充電器のコードを切って、リレーの 5V 入力に接続。赤が 5V、黒が GND。
- Ikea のプラスチックボックスに物資を仕込む。グルーガンでケースに固定。


## Linked from

* [ESP-01Sでスマートコンセント](/ESP-01Sでスマートコンセント)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/ESP-01Sでスマートコンセント.md)

