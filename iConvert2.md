---
title: iConvert2
---
[web](/web) service


# [iConvert2](/iConvert2)(仮称)

htmlページを携帯電話用に分割するスクリプトを作る。


## 覚え書き


### HTML::TreeBuilderの動作チェック

```
use HTML::Parser;
use LWP::Simple;
use HTML::TreeBuilder;
use Data::Dumper;
use HTML::FormatText;
use Jcode;

my $content = get("http://www.google.co.jp");
print $content;
my $tree = HTML::TreeBuilder->new;

$tree->parse( Jcode->new($content)->euc );
print Dumper( $tree );   #in data dump format

print $tree->as_HTML( '<>&' );  #in html format

my $format  = new HTML::FormatText(leftmargin=>0,rightmargin=>1000);
my $text    = $format->format( $tree );
print $text;                 #in plain text
```
TreeBuilderの生成するデータ構造を、各階層ごとに別ページに出力するようにしてみよう。双方向リンクになっている部分がどうなるか気にかかるが。


### いろいろ問題

* ~~どれぐらいの粒度に分割するかは、人によって、あるいはページによって好みが分かれるはず。粒度を簡単に変更できるとよい。~~2004-08-30 ヘッダ部分に100b/1k/5kの選択肢追加。
* 不具合が起こった（変な分割になった）場合に、すぐに不具合報告ができる仕組み。
* 画像がリンクになっている場合の取り扱いをどうするか。リンクをたどりたい場合と拡大画像を見たい場合をどう区別するか。
* タグごとに分割してもページが短くならない場合は、コンテンツの途中で強制ページ分割すべきだろう。
* 連続するブロックの間の相互リンクが欲しい。


* formはどうなる? - [matto](/matto) (2004年08月30日 00時43分55秒)
* 最初のページがいきなりブロック分割される問題。 - [matto](/matto) (2004年08月30日 13時05分29秒)
<!--  -->


## Linked from

* [iConvert2](/iConvert2)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/iConvert2.md)
