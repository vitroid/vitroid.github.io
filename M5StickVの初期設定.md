---
title: M5StickVの初期設定
---
# [M5StickVの初期設定](/M5StickVの初期設定)

M5StickVはM5Stackの小型版([M5Stick](/M5Stick))の、さらにAIエンジン搭載のもの、らしい。情報がなく、いろいろ苦労する。


## 2019-11-19更新

ひさびさに情報収集。10/22版のFirmwareがでているようなので、書きこんでみる。

Firmwareは[こちら](https://docs.m5stack.com/#/en/quick_start/m5stickv/m5stickv_quick_start).

書き込みには[kflash](https://github.com/kendryte/kflash.py)を使う。

    kflash -p /dev/cu.usbserial-000033 -b 1500000 M5StickV_Firmware_1022_beta.kfpkg 

今回は、CPUの種類も自動で検知したようだ。ビットレートは1500000にしないと遅くて待たされる。

```
(base) vitroid-black-9:GoogleDrive matto$ sudo cu -l /dev/cu.usbserial-000033 -s 115200
Connected.

[MAIXPY]Pll0:freq:832000000
[MAIXPY]Pll1:freq:398666666
[MAIXPY]Pll2:freq:45066666
[MAIXPY]cpu:freq:416000000
[MAIXPY]kpu:freq:398666666
[MAIXPY]Flash:0xc8:0x17
open second core...
gc heap=0x80215060-0x80295060
[MaixPy] init end

 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

M5StickV by M5Stack : https://m5stack.com/
M5StickV Wiki       : https://docs.m5stack.com
Co-op by Sipeed     : https://www.sipeed.com

[MAIXPY]: result = 0
[MAIXPY]: numchannels = 1
[MAIXPY]: samplerate = 44100
[MAIXPY]: byterate = 88200
[MAIXPY]: blockalign = 2
[MAIXPY]: bitspersample = 16
[MAIXPY]: datasize = 158760
init i2c2
[MAIXPY]: find ov7740
MicroPython v0.4.0-52-g3b8c18b84-dirty on 2019-10-21; M5Stick-V with Kendryte K210
Type "help()" for more information.
>>> 
>>> 
```

MicroPythonが0.4.0になっているね。

さて、何しようか。MaixPyはいまだにPythonに対応していないみたいなので、uPyLoaderで書くしかない。

[https://qiita.com/mayfair/items/d1a4ad360670c61ba0fa](https://qiita.com/mayfair/items/d1a4ad360670c61ba0fa) を参考に。相変らず、接続には瞬発力を要する。

SDからの起動にはまだ成功していない。

### 以下は古い内容になってしまいました。

## Firmwareの書き込み

小林先生の [https://qiita.com/mayfair/items/d1a4ad360670c61ba0fa](https://qiita.com/mayfair/items/d1a4ad360670c61ba0fa) ほかいろいろ参考にするもKflash-gui 1.5.2が動かず、古いバージョン1.2は書き込みに成功しない。




* pip install kflushでCUIツールをインストール
* [M5Stack Quick Start](https://docs.m5stack.com/#/en/quick_start/m5stickv/m5stickv_quick_start)からfirmwareを入手。
* 電源を落とし、一旦コネクタを抜いたあと、正面のAボタンを押しながらコネクタを差し込んでboot.pyの自動起動を回避。
* 以下のcommandで書き込んだ。
        kflash -B M5StickV  -p /dev/cu.usbserial-B55A3DF445 -b 115200 ~/Downloads/m5stickV_Firmware_0630Fixed.kfpkg 
       -Bには機種名を入れるのだが、M5StickVがどれに該当するのかわからず、適当に書いたら自動認識(goE/kd233)してくれた。

* Serial TerminalからのHello worldの実行は問題なかったが、MaiXPy IDEからのコードの書きこみはまだうまくいかない。もしかして、IDEで書いたあと、一旦セーブして、あらためて転送しないといけない?
* uPyLoaderの意義もよくわからない。MaiXPy IDEのtransferは機能しないのだが、uPyLoaderを一旦実行して、__upload.pyが生成したら問題は解決する、のか? 
* とりあえず書いてある通りにやってみる。uPyLoaderをダウンロードし、実行。M5StickVにはじめから書きこまれているファイルをMacに落として中身を見てようやく理解。boot.pyが起動時に実行されているようだ。つまり、これを書きかえてやれば、何でもできる、と。
* 処理の様子を見る限り、MicroPythonでもそれなりの速度が出ている。また、kpuを利用したければ、MicroPythonを使わざるをえないのだろう。とりあえずIDEは当分使わない予定。



さくっと試しに実行するだけなら、ターミナルでシリアル接続して、直にPython interpreterに書くのがてっとりばやい。

```shell
% sudo cu -l /dev/cu.usbserial-B55A3DF445 -s 115200
Connected.

[MAIXPY]Pll0:freq:832000000
[MAIXPY]Pll1:freq:398666666
[MAIXPY]Pll2:freq:45066666
[MAIXPY]cpu:freq:416000000
[MAIXPY]kpu:freq:398666666
[MAIXPY]Flash:0xc8:0x17
open second core...
gc heap=0x80184b70-0x80204b70
[MaixPy] sd_init | SD_CMD0 is FF
[MaixPy] init end

 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

M5StickV by M5Stack : https://m5stack.com/
M5StickV Wiki       : https://docs.m5stack.com
Co-op by Sipeed     : https://www.sipeed.com

[MAIXPY]: result = 0
[MAIXPY]: numchannels = 1
[MAIXPY]: samplerate = 44100
[MAIXPY]: byterate = 88200
[MAIXPY]: blockalign = 2
[MAIXPY]: bitspersample = 16
[MAIXPY]: datasize = 158760
init i2c2
[MAIXPY]: find ov7740 (ここでCtrl-Cを押して強制終了)
Traceback (most recent call last):
  File "_boot.py", line 38, in <module>
  File "./boot.py", line 122, in <module>
NameError: name 'sys' isn't defined
MicroPython v0.3.2-44-ga21a2ba1c-dirty on 2019-06-30; M5StickV with Kendryte-k210
Type "help()" for more information.
>>> 
>>> 
```

今後は、


1. emacsでコーディング
2. uPyLoaderで書き込みboot.pyを上書き
3. 再起動実行

というサイクルで使うのかな。

## 続報 2019-09-05

uPyLoaderでファイルを転送する場合にも、boot.pyを殺す必要がある。すなわち、下側ボタンを長押ししてリブートさせたあとすぐに正面ボタンを長押しする。

uPyLoaderでM5StickVからファイルを転送するのには成功したが、逆はうまくいかない。

SDメモリは秋葉原でわざわざ買ってきたものがみごとに[ハズレ](https://docs.google.com/spreadsheets/d/10Vv8ZQkbXX59aT_GkoolTMHf83zroIT21uNjvQMaGng/edit#gid=0)。なかなかプログラムを書くところまでいかずもどかしい。

## 続報2 2019-09-11

デジカメに使っていたmicroSDなら認識することが判明。フォーマットし、brownieのコードを入れてから再起動するのだが、SDを差しても抜いても起動しない。

Serial コンソールから直接Pythonを書いてboot.pyの中身を確認したところ、本体フラッシュのboot.pyが壊れているらしく、にっちもさっちもいかなくなった。調べたところ新しいFirmwareが0830に出ていたのでこれを入手し書き換えて一新。

Firmwareの書き換えは怖いほど時間がかかる。

書き換えた。内蔵flashからは起動するようになったが、SDからは起動しない。どういう優先順位になってるんだ？

どうもtranscendのSDでもだめっぽい。また出直す。


## ToDos

* 当面の目標はBrownieを動かし、ボタンを押した瞬間以外スリープするようにしたい。
* 仮に、KPUを使わずにただのビデオカメラとして使うとどれぐらいのfpsを出せるのか。→7fpsぐらい? 大差ない。
* シャッターボタンを組みこんで、とりあえず普通のstill cameraにできるか。→できるけど、保存方法がまだ不明。
* gyroは入っているという説がある。([https://tech.144lab.com/entry/2019/07/24/M5StickV_IMU](https://tech.144lab.com/entry/2019/07/24/M5StickV_IMU) )これを見ていると、まだFirmWare自体開発中っぽい。
* 電池を内蔵しているのでWirelessでは使えるものの、Wifiが搭載されていない。この点はPi Zero (Zero Wではなく)に近い。Groveコネクタを使って、外部と連携させないとただのカメラになってしまう。
* KPUの学習をさせる方法を知りたい。
* 適切な用途。



[M5StickV](/M5StickV) [2019夏の自由研究](/2019夏の自由研究)  [自由研究](/自由研究) 
[IoT](/IoT)





## Linked from

* [2024夏の自由研究](/2024夏の自由研究)
* [M5StickVの初期設定](/M5StickVの初期設定)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/M5StickVの初期設定.md)

