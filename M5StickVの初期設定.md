---
---
        kflash -B M5StickV  -p /dev/cu.usbserial-B55A3DF445 -b 115200 ~/Downloads/m5stickV_Firmware_0630Fixed.kfpkg 
       -Bには機種名を入れるのだが、M5StickVがどれに該当するのかわからず、適当に書いたら自動認識(goE/kd233)してくれた。
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
    
## Linked from

* [M5StickVの初期設定](M5StickVの初期設定.md)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/M5StickVの初期設定.md)
