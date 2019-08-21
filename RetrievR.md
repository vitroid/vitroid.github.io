---
---
[palmware#web](/palmware#web) service
# [RetrievR](/RetrievR)(仮称)
ref_image main.png
レトリバーと読みます。鋭意開発中。[RetrievR](/RetrievR)は、非同期でwebを取得するpalmwareです。

[MemoURL](/MemoURL)の機能（PalmでURLを書きためておいて、HotSync時にそれらをPCのブラウザで閲覧する）を、Palm単体で（できる範囲で）実現することを目的にしています.
## 動作
Palm上の[RetrievR](/RetrievR)からURLを複数[まとめ](/まとめ)てリクエストすると、専用の非同期ウェブプロキシサーバがリクエストされたページを取得し、30秒以内にサーバがMeDocもしくは[Plucker](/Plucker)形式に変換して返信するので、[RetrievR](/RetrievR)はそれを取得しインストールします。間に合わなかったページはサーバにとり置かれ、次回アクセス時にダウンロードされます。

[RetrievR](/RetrievR)は、[MemoURL](/MemoURL)データベースに記録されているURLを直接ダウンロードした後、[MemoURL](/MemoURL)データベースのエントリを消しません。取得済みのURLを[MemoURL](/MemoURL)データベースから完全に消去するには[MemoURL](/MemoURL)アプリケーションが必要です。
## インストール
次の4つのファイルをPalmにインストールしてください。
<dl>
  <dt>ref 20040825en.prc</dt><dd>[RetrievR](/RetrievR)本体(v0.1b72, 2004-08-25. Emulatorでは動作しますが、実機では非常に不安定です。)
</dd>
  <dt>[PalmZLib](/PalmZLib)</dt><dd>圧縮ライブラリ
</dd>
  <dt>ref MemoUrl.prc,[MemoURL](/MemoURL)</dt><dd>[MemoURL](/MemoURL)アプリ([英語](/英語)版)。[NCSync](/NCSync)経由で[NewsClip](/NewsClip)にチャンネル設定を還流させるのに内部で使用しています。
</dd>
  <dt>ref [MemoURL](/MemoURL)_Search_US.pdb,[MemoURL](/MemoURL)</dt><dd>[MemoURL](/MemoURL)用検索プラグイン([英語](/英語)版)
</dd>
</dl>
以下は好みで選んでください。
* [拡張版PluckerViewer](/拡張版PluckerViewer)
* Me[Docリーダ](/Docリーダ)
* [MemoURL DA](/MemoURL DA)
## 使い方
1. [MemoURL](/MemoURL)に、URLを登録します。[MemoURL](/MemoURL)アプリで直接指定するか、[MemoURL DA](/MemoURL DA)/DDなどのヘルパーアプリを使うか、[拡張版PluckerViewer](/拡張版PluckerViewer)などの[MemoURL](/MemoURL)対応アプリで登録してください。
ref_image memourl.png
1. [RetrievR](/RetrievR)を起動し、猫が二匹描いてあるボタンを押すと、Proxyサーバとの通信が始まり、サーバにリクエストを送り、指定された時間待ってから、巡回済みのWebページをダウンロードします。（猫一匹のボタンを押した場合は、リクエストを送るだけでダウンロードは行いません。）
ref_image main.png
1. [Plucker](/Plucker)形式を指定した場合は、ダウンロードしたページを[拡張版PluckerViewer](/拡張版PluckerViewer)で閲覧してください。
ref_image plucker main.png
## 他ソフトウェアとの比較
### ブラウザのオフライン機能との比較
最近のPalmにはNetFrontなどの本格的なブラウザが標準で入っている場合も多く、オフライン使用時にリンクがきれていても、オンラインになったときに[まとめ](/まとめ)て巡回することはできるので、[RetrievR](/RetrievR)を使う必要性を感じないかもしれません。[RetrievR](/RetrievR)を使うメリットは、
* [MemoURL](/MemoURL)と連携している。[MemoURL DA](/MemoURL DA)やGoogle DAなどでURLを書きためておけるので、メモ帳やアドレス帳、Docファイルなどあらゆるデータに出現するURLを巡回できます。
* 巡回結果はMeDocや[Plucker](/Plucker)形式で取得できるので、普段利用する[Docリーダ](/Docリーダ)で読むことができる。
* サーバ側で巡回するので、Palmの通信速度や処理速度に依存しない。旧機種のPalmでも利用可能。
* Palm用クライアントは20kバイトと非常にコンパクト。
* サーバからPalmへの転送時には圧縮が行われ、通信量、電池消費量が極小化される。
* 巡回リクエストとダウンロードを別セッションで行えるので、通信が不安定な場合には巡回リクエストだけ送って、ダウンロードを後日行うこともできる。
[RetrievR](/RetrievR)の大きな欠点は、対話的なページ(webフォーム)や、PDFなどの
異種ファイルを扱えないことです。
### [NewsClip](/NewsClip)との比較
[NewsClip](/NewsClip)は同じサイトを定点観測することを目的としています。そのため、不要な部分を切り取ったり、前日の記事との差分をとって、必要部分だけに絞り込む機能が充実しています。[RetrievR](/RetrievR)は、単なるプロキシサーバなので、そのような編集機能はありません。

一方、[NewsClip](/NewsClip)の編集機能を使うには、ユーザ登録とPCが不可欠ですが、[RetrievR](/RetrievR)はPalm単体で登録なしにだれでも利用できます。
### [MemoURL](/MemoURL)との比較
PCがなくてもよいのが最大のメリットです。

## サンプルサーバ

http://newsclip.chem.nagoya-u.ac.jp/cgi-bin/ret.cgi
## Link
* [MemoURL](/MemoURL)
* [拡張版PluckerViewer](/拡張版PluckerViewer)
* [NewsClip](/NewsClip)
* [NCSync](/NCSync)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/RetrievR.md)
