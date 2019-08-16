# M5StickVの初期設定

M5StickVはM5Stackの小型版(M5Stick)の、さらにAIエンジン搭載のもの、らしい。情報がなく、いろいろ苦労する。



### Firmwareの書き込み

小林先生の https://qiita.com/mayfair/items/d1a4ad360670c61ba0fa ほかいろいろ参考にするもKflash-gui 1.5.2が動かず、古いバージョン1.2は書き込みに成功しない。




* pip install kflushでCUIツールをインストール
* [M5Stack Quick Start](https://docs.m5stack.com/[/en/quick_start/m5stickv/m5stickv_quick_start)からfirmwareを入手。](/en/quick_start/m5stickv/m5stickv_quick_start)からfirmwareを入手。.md)
* 電源を落とし、一旦コネクタを抜いたあと、正面のAボタンを押しながらコネクタを差し込んでboot.pyの自動起動を回避。
* 以下のcommandで書き込んだ。
        kflash -B M5StickV  -p /dev/cu.usbserial-B55A3DF445 -b 115200 ~/Downloads/m5stickV_Firmware_0630Fixed.kfpkg 
       -Bには機種名を入れるのだが、M5StickVがどれに該当するのかわからず、適当に書いたら自動認識(goE/kd233)してくれた。

* Serial TerminalからのHello worldの実行は問題なかったが、MaiXPy IDEからのコードの書きこみはまだうまくいかない。もしかして、IDEで書いたあと、一旦セーブして、あらためて転送しないといけない?
* uPyLoaderの意義もよくわからない。MaiXPy IDEのtransferは機能しないのだが、uPyLoaderを一旦実行して、__upload.pyが生成したら問題は解決する、のか? 
* とりあえず書いてある通りにやってみる。uPyLoaderをダウンロードし、実行。M5StickVにはじめから書きこまれているファイルをMacに落として中身を見てようやく理解。boot.pyが起動時に実行されているようだ。つまり、これを書きかえてやれば、何でもできる、と。
* 処理の様子を見る限り、MicroPythonでもそれなりの速度が出ている。また、kpuを利用したければ、MicroPythonを使わざるをえないのだろう。とりあえずIDEは当分使わない予定。



さくっと試しに実行するだけなら、ターミナルでシリアル接続して、直にPython interpreterに書くのがてっとりばやい。

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
    

今後は、


1. emacsでコーディング
2. uPyLoaderで書き込みboot.pyを上書き
3. 再起動実行

というサイクルで使うのかな。



### ToDos


* 仮に、KPUを使わずにただのビデオカメラとして使うとどれぐらいのfpsを出せるのか。→7fpsぐらい? 大差ない。
* シャッターボタンを組みこんで、とりあえず普通のstill cameraにできるか。→できるけど、保存方法がまだ不明。
* gyroは入っているという説がある。(https://tech.144lab.com/entry/2019/07/24/M5StickV_IMU )これを見ていると、まだFirmWare自体開発中っぽい。
* 電池を内蔵しているのでWirelessでは使えるものの、Wifiが搭載されていない。この点はPi Zero (Zero Wではなく)に近い。Groveコネクタを使って、外部と連携させないとただのカメラになってしまう。
* KPUの学習をさせる方法を知りたい。
* 適切な用途。



[M5StickV](M5StickV.md) [2019夏の自由研究](2019夏の自由研究.md) 



