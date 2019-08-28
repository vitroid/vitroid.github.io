#palmware


# MemoURL DA/DD(ver. 0.8)

(平成14年11月23日(土))



MemoURLへの登録を支援するDA module/DD module


## ダウンロード

* [](storage:MemoURL DA/memourlda.prc) MemoURL DAバイナリ(2kbytes)
* [](storage:MemoURL DA/memourldd.prc) MemoURL DDバイナリ(2kbytes)
* [](storage:MemoURL DA/googleda.prc) Google DAバイナリ(6kbytes)
* [](storage:MemoURL DA/memourlda-0.8.tar.gz) ソース

## 概要

<dl>
  <dt>MemoURL DA</dt><dd> メモ帳などで選択した文字列(もしなければクリップボードの内 容)をMemoURLに登録します。
</dd>
  <dt>MemoURL DD</dt><dd> メモ帳などで選択した文字列をMemoURLに登録するDrag & Dropモジュールです。
</dd>
  <dt>Google DA</dt><dd> メモ帳などで選択した文字列(もしなければクリップボードの内 容)をMemoURL経由でGoogleで検索するよう予約します。
</dd>
</dl>


DDを利用するには、Drag&Dropをインストールしておく必要があります。また、DAを利用するには、あらかじめ適当なDA Launcherをインストールしておく必要があります。MemoURL DA/DDを使うまえに、あらかじめMemoURL(アプ リケーション版、ver.1.4以降)をインストールしておく必要があります。


## 動作

MemoURL DA/DDは、選択された文字列のうち、"http"よりも前の部分をMemoURLに登録する時の Bookmark名とみなします。例えば、「MemoURLに関する情報は http://www.geocities.co.jp/SiliconValley/6737/」という文字列を選択して MemoURL DD/DAで登録すると、「MemoURLに関する情報は」の部分がbookmark名 に、「http://www.geocities.co.jp/SiliconValley/6737/」がURLに登録され ます。



MemoURL DA/DDで登録されたURLは「一回だけ開く」設定となります。設定を変 えたい場合はアプリ版のMemoURL(ver.1.4以降)を使って下さい。






## 著作権

このソフトウェアはGNU Public Licenseに準拠するフリーウェアです。


## 関連ソフト

<dl>
  <dt>MemoURL</dt><dd>Palm上で収集したURLを、HotSync時に母艦PC上のブラウザで表示
</dd>
  <dt>RetrievR</dt><dd>MemoURLで収集したURLを、専用Proxyサーバ経由でPalm単体で閲覧
</dd>
  <dt>拡張版PluckerViewer</dt><dd>MemoURL対応拡張機能つきのオフラインブラウザ
</dd>
  <dt>Drag&Drop</dt><dd>様々な編集機能を追加できるHackWare。
</dd>
</dl>

## 謝辞

MemoURLというすばらしいアイディアを具体化し、なおかつソースを見せて下 さいました門田さんに深く感謝いたします。MemoURL DD/DAのソースの一部は、 門田さんから頂いたものをそのまま使用しています。




## Change Log



<dl>
  <dt>平成16年5月7日(金) Version 0.8</dt><dd>Googleの仕様変更にともない、googledaを改良。(吉永さんありがとう)
</dd>
  <dt>平成15年2月5日(水) Version 0.7</dt><dd>DAのdialog windowの境界判定を改善。(高橋さんありがとう)
</dd>
  <dt>平成14年11月23日(土) Version 0.6</dt><dd>MemoURL1.4仕様に準拠。URLとTITLEの長さの制限がなくなった。
</dd>
  <dt>Version 0.5</dt><dd>二重起動を防ぐコードを追加
</dd>
  <dt>Version 0.4</dt><dd>クリップボードからもセレクションからも文字列を取得できなかった場合にFatal Errorとなるバグを修正。
</dd>
  <dt>Version 0.3</dt><dd>細かい使い勝手の改善をおこなった。
</dd>
</dl>
* MemoURL DD & MemoURL DA: URLにhttp://が含まれていない場合は追加する。
* Google DA: 引用した文字列をselectするように変更
* Google DA: clipboardから引用したあと、clipboardを消去するようにした。
* clipboardから切り出す手続きを共通化
<dl>
  <dt>Version 0.2</dt><dd>StrNCopy周辺の改善、google DAを追加
</dd>
