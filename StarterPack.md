---
title: StarterPack
---

# スターターパックサンプル


## 通信機能付きPalm

以下のファイルをPalmにインストールしてください。

<dl>
  <dt>[NCSync](/NCSync)</dt><dd>[NCSync](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/ncsync0.10b26ja.prc)
</dd>
  <dt>[MemoURL](/MemoURL)</dt><dd>[](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/MemoUrl.prc)
</dd>
  <dt>[PalmZLib](/PalmZLib)</dt><dd>[PalmZLib](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/SysZLib.prc) (全機種)または[PalmZLib](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/ArmSysZLib.prc) (OS5以降)
</dd>
  <dt>[拡張版PluckerViewer](/拡張版PluckerViewer)</dt><dd>[拡張版PluckerViewer](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/20040527ja.prc)または [拡張版PluckerViewer](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/20040704ja.prc)(ローレゾ機専用)
</dd>
  <dt>[RetrievR](/RetrievR)</dt><dd>開発中
</dd>
</dl>

## Palm一般

以下のファイルをPalmにインストールしてください。

<dl>
  <dt>[PalmZLib](/PalmZLib)</dt><dd>[PalmZLib](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/SysZLib.prc) (全機種)または[PalmZLib](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/ArmSysZLib.prc) (OS5以降)
</dd>
  <dt>[拡張版PluckerViewer](/拡張版PluckerViewer)</dt><dd>[拡張版PluckerViewer](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/20040527ja.prc)
</dd>
</dl>

## オプション1

Windows機とHotSyncする際に自動的に[NewsClip](/NewsClip)から記事をダウンロードするには、以下のパッケージをインストールしてください。

<dl>
  <dt>JSync</dt><dd>[](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/JSyncInstaller.exe)
</dd>
  <dt>[NewsClipSync Conduit](NewsClipSync Conduit)</dt><dd>[NewsClipSync-0.36.zip](http://wiki.yoshimov.com/wiki.cgi?action=ATTACH&page=NewsclipSync+Conduit&file=NewsclipSync%2D036%2Eexe) ([Yoshimopedia](http://wiki.yoshimov.com/wiki.cgi)より)
</dd>
</dl>

## オプション2

[Plucker](/Plucker) viewerで記事を読んでいるときに切れていたリンクを、HotSync時にWindows機上でブラウズするには以下のパッケージをWindows機にインストールしてください。

<dl>
  <dt>[MemoURL](/MemoURL)</dt><dd>[memourl.zip](http://muchy.com/CGI/count.cgi?http%3A%2F%2Fmuchy%2Ecom%2Fdata%2Fmemourl%2Ezip+PW002769) ([muchy.com](http://www.muchy.com)より)
</dd>
</dl>

## ユーザ登録

[NewsClip新規登録](http://newsclip.chem.nagoya-u.ac.jp/cgi-bin/newsclip.cgi?Register=1)画面にアクセスして、利用登録してください。


# スターターパックの設計

[newsclip](/newsclip)


## インストール

Clie+Windows+[Plucker](/Plucker)を想定する。どれだけ手数を減らすことができるか。

* Palmにインストールするプログラムは[まとめ](/まとめ)ておく。
* Windowsのソフトはインストーラがある方が良い。
* 登録ページのhtmlファイルを含んでおき、それを開いてメールアドレスを入れればユーザ登録できるようにする。
* NewsClip Server
   * ユーザ登録直後から、人気10チャンネルが購読できるようにする。(サーバ側の追加機能)
   * [Plucker](/Plucker) 8bppをデフォルトで指定。
* [Plucker](/Plucker) Viewer
   * Clieにあわせてあらかじめカスタマイズしておく。
   * [NCSync](/NCSync)との連携をスムーズにするために、MemoURL DBを[Plucker](/Plucker) Viewer側から作成できるようにする。



## 記事を読むソフト


### Palm

* plucker viewer..画面深さなどの初期値をあらかじめデバイスにあわせてカスタマイズした物を準備
* zlib

### Zaurus

* [Opie Reader](http://www.timwentford.uklinux.net/)?..日本語化が必要 [http://www.sibelle.info/gadgets/zopier.htm](http://www.sibelle.info/gadgets/zopier.htm)
* 適当な[Docリーダ](/Docリーダ)

### PocketPC

* [Vade Mecam](http://sourceforge.net/projects/vade-mecum)?..日本語化が必要
* 適当な[Docリーダ](/Docリーダ)
----


## 同期ツール


### Palm単体で[NewsClip](/NewsClip)を利用する

* [NCSync](/NCSync)

## 母艦はWindows

* [NewsClipSync Conduit](/NewsClipSync Conduit)
----


## オプション


### [MemoURL](/MemoURL)



[](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/MemoUrl.prc)

[](http://theochem.chem.okayama-u.ac.jp/vitroid/StarterPack/JSyncInstaller.exe)









## Linked from

* [NewsClipSync Conduit](/NewsClipSync Conduit)
* [StarterPack](/StarterPack)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/StarterPack.md)

