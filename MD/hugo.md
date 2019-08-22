訳あってPrivateに全文検索するサイトが欲しくなったので、今風に静的サイト生成器を使って作ってみる。

## install

[exlair.net](https://exlair.net/trend-for-static-site-generator/)さんの大変ありがたい比較記事を参考に、とりあえずHugoを入れて動かしてみる。Jekyllは自分の個人サイトですでに試してみたが、ページ数が多いとそれなりに遅いので、速いのがウリのHugoにする。

```shell
% brew install hugo
```

あとは上の記事のまま。

```shell
$ hugo version
Hugo Static Site Generator v0.55.4/extended darwin/amd64 BuildDate: unknown

$ hugo new site quickstart
$ cd quickstart
$ git init
$ git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
$ echo 'theme = "ananke"' >> config.toml
$ hugo new posts/my-first-post.md
$ hugo server -D
```

できた。速い。

## 検索したいページを作る

トップページに表示されるものはblogのポストっぽいがそれは使わないことにして、静的ページをcontent/program以下に並べておくことにしよう。

[http://rs.luminousspice.com/hugo-site-search/](http://rs.luminousspice.com/hugo-site-search/)さんを参考にする。

これは魔法のようは技術だ・・・

## 結局

luminousspiceさんの検索のjavascriptをよく読んだ結果、Hugoが必要なわけではなく、あらかじめ索引ファイルを1つ作っておけば十分高速に検索ができることがわかったので、当初の目的のためにはSSGもなにも要らないことが判明。今日はここまで。


#software
#hugo
#雑記
#インストール
