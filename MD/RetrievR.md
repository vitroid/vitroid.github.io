#palmware#web service


# RetrievR(仮称)

![](storage:RetrievR/main.png)

レトリバーと読みます。鋭意開発中。RetrievRは、非同期でwebを取得するpalmwareです。



MemoURLの機能（PalmでURLを書きためておいて、HotSync時にそれらをPCのブラウザで閲覧する）を、Palm単体で（できる範囲で）実現することを目的にしています.


## 動作

Palm上のRetrievRからURLを複数まとめてリクエストすると、専用の非同期ウェブプロキシサーバがリクエストされたページを取得し、30秒以内にサーバがMeDocもしくはPlucker形式に変換して返信するので、RetrievRはそれを取得しインストールします。間に合わなかったページはサーバにとり置かれ、次回アクセス時にダウンロードされます。



RetrievRは、MemoURLデータベースに記録されているURLを直接ダウンロードした後、MemoURLデータベースのエントリを消しません。取得済みのURLをMemoURLデータベースから完全に消去するにはMemoURLアプリケーションが必要です。


## インストール

次の4つのファイルをPalmにインストールしてください。

<dl>
  <dt>[](storage</dt><dd>RetrievR/20040825en.prc):RetrievR本体(v0.1b72, 2004-08-25. Emulatorでは動作しますが、実機では非常に不安定です。)
</dd>
  <dt>PalmZLib</dt><dd>圧縮ライブラリ
</dd>
  <dt>[MemoURL](storage</dt><dd>RetrievR/MemoUrl.prc):MemoURLアプリ(英語版)。NCSync経由でNewsClipにチャンネル設定を還流させるのに内部で使用しています。
</dd>
  <dt>[MemoURL](storage</dt><dd>RetrievR/MemoURL_Search_US.pdb):MemoURL用検索プラグイン(英語版)
</dd>
</dl>
以下は好みで選んでください。

* 拡張版PluckerViewer
* MeDocリーダ
* MemoURL DA

## 使い方

1. MemoURLに、URLを登録します。MemoURLアプリで直接指定するか、MemoURL DA/DDなどのヘルパーアプリを使うか、拡張版PluckerViewerなどのMemoURL対応アプリで登録してください。
![](storage:RetrievR/memourl.png)

1. RetrievRを起動し、猫が二匹描いてあるボタンを押すと、Proxyサーバとの通信が始まり、サーバにリクエストを送り、指定された時間待ってから、巡回済みのWebページをダウンロードします。（猫一匹のボタンを押した場合は、リクエストを送るだけでダウンロードは行いません。）
![](storage:RetrievR/main.png)

1. Plucker形式を指定した場合は、ダウンロードしたページを拡張版PluckerViewerで閲覧してください。
![](storage:RetrievR/plucker main.png)


## 他ソフトウェアとの比較


### ブラウザのオフライン機能との比較

最近のPalmにはNetFrontなどの本格的なブラウザが標準で入っている場合も多く、オフライン使用時にリンクがきれていても、オンラインになったときにまとめて巡回することはできるので、RetrievRを使う必要性を感じないかもしれません。RetrievRを使うメリットは、

* MemoURLと連携している。MemoURL DAやGoogle DAなどでURLを書きためておけるので、メモ帳やアドレス帳、Docファイルなどあらゆるデータに出現するURLを巡回できます。
* 巡回結果はMeDocやPlucker形式で取得できるので、普段利用するDocリーダで読むことができる。
* サーバ側で巡回するので、Palmの通信速度や処理速度に依存しない。旧機種のPalmでも利用可能。
* Palm用クライアントは20kバイトと非常にコンパクト。
* サーバからPalmへの転送時には圧縮が行われ、通信量、電池消費量が極小化される。
* 巡回リクエストとダウンロードを別セッションで行えるので、通信が不安定な場合には巡回リクエストだけ送って、ダウンロードを後日行うこともできる。
RetrievRの大きな欠点は、対話的なページ(webフォーム)や、PDFなどの

異種ファイルを扱えないことです。


### NewsClipとの比較

NewsClipは同じサイトを定点観測することを目的としています。そのため、不要な部分を切り取ったり、前日の記事との差分をとって、必要部分だけに絞り込む機能が充実しています。RetrievRは、単なるプロキシサーバなので、そのような編集機能はありません。



一方、NewsClipの編集機能を使うには、ユーザ登録とPCが不可欠ですが、RetrievRはPalm単体で登録なしにだれでも利用できます。


### MemoURLとの比較

PCがなくてもよいのが最大のメリットです。




## サンプルサーバ



http://newsclip.chem.nagoya-u.ac.jp/cgi-bin/ret.cgi


## Link

* MemoURL
* 拡張版PluckerViewer
* NewsClip
* NCSync
