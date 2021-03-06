---
title: MML DA
---
[palmware](/palmware)


# [MML DA](/MML DA)(ver 0.9)

平成14年11月21日(木)


## ダウンロード

* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/mmlda.prc) [MML DA](/MML DA)本体
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/regmmlda.prc) reg[MML DA](/MML DA)本体
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/mmldd.prc) MML Drag&Dropモジュール本体
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/mmlpackdd.prc) MMLpack Drag&Dropモジュール本体
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/mmlda-0.9.tar.gz) ソース
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/galax.txt) MMLのサンプル、[](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/KansasCityStandard.txt) もう一つ。
* [](http://theochem.chem.okayama-u.ac.jp/vitroid/MML DA/galax.mid) それをMIDIファイルに変換したもの(PCだとピアノ音で再生されるのでかなり変です)

## 概説


### [MML DA](/MML DA)

スタイラスで選択した領域またはクリップボードの内容をMML(Music Macro Language)とみなし演奏するDAです。別途DA Launcherが必要です。


### reg[MML DA](/MML DA)

スタイラスで選択した領域またはクリップボードの内容をシステムのアラーム音に登録することができます。別途DA Launcherが必要です。


### MML DD

[MML DA](/MML DA)のDrag&Dropモジュール版です。選択した文字列をモジュールアイコンに重ねると演奏します。別途Drag&Dropが必要です。


### MMLpack DD

mmlpack DDは[MelodyEditor](/MelodyEditor)またはMMLで書かれた楽譜を、それなりに清書します。別途Drag&Dropが必要です。



mmlpack DDは選択された領域のMMLを清書し、余分な調号や記号をてきとうに省きます。[MelodyEditor](/MelodyEditor)で入力した曲をさっぱりさせたい場合に効果的です。ただ、完全に無駄を省けるわけではなく、時には余計な記号を追加してしまう場合もあることがわかっています。また、音長については、例えばc163がc24に置きかえられたり、c8^8がc4におきかえられたり、r8r8がr4におきかえられたり、といったおせっかいはしません。



これらを組みあわせると、ぱっと思いついた時に[MelodyEditor](/MelodyEditor)で曲を打込み、memopadにexportしてから、mmlpackddでMMLに清書して保管、必要な時に演奏したりアラームに登録したり、といった一連の流れができます。作った曲の管理は[MelodyEditor](/MelodyEditor)を利用してください。


## MMLとは

MMLは、N88-BASICに内蔵されていた音楽記述用簡易言語です(MSX-Basicも同じ文法のようです)。[MML DA](/MML DA)では、MMLの中の以下の非常に基本的な命令サブセットのみに対応しています。もちろん和音は鳴りません。MMLについては、[ここ](http://www2u.biglobe.ne.jp/%7Ealbelt/n88/mml)を参考に、ボリューム変更命令と連符指定命令以外に対応し、移調命令"i"を追加しています。(連符は、例えば8分音符を3等分したい場合は単に24分音符を指定すればよい)

<dl>
  <dt>a〜g(またはドレミファソラシ)</dt><dd>発音。cdefgab(またはドレミファソラ シ)の順で長調の1オクターブを構成。直後に数字、ピリオド、"^"(または「ー」)を付加して長さを指定可能。"+"または"["、"-"を音名の直後に複数付加して半音高くしたり低くしたりすることができます。MelodyEditor互換機能として、"~"で1オクターブ高くしたり、"_"で1オクターブ低くしたりすることもできます。なお、"+#-~_"はいずれも臨時記号で、以降の音には影響を与えません。音長を省略した場合は"L"命令で指定した長さになります。【例：c~++8.^24](/"、"-"を音名の直後に複数付加して半音高くしたり低くしたりすることができます。MelodyEditor互換機能として、"~"で1オクターブ高くしたり、"_"で1オクターブ低くしたりすることもできます。なお、"+#-~_"はいずれも臨時記号で、以降の音には影響を与えません。音長を省略した場合は"L"命令で指定した長さになります。【例：c~++8.^24) は、1オクターブ上のD音を、符点8分音符+24分音符分の長さ だけ演奏します】
</dd>
  <dt>r(またはッ、ン)</dt><dd>休符。直後に数字、ピリオド、"^"(または「ー」)を付加して長さを指定可能。音長を省略した場合は"L"命令で指定した長さになります。【例：r8.】
</dd>
  <dt>tx</dt><dd>テンポを4分音符=xに変更。
</dd>
  <dt>ix</dt><dd>半音のx倍だけ移調。xは-96より大きく96より小さい整数で指定、省略した場合は0
</dd>
  <dt>ox</dt><dd>オクターブをxに変更(xは省略不可)
</dd>
  <dt><</dt><dd>1オクターブ下げる
</dd>
  <dt>></dt><dd>1オクターブ上げる
</dd>
  <dt>qx</dt><dd>ゲート長(音符の長さに対する発音時間の長さ)をx/8に変更。(xは1以上8以下)
</dd>
  <dt>lx</dt><dd>デフォルト音長指定。xには数字、ピリオド、"^"(または「ー」)を付加して長さを指定。(xは省略不可)
</dd>
</dl>
初期値はo4 i0 q7 t120 L4となっています。 各命令と直後の引数のあいだに空白を入れることはできません。発音命令、休符命令以外の命令の引数はできるだけ省略しないで下さい。大文字小文字は区別しません。上記以外の命令や、有効範囲外の引数はすべて無視されますので、小節線として"|"を挿入したり、見易いようにカッコでくくったりしても構いません。


## 独自拡張文法

[MelodyEditor](/MelodyEditor)との互換性を保つため、音長に13,23など3でおわる数字を与えた場合に限り、3連符として演奏します。例えばc163はc音の163分音符ではなく、c音の8分音符を3等分した長さ(つまり24分音符)となります。通常13連符や23連符はまず出現しないので、問題ないと思いますが注意して下さい。



version 0.5から[ストトン表記](/ストトン表記) に一部対応しました。「L8レッレレレソミレーッミッミッ」 と書くこともできるようになりました。また[ストトン表記](/ストトン表記)をMMLpack DDに渡す とMMLに変換してくれます。(上の例だとL8drdddged^rererになるはず)


## さいごに

このプログラムは、JFileなどのデータベースに、音楽を書きこむために作成しましたが、他にもいろいろ使いみちがあると思います。 改良要望、ソースを見たい、あるいはバグなどありましたら[matto](/matto)までお尋ね下さい。



MMLをSMFに変換する部分は独立したソースにしてあります。音をならしたいけ どMIDIを直接吐くプログラムをかくのは大変、という場合にご利用下さい。曲 が長い場合はMMLの方がメモリを食わないはずです。



それにしても、PalmOSが音楽[API](/API)にSMF形式を選んだ点は、「おっ」っと思わせ るものがあります。独自フォーマットを選ばず、一番ユニバーサルなフォーマットを採用したところに開発者のセンスを感じます。


## 変更履歴

<dl>
  <dt>0.9</dt><dd>二重起動を防ぐためのコードを追加、PalmOS5 SDKに対応
</dd>
  <dt>Version 0.8</dt><dd>regmmldaで曲の末尾が切れるバグを修正。
</dd>
  <dt>Version 0.7</dt><dd>初歩的なバグを見付けてもらいました。感謝!
</dd>
  <dt>Version 0.6</dt><dd>主にソースの整理を行った。
</dd>
  <dt>Version 0.5</dt><dd>[ストトン表記](/ストトン表記)法 に一部対応。全角カタカナ「ドレミファソラシドッンー」が使えます。
</dd>
  <dt>-</dt><dd>音長指定で数字を省略した場合にデフォルト長さが採用されるようにした。こ れまで、l4c^という表記では最後の^は無視していたが、c4^4=c2のように演奏され るようになった。
</dd>
  <dt>-</dt><dd>MMLpack DDで"i"を解釈するようにした。一旦打ちこんだ曲全体の移調をした い場合は、先頭に"i"コマンドを付加してからMMLpack DDに渡すだけですむ。
</dd>
  <dt>Version 0.4</dt><dd>細かい修正、日本語対応など。
</dd>
  <dt>Version 0.3</dt><dd>DA版では、選択反転表示領域があればその部分を優先して演 奏、なければClipboardの内容を演奏。DD版は変更なし。
</dd>
  <dt>Version 0.2</dt><dd>[MelodyEditor](/MelodyEditor)互換
</dd>
  <dt>Version 0.1</dt><dd>初期バージョン。DDとDA版を提供。
</dd>
</dl>






## Linked from

* [MML DA](/MML DA)
* [MelodyEditor](/MelodyEditor)
* [ストトン表記](/ストトン表記)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/MML DA.md)

