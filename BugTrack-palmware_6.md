---
---
# proxy情報が正しく更新されない
* 投稿者： tw1nspapa
* カテゴリ： [NCSync](/NCSync)
* 優先度： 重要
* 状態： 提案
* 日時： 2005年08月17日 18時38分44秒

## 内容
proxy初期状態として「mbox.chem.nagoya-u.ac.jp」(24文字)が設定されていますが、これをすべて削除したうえで24文字よりも短い入力を行った場合、初期値の一部が残ってしまいます。

リリースされてからかなりの期間において同様の報告がないところを見ると、私だけの問題なのかもしれませんが、もしお気づきの点などあれば、対応についてご教授いただければ幸いです。

ちなみに使用デバイスはTungsten|Cです。

例)
「mbox.chem.nagoya-u.ac.jp」を全て削除したのち、「hoge.hoge.hoge.com」(18文字)を入力。いったんOKを押して「Proxyサーバの設定」画面を終了させ、再度同画面を開くと、「hoge.hoge.hoge.com.ac.jp」となってしまいます。

## コメント
<!--  -->



----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/BugTrack-palmware_6.md)
