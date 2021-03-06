#palmware




# 拡張版Plucker viewer

This page gives information on the hacking of plucker software. 



このページでは、私がplucker viewerに対して行った拡張のうち、本家で採用されていない独自機能を紹介します。



現在は本家から入手できる最新版のplucker viewerも日本語(J-OS, CJKOSを含む)に対応していますので、そちらをご利用下さい。

また、Plucker形式のファイルを生成するために必要なツールは本家より入手して下さい。


## PluckerViewerとは

Pluckerは、画像や装飾書体を含むハイパーテキストをPalm上で表示するツールです。Palm上で動く viewerのほか、UnixなどでHTMLやtextファイルを変換するツールが含まれてい ます。


## コンパイル済みバイナリ

上にいくほど新しくなります。どんどん機能が追加されているようですので、 最新のものをご利用下さい。不具合などの報告はできればNC-Fan2掲示板へおねがいします。


### 最新バージョン

<dl>
  <dt>[](storage</dt><dd>拡張版PluckerViewer/20040527ja.prc):2004/5/27版(plucker viewer1.8をベースに作成しました。tsPatch, annotation機能を新たに追加。vfsfont, antialiasなどのフォント関連の拡張機能は無効になっています。)
</dd>
  <dt>PalmZLib</dt><dd>圧縮形式の文書を閲覧する場合に必要です。
</dd>
</dl>

### ローレゾ用

上のバイナリがWorkPad 30Jでは動かなかったので、ハイレゾ対応を除いたバイナリを作成しました。

<dl>
  <dt>[](storage</dt><dd>拡張版PluckerViewer/20040704ja.prc):2004/7/04版(plucker viewer1.8をベースに作成しました。tsPatch, annotation機能を新たに追加。vfsfont, antialiasなどのフォント関連、およびハイレゾ拡張機能は無効になっています。)
</dd>
</dl>

### 以前のバージョン

<dl>
  <dt>[](storage</dt><dd>拡張版PluckerViewer/20040526ja.prc):2004/5/26版(新機能は追加していませんが、前回のコンパイルオプションに加えてtsPatchを可用にしました。)
</dd>
</dl>
これより古いバージョンは[旧ページ](http://www.chem.nagoya-u.ac.jp/matto/90/30Palm/plucker/)をご覧ください。


## 本家での開発状況

現在の本家の開発状況は以下の通りです。(平成15年11月19日(水)改訂)

<dl>
  <dt>Desktop</dt><dd>Plucker Desktopのメッセージは日本語化されています。
</dd>
  <dt>Parser</dt><dd>日本語のエンコーディングが変換されないため、Shift-JIS以外のページを巡回すると文字化けするはず。
</dd>
  <dt>Viewer</dt><dd>日本語に完全に対応しています。使える文字コードはShift-JISのみです。
</dd>
</dl>



## matto私家版の特長

以下では、正式にCVSにとりこまれていない(開発チームの同意を得ていない)拡張機能を提供します。平成15年11月19日(水)現在の独自拡張機能は以下の点のみです。

* MemoURLに対応する機能。外部リンクを、MemoURLに登録し、次回のHotSync時にPCのブラウザでそのリンクを表示できるようになります。この機能はコンパイル時のオプションです。
* (J-OS対応のためのパッチは開発版にとりこまれました。)
* (UX-50対応のためのパッチは開発版にとりこまれました。)
* Quick Export機能。外部リンクをタップすると、即時にMemoまたはMemoURLにexportされます。外部リンクは太いアンダーラインで通常のリンクと区別されます。この機能はコンパイル時のオプションです。一般設定の「書き出し」で設定することができます。
* Frequent Marking機能。検索やジャンプした時に、ジャンプ元の位置を自動的にhistoryに記録し、もといた場所に1ストロークで戻れるようにします。この機能はコンパイル時のオプションです。
* KIRA*さんによる、SonyのOS5デバイスでtiny/smallフォントの文字化けに対する修正。(平成15年12月04日(木))この機能はコンパイル時のオプションです。
* (rubikitchさんによる、手動でヒストリースタックに現在位置を記録する修正は開発版に取り入れられました。)
* (rubikitchさんによる、文書閲覧時にソフトウェアキーボードを抑止する修正は平成15年12月31日(水)に開発版に取り入れられました。)
* (タップして選択した単語を、クリップボードにコピーする機能は平成16年1月9日(金)に開発版に取り入れられました。ただし、日本語の文書の場合、一行まるごとコピーされてしまいます。)
* KIRA*さんによる、tsPatch対応修正。T|TなどのSony以外のOS5デバイスでも、tsPatchを援用することでtiny/smallフォントを使用できます。(平成16年1月18日(日))この機能はコンパイル時のオプションです。
ほかに要望があればmattoにお知らせ下さい。




## 既知の問題点

いろいろ。NC-Fan2を御覧下さい。




## 関連プロジェクト



<dl>
  <dt>NewsClip</dt><dd> オンラインでwebページの巡回を行うサービス。Plucker形式に対応しています。
</dd>
  <dt>PalmBasket</dt><dd> (約)1クリックであなたのサイトをPalmに流しこみます。 MeDoc/iSilo/tealdoc/Plucker形式に対応しています。Pluckerによる多階調画 像表示を試してみて下さい。
</dd>
  <dt>Plucker</dt><dd> 本家。  開発チームにはアジア人は少ないようで、マルチバイト対応ははじまった  ばかりです。Windows/Linuxでプログラムを書ける人は手伝って下さい。
</dd>
  <dt>MemoURL</dt><dd>Palm上で収集したURLを、HotSync時に母艦PC上のブラウザで表示。関連するツールにMemoURL DA、RetrievRなどがあります。
</dd>
</dl>
<!-- :るびきちさんのplucker関連情報のページ。:必見。 -->

## 翻訳者・開発者募集

Plucker開発チームではPluckerのツール群のメッセージやヘルプを翻訳してくれる方を募集しています。現在のPluckerツールには、Linux Zaurusで動くviewerや、Windowsでウェブページを巡回するパーザーなど、多種多様なソフトウェアが含まれています。それらの多くは、メッセージを日本語化し、少しパッチをあてるだけで、日本人が簡単につかえるツールになります。現在開発チームには僕しか日本人がいないようですが、とてもそこまで手が回りません。「俺のりぬざうでPluckerを動かしてやるぜ」「画像入りのウェブページをとりこめる巡回ソフトが欲しい」という方、ぜひご連絡下さい。Windows/Linuxで開発できる人ももちろん歓迎です。








## License notice

This is free software.




## 謝辞

Pluckerを開発したみなさん、Pluckerを日本語化するために改良すべき個所を 教えてくれたMichael Nordstromさん、J-OSに関する詳しい情報をいただいた 山田さん他palm-tech-mlのみなさん、ありがとうございました。みなさんの適 切なアドバイスのおかげで、思っていたよりもずっと早く、とりあえず動くバー ジョンを公開できました。




## 履歴

<dl>
  <dt>平成16年4月16日(金)</dt><dd>2004年1月以降のソースを使うと、HandEra 330でFatal Errorになるので、その点をQuick Hackした。
</dd>
  <dt>平成15年12月04日(木)</dt><dd>KIRA*さんの修正を追加。パッチ提供ありがとうございました。
</dd>
  <dt>平成15年5月26日(月)</dt><dd>Strike-thru on libraryformを実装。
</dd>
  <dt>平成14年11月11日(月)</dt><dd>旧い実行ファイルを削り、大幅に整理しました。
</dd>
  <dt>平成14年9月4日(水)</dt><dd>cvsからファイルをとってくる方法、リンクを更新
</dd>
</dl>



## コメント

* http://www.timwentford.uklinux.net/ TWReader for Zaurus - matto (2004年05月31日 16時12分09秒)
* http://vade-mecum.sourceforge.net/ Vade Mecum for PocketPC - matto (2004年06月02日 12時01分56秒)




