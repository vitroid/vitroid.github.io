---
---
[web](/web) service
# Phorum 5のインストール
[CPML](/CPML)の掲示板として、phorumを採用するかどうか検討。他の候補としてslashsterを検討する。
1. http://phorum.org/から安定版5.0.10のソースを取得。
1. webのディレクトリ内でphorumのソースを展開し、ownerを変更。
1. include/db/config.phpの中身を適当に書き換える。
1. admin.phpをブラウザから呼び出してみたが、mysql_connectが呼び出せないというエラーが出る。php4以外にphp4-mysqlが必要だったのでapt-getでインストール。
```
# apt-get install php4 php4-mysql
```
1. mysqlのユーザを作成。
```
# mysqladmin create phorum5
# mysql phorum5
mysql> GRANT Select,Update,Insert,Delete,Create ON phorum5.* TO phorum5@localhost IDENTIFIED BY '********';
```
1. admin.phpを呼び出し、エラーをつぶしてゆく。
1. 管理者のアカウントadmin, メールアドレスcpml-admin, パスワードは******
1. http://www.bitscope.co.jp/library/phorum/[id_194_](/id_194_) を参考にメッセージを日本語化。本家においてある日本語メッセージは少しバージョンが古い(5.0.6用)ため、いろんなメッセージがちゃんと表示されないので、[英語](/英語)のメッセージにしかないメッセージを追加してやる必要があった。
1. あとは、管理者グループを作ったり細かい設定の調整。
## 使い勝手
メーリングリスト機能がついていれば、cpml本体をこっちにうつしてしまうのだけれど。PhorumにしてもSlashsterにしても、メンバーリストがSQLデータベースなので、fmlと共有させるのはちょっと難しい。
# slashsterのインストール
1. ソースを、[CPML](/CPML)のwebディレクトリ以下に展開。
1. 説明書き通りにsetup/configureを実行するとエラーが出るので、以下のディレクトリを作成する。
```
# mkdir cron/tmp
# mkdir friendlist
```




----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/CPML用掲示板の検討.md)
