#palmware#newsclip




# NCSync

(version 0.10)




## はじめに

NCSyncは、Palm単体でNewsClipの記事をダウンロードするためのツールです。




## インストール

以下の4つのファイルをPalmデバイスにインストールして下さい。

<!-- *[](ncsync.prc) NCSync本体(日本語版、バージョン0.7、約19kB) -->
<dl>
  <dt>[](ncsync0.10b26ja.prc)</dt><dd>NCSync本体(日本語版、バージョン0.10build26、約21kB 2004-06-25)
</dd>
  <dt>PalmZLib</dt><dd>圧縮ライブラリ
</dd>
  <dt>[MemoURL](MemoUrl.prc)</dt><dd>MemoURLアプリ(英語版)。NCSync経由でNewsClipにチャンネル設定を還流させるのに内部で使用しています。
</dd>
  <dt>[MemoURL](MemoURL_Search_US.pdb)</dt><dd>MemoURL用検索プラグイン(英語版)
</dd>
</dl>

### 以前のバージョン

* [](ncsync0.10b26ja.prc) NCSync本体(日本語版、バージョン0.10build26、約21kB 2004-06-25)
* [](ncsync0.10b26en.prc) NCSync binary(English, version 0.10build26, about 21kB 2004-06-25)
* [](ncsync_ja0.10b24.prc) NCSync本体(日本語版、バージョン0.10build24、約21kB 2004-06-24)
* [](ncsync_en0.10b24.prc) NCSync binary(English, version 0.10build24, about 21kB 2004-06-24)
* [](ncsync_ja0.9b67.prc) NCSync本体(日本語版、バージョン0.9build67、約19kB 2004-06-24)
* [](ncsync_en0.9b67.prc) NCSync binary(English, version 0.9build67, about 19kB 2004-06-24)
* [](ncsync_ja0.9b57.prc) NCSync本体(日本語版、バージョン0.9build57、約19kB)
* [](ncsync_en0.9b57.prc) NCSync binary(English, version 0.9build57、about 19kB)

## 使い方

* Palmデバイス単体でインターネットに接続できる環境が必要です。
* まず、NewsClipに通常のブラウザでアクセスし、IDを取得します。(IDは、画面左上のユーザ名の直右に表示してあります。)
![](newsclip-id.png)

* NCSyncを立ちあげると、ID入力ウィンドウが出てきますので、ブラウザで表示された文字列(ハイフンでつながった3つの単語)を入れてOKを押して下さい。IDの設定は一回だけでOKです。
![](id-entry.png)

* ダウンロードするファイルの形式を選択して下さい。MeDoc、Default、Subset1、Subset2の中から選択できます。NewsClipウェブ画面で指定した形式でダウンロードする場合はDefaultを、記事サブセットをダウンロードする場合はSubset1/2を選択して下さい。
![](main.png)

![](main-menu.png)

右上の点線わく内をタップして、IDを再入力することもできます。また、メモリの余地を指定しておけば、メモリに収まるように、自動的にダウンロードするアーカイブの大きさが調節されます。

* 中央のクリップボタンを押すと、NewsClipに接続し、記事を取得します。
![](download.png)

![](expand.png)

ダウンロードの途中でキャンセルした場合も、もう一度クリップボタンを押してダウンロードを再開することができます。


## 注意

* トラブルがおきてリセットした場合は、NCSyncを再起動し、左下の「ログ」の内容を開発者までお知らせ下さい。
* MeDoc形式以外を選択した場合は、通信量を最小化するために、ZIP書庫形式でダウンロードしてから、Palm上で展開します。
* 記事サブセット1/2でダウンロードされるファイルのフォーマットは、NewsClip上で設定して下さい。
* 記事サブセットのファイル形式にText形式を指定した場合は、Palmがtextファイルを直接扱うことができないため、ダウンロード後展開されたファイルはZboxZでラップされた状態になります。このファイルをDocに変換したり削除したりするには、ZboxZが必要です。
* Palm上で、記事を選択する機能はあえて付けませんでした。
* バージョン0.3まではダウンロードする記事のファイル形式をNCSync上で指定できるようになっていました。しかし、現在のNewsClipシステムでは、iSilo形式やplucker形式を生成するのに非常に時間がかかるため、それぞれのチャンネルであらかじめ予約されているフォーマット以外は生成していません。ですから、普段MeDoc形式で購読しているチャンネルを、NCSync上で気まぐれにiSilo hires形式などでダウンロードしようとしても、実際にはダウンロードすることはできませんでした。そこで、バージョン0.4からは、ダウンロードするファイルの形式はWeb上で指定するようにしました。plucker形式などでダウンロードする場合は、あらかじめNewsClipウェブページ上で指定しておいて下さい。

## ソース

* [](ncsync-0.10b26.tar.gz)
* [](ncsync-0.10b24.tar.gz)
* [](ncsync-0.9b57.tar.gz)



## 著作権

このソフトウェアはGNU Public Licenseに基づくフリーソフトウェアです。 一方、ダウンロードしたそれぞれの記事については、原作者の著作権が及びますので、記事を再配布する場合は、原作者の許諾を得る必要があります。




## その他

NCSyncの開発にあたって、以下のソフトウェアを参考にしました。

* Plucker viewer
* palmboxer
* [ほしさんのpz](http://www.sra.co.jp/people/hoshi/palmos/pz-j.html)
* MemoURL
ソースを公開して下さっている方々に感謝いたします。




## 変更履歴

<dl>
  <dt>0.10</dt><dd>2004-06-24 Proxy対応。ただし認証はできません。バージョン1.0には、なれませんでした。
</dd>
  <dt>0.9</dt><dd>newsclip:xxxxx型のURLを解釈し、NewsClipサーバに送る機能を追加。Plucker文書中にncsyncタグを埋め込み、拡張版PluckerViewerのMemoURL連携機能を使うことで、Palm単体でチャンネルの購読予約ができます。2004-06-19 いろいろ問題があるようなので、配布を中止しました。2004-06-21unixのmemset()とPalmOSのMemSet()の引数の順番が違うことに気づかず、そのまま置き換えたため動かなくなったことが判明しました。修正しました。
</dd>
  <dt>0.8</dt><dd>メッセージの国際化など。
</dd>
  <dt>0.7</dt><dd>メモリ空き容量を計算し、メモリにおさまる範囲でダウンロードするようにした。
</dd>
  <dt>0.6</dt><dd>PalmBasketSyncとの分岐。ソースの大部分を共用する。
</dd>
  <dt>0.5</dt><dd>ダウンロードを中断したあと、3時間以内であれば再開できるようにした。
</dd>
  <dt>0.4</dt><dd>フォーマットの選択肢を変更、非圧縮Zipアーカイブがまれに展開できないバグを修正
</dd>
  <dt>0.3</dt><dd>即時切断オプションを追加
</dd>
  <dt>0.2</dt><dd>Progress Managerを導入し、ダウンロードや展開途中で中断できるようにした。
</dd>
  <dt>0.1</dt><dd>最初のバージョン
</dd>
</dl>
* VFS利用の要望あり。 - matto (2004年06月22日 01時15分01秒)
* proxy対応を要望。 - matto (2004年06月24日 10時26分24秒)
* http://x68000.startshop.co.jp/~68user/net/http-3.html proxy対応のサンプル - matto (2004年06月24日 10時29分07秒)
* NC syncのログに failed to open TCP. とありDLできません。NetFrontは使える環境なのですが、なにか設定ミスでしょうか? TH55使っています。 - 早川　祥史 (2004年08月31日 23時12分05秒)
* PalmOS5の機種は触ったことがないので詳しくはわかりませんが、環境設定のネットワークのパネルから直接接続を確立したうえで、NCSyncを起動してもエラーになるのでしょうか・・・ - matto (2004年08月31日 23時37分35秒)
* 間が空いてすみません。ご指摘のとおりにネットワークパネルから接続してNCSyncしましたが、やはりfailed to open TCP.となり接続できませんでした。そのままNetFrontを立ち上げるとつながります。ほかに確認することありませんか?よろしくお願いします。 - 早川　祥史 (2004年09月09日 23時19分03秒)
* nx73v + Wireless LAN で 404 エラーになります。 - tks (2004年11月15日 01時04分53秒)
* その他、状況は早川さんと同様のようです。申し遅れましたが、大変便利な環境をありがとうございます。 - tks (2004年11月15日 01時08分18秒)


[](main-menu.png)

[](expand.png)

[](download.png)

[](id-entry.png)

[](ncsync_en0.9b67.prc)

[](ncsync_ja0.9b67.prc)

[](newsclip-id.png)

[](ncsync_en0.10b24.prc)

[](ncsync_ja0.10b24.prc)

[](ncsync-0.10b24.tar.gz)

[](ncsync0.10b26en.prc)

[](ncsync0.10b26ja.prc)

[](ncsync-0.10b26.tar.gz)







