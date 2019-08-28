---
title: CMS調査
---
[survey](/survey)

とあるサイトの構築に使うCMSの調査。


## 絞り込み

[http://www.cmsmatrix.org/で、以下の条件を与えて大雑把に絞りこむ。](http://www.cmsmatrix.org/で、以下の条件を与えて大雑把に絞りこむ。)

* WYSIWYG editor - ブラウザ上で文字の装飾を直接行える。
* Multilingual - 多言語対応
* UTF-8 - ユニコード対応。
* Online admin. - ブラウザ上での管理
* Content scheduling - コンテンツの掲示期間を自動管理
* Versioning - 変更履歴の記録
* Themes/Skins - 見た目を簡単に変更
* Third Party Developers - 開発者コミュニティがあるかどうか=OSSかどうか
* Content Approval = コンテンツの変更には責任者の承認が必要
あと考慮すべき条件は

* ライセンス。proprietaryなライセンスで、海外のソフトハウスの製品だと、国内サポートはまず期待できないし、会社がなくなると大変なことになる。日本人の開発者コミュニティがしっかりしたOSSが望ましい。
* 日本での使用実績。Multi-lingualといっても、欧米語だけという場合も多々ある。
* サーバ側の要件、Solaris+Postgresql。ただし、これを入れると選択肢を非常に狭めるので、とりあえずUnixで動く(Windowsではない)ものに限る。
とりあえず、上の条件にOSSを付加してしぼったのが以下のリスト。件数はgoogle日本語版での結果数。

* [http://www.ametys.org](http://www.ametys.org) ametys 3件
* [http://codejungle.is-a-geek.org](http://codejungle.is-a-geek.org) cms-bandits 8件
* [http://www.conterior.de](http://www.conterior.de) conterior 1件
* [http://drupal.org/](http://drupal.org/) drupal 1,110,000件
* [http://www.exoplatform.com](http://www.exoplatform.com) eXo platform  66件
* [http://ez.no](http://ez.no) eZ publish 124,000件
* [http://www.falt4.org](http://www.falt4.org) flat4 14件*
* [http://www.infoglue.org](http://www.infoglue.org) infoglue 40件
* [http://www.joomla.org/](http://www.joomla.org/) joomla! 1,160,000件
* [http://www.liferay.com/web/guest/home](http://www.liferay.com/web/guest/home) liferay 23,800件
* [http://source.mambo-foundation.com](http://source.mambo-foundation.com) mambo 135,000件
* [http://www.midgard-project.org/](http://www.midgard-project.org/) midgard CMS 488件*
* [http://www.cps-project.org/](http://www.cps-project.org/) Nuxeo CPS 27件
* [http://www.openedit.org](http://www.openedit.org) OpenEdit CMS 10件
* [http://www.openphpnuke.com](http://www.openphpnuke.com) OpenPHPNuke 22件
* [http://www.papaya-cms.com/](http://www.papaya-cms.com/) papaya CMS 82件
* [http://postnuke.com/](http://postnuke.com/) postnuke 17200件
* [http://www.typo3.org](http://www.typo3.org) typo3 218,000件
* [http://wordpress.org/](http://wordpress.org/) wordpress 1,750,000件*
* [http://www.xoops.org](http://www.xoops.org) xoops 2,130,000件
件数に*のついているものは、名前が一般的すぎるので、google検索のキーワードに「CMS」を追加して検索した。

[名前は重要](/名前は重要)である。検索にひっかかる名前でないと存在しないに等しい。ploneがひっかからなかったのはちょっと不思議。





日本語コミュニティの存在するCMSは限られている。

<dl>
  <dt>drupal</dt><dd>[http://drupal.jp/](http://drupal.jp/) サイト落ちてる?
</dd>
  <dt>ez publish</dt><dd>[http://www.zend.co.jp/ezpublish/](http://www.zend.co.jp/ezpublish/) なかなかよさそう。有償サポートあり。フリー版をサポートする会社もある。
</dd>
  <dt>joomla!</dt><dd>[http://www.joomla.jp/](http://www.joomla.jp/) [http://demo.joomla.jp/index.phpでスキンを変更すると全く違う印象に切り替わる。](http://demo.joomla.jp/index.phpでスキンを変更すると全く違う印象に切り替わる。)
</dd>
  <dt>mambo</dt><dd>後継がjoomla!らしい。
</dd>
  <dt>postnuke</dt><dd>[http://sourceforge.jp/projects/postnuke-jp/](http://sourceforge.jp/projects/postnuke-jp/) 見たかんじでは全く低調。
</dd>
  <dt>typo3</dt><dd>[http://www.typo3.ne.jp/](http://www.typo3.ne.jp/) 超高機能。そのせいで普及していないのかもしれないが、Enterprise CMSとしては完璧。世界的な導入実績では申し分ない。
</dd>
  <dt>wordpress</dt><dd>[http://wordpress.xwd.jp](http://wordpress.xwd.jp) personal publishing platformなのでちょっと目的が違うかも。
</dd>
  <dt>xoops cube</dt><dd>[http://jp.xoops.org/](http://jp.xoops.org/) コミュニティポータル構築用のオープンソースアプリケーションなのでこれも目的が違うかも。
</dd>
</dl>

## 生成するHTMLの品質

調査中。

* joomla!のWYSIWYG editorの出力はどこかで見たものとそっくり。たぶんJavascriptで書かれた汎用WYSIWYG editorを使いまわしているので、気にいらなければ外注して改善してもらえばいい。

## [まとめ](/まとめ)

今のところ候補は、joomla!、typo3、ez publishあたりか。ploneも候補のつもりだがCMS matrixで情報得られず。drupalも未調査。他に可能性があるのはMovable Type(これは化学G-COEで導入するので、実際に操作を試せる)。


## その他の情報源

* [http://www.cmshikaku.com](http://www.cmshikaku.com)
* [](cmsmatrix.pdf) 主要なCMSの機能比較表。
* [http://www.turbine.co.jp/index.html](http://www.turbine.co.jp/index.html) 名古屋でMovable Typeを実装する会社。 - [matto](/matto) (2007年11月29日 11時25分20秒)
* [http://www.site-master.jp/contact/index.html](http://www.site-master.jp/contact/index.html) 名古屋の会社。いろんなCMSを扱える。 - [matto](/matto) (2007年11月29日 11時28分17秒)
* [http://xlab.jp/](http://xlab.jp/) xoopsを扱う名古屋の会社。 - [matto](/matto) (2007年11月29日 11時30分07秒)
* [http://www.3pc.jp/content/blogcategory/12/87/](http://www.3pc.jp/content/blogcategory/12/87/) open CMSの比較。 - [matto](/matto) (2007年11月29日 11時40分31秒)
* 全学WebサーバではPostgreSQLが動いていませんでした。申し訳ありません。どこかに間借りすることになるなら、MySQLかPostgreSQLを条件で探してもらってますので、確定するまでお待ち下さい。 - たかた (2007年11月29日 18時47分22秒)




----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/CMS調査.md)

