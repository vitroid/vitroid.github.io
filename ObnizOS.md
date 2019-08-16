# Obniz OS
つい先日国内でも公開されたObniz OSを、さっそくESP32-CAMに入れて試す。

(もっぱらobnizのウェブページの[説明](https://obniz.io/doc/obnizos/os_overview)通りに問題なく進みました。)

## ESP32-CAMをMacに接続
ESP32-CAMはUSB端子を持たないので、Serial Adapterを介して接続する。

参考: [1300円のESP32-CAMでWebカメラを試す](https://qiita.com/Nabeshin/items/b195cad1afe99ce29f1e)

書き込み時にはIO0をGNDに接地しておくことに注意。

## Obniz OSの書き込み
[Obniz OSの説明ページ](https://obniz.io/doc/obnizos/os_install)を参考にOSを書き込む。

書き込みおわったらIO0のジャンパーを外してからリセットし、Mac側はminitermを使ってESP32にシリアル接続する。

## ライセンスキーの購入
[Obniz OSの説明ページ](https://obniz.io/doc/obnizos/os_devicekey)の説明に従い、Obniz OSのライセンスを購入します。1500円です。

ライセンスを購入すると、デバイスキーが発行されました。これを、上でシリアル接続したESP32に書き込みます。

このあたりの作業は、Obnizハードウェアを使う場合には必要なかったですね。
## ESP32をWifiにつなぐ
デバイスキーを入力したあと、Wifiの接続に入ります。Obnizハードウェアの場合には本体画面上で作業しましたが、ESP32の場合はシリアルコンソールからの作業なので、かえって楽です。

とちゅうでObniz ID(8桁の数字)が表示されます。

    obniz id: 12345678

接続が成功すると、Onlineと表示され、コンソールからは操作ができなくなります。

## デモプログラムの実行
[Obniz.io](https://obniz.io)から、右上の「Developer Console」を押して、プログラム画面に遷移します。デバイスメニューでObniz ID 12345678を選ぶと、サンプルプログラム(Javascript)が表示されます。

このデモプログラムはボタンでLEDを点滅させるだけのコードですが、とりあえず動作を確認するには十分です。ESP32-CAMのストロボLEDは[GPIO4](https://www.esp32.com/viewtopic.php?t=11190)につながっているらしいので、デモコードの

    var led = obniz.wired("LED", { anode:12 } );

の部分を

    var led = obniz.wired("LED", { anode:4 } );
    
に変更して実行しました。


## カメラ
肝心のCamera (AI-Thinker)はまだ動いていません。

