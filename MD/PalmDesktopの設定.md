#tips




## PalmDesktop on MacOSXの覚え書き

handera330を、Macと同期させる方法。

1. remove /Library/Application Support/Palm* - matto 
1. remove /Application/Palm - matto 
1. remove ~/Documents/Palm
1. PalmDesktop4.1.2をインストール
1. PalmDesktopとClie SL10の同期
1. iSyncを起動
  1. 「Palmデバイスの同期を有効にする」PalmDesktopと重複しているsync機能(カレンダーなど)を排除する。
  1. HotSync設定でiSync conduitが設定されていることを確認
1. iSyncで同期

## シリアルクレードルをMacで使う。

* http://www.ne.jp/asahi/masa/training/oitoku/mac_palm_sync/index.html これによれば、HanderaならMissingSyncなしでもMacと同期できる。
* http://www.palm.com/jp/support/downloads/mac_desktop40.html PalmDesktop suitable for Handera330 - matto 
* HanderaのUSB接続には、ありあわせのUSB-CVRS9を使用。USB-CVRS9の中身はProlific PL-2303らしい。 http://www.prolific.com.tw/eng/downloads.asp?ID=31 ドライバーを入手 - matto 
* http://www.osxhax.com/archives/000006.html これが一番参考になった。Info.plistをかきかえ(dictを書きたすのではなく)たあと、kextloadでドライバーを読みこませる。 - matto 

## その他

* Handeraを接続するためのUSB-serial変換器があまりにてこずるので、Clie SL10を復活させようかと思ったが、こいつはコンデンサが抜けちゃってるらしい。電池を抜くと即座に忘れる。ひどい製品だな。 - matto 
* iSyncでうまくいかない原因は、古いフォルダが残っているせいの場合が多い。 - matto 
* 数年ぶりのHotSyncなので非常に時間がかかった。 - matto 
* sudo kextload /System/Library/Extensions/ProlificUsbSerial.kext  - matto 
<!--  -->


