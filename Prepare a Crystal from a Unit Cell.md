---
title: Prepare a Crystal from a Unit Cell
---
[software](/software)

[analysis](/analysis)

[unitcell](/unitcell)

[unitrepeat](/unitrepeat)



In this document, the way how to make a bulk crystal structure which fits to periodic boundary condition from a unit cell is described. (English version will be provided soon.)


## unitcell - 格子の変換



シミュレ−ションで使用する初期構造に固体の結晶構造を使用する場合には、 一般には結晶学で与えられる単位格子をx,y,z方向に並べることで、より大き な結晶を作成します。この方法で周期境界条件下で、各結晶軸がシミュレ−ショ ンセルの各軸に平行になるような配置を作成するのは容易ですが、それ以外の 場合(斜方晶(各軸の長さは異なるが互いに直交する結晶系)のシミュレ−ショ ンセルに対して、結晶軸を傾けて埋めこむ場合、あるいは単位格子が三斜晶の 場合)は、試行錯誤でその角度と繰り返しの数を求めるのは非常に困難です。



このプログラムunitcellは、与えられた斜方晶の単位格子と、与えられた軸 (あるいは結晶面。通常3つの整数で表現される。ここではi軸と呼ぶ)にもとづ いて、適切な斜方晶のシミュレ−ションセルの大きさを決定し、残りの2つの 軸(それぞれj,k軸と呼ぶ)の方向を決定します。一般的には、残りの軸が厳密 に直交するように選べない場合が多いので、軸同士の内積の上限値(軸同士が 完全に直交すれば内積は0になる)を与えることによって、おおざっぱに直交条 件をみたす組合せが列挙されます。



標準出力に出力されるデータは、第1カラムがシミュレ−ションセル内に含まれる単位格 子の数(整数)、第2カラムが計算された3軸の内積の直交度(3軸がなす菱面体の 体積を、3軸の長さの積でわったもの。完全な直方体の場合は1、ひずみが大き くなるほど小さな値になる。)、第3、4、5カラムがi軸の方向、6、7、 8カラムはj軸の方向、第9、10、11カラムがk軸の方向を表します。




### 使い方の例



Ice Icの単位格子は8個の水分子を含む立方体です。Ice Icの[111](111)面からの結 晶の成長を見るためには、[111](111)面をシミュレ−ションセルのz軸に向け、x,y 軸に周期境界を与えることにします。x、y軸の方向の候補は





```
unitcell 1 1 1 1 1 1 | sort -n | less
```


とすると得られます。引数の最初の3つは単位格子の辺の長さが(1,1,1)である ということを指示し、あとの3つはi軸を[111](111)方向にとることを指示していま す。これから、次のような結果が得られます。





```
6 1.000000 1 1 1 -1 0 1 -1 2 -1
```


単位格子6個分の新しいシミュレ−ションセル(辺の方向はもとの単位格子の [1 1 1](1 1 1)[-1 0 1](-1 0 1)[-1 2 -1](-1 2 -1)方向。ここでの表記[ijk](ijk)の意味は、単位格子の辺 の長さをそれぞれlx,ly,lzとした時に、(i*lx,j*ly,k*lz)という成分をもつベ クトルを表す。)がなかなか良い候補のようです。第2カラムの値が1であると いうことから、新しいセルの形状は完全な直方体であることがわかります。




## 氷の単位格子の生成

iceIcunit.plとiceIhunit.plは、[氷I](/氷I)cとIhの単位格子を生成します。

```
perl iceIcunit.pl
```
で8つの分子の重心位置を含み、密度1.0g/cm3の単位格子の座標が出力されます。その際、酸素酸素間距離が画面に出力されます。

```
2.68766137290804 O-O length
```


引数に密度を指定すると、その密度の格子を出力します。

```
perl iceIcunit.pl 3.7363
2.68766137290804 O-O length
```
密度に3.7363を指定すると、[氷I](/氷I)cの場合、分子の位置がちょうど整数になります。searchで使用する格子を生成する場合に便利です。


## unitrepeat



unitrepeatは、単位格子の座標を読み込んで、unitcellで求めたijkベクトルを 元に、実際の結晶構造、つまり各原子の座標位置を生成します。




### 使い方の例



unitcellで得られた情報を元に、単位格子をならべて大きな結晶格子を作って みましょう。Ice Icの単位格子には8分子しか含まれていませんから、この情 報をそのまま使うと単位格子6格子分では48分子しか含まない小さな格子しか できません。そこで、j軸方向に倍の大きさの格子を作らせることにします。 具体的な手順は次のようになります。





```
iceIcunit.pl | unitrepeat 1 1 1   -2 0 2  -1 2 -1 > outfile.ar3a
```


最初のiceIcunit.plコマンドが、単位格子の大きさ([@BOX3](/@BOX3)形式)と、8個のサイ トの位置を出力します。次に、unitrepeatコマンドが単位格子を12個並べて96 サイトを含む大きな格子を生成します。単位格子の並べ方は、unitcellコマン ドの出力をそのまま流用できますが、ここではunitcellの出力を、j軸方向に2 つ並べるために、jベクトルの値を2倍してあります。



できた配置を画面で確認したい場合はunitrepeatコマンドに-yオプションを付 けると、座標データがyaplotのデータ 形式で出力されます。



unitrepeatはあまり巨大な格子を作ることができません。単純にx軸方向にp倍、y軸方向にq倍、z軸方向にr倍したい場合はxxコマンドを使うこともできます。

```
iceIhunit.pl | xx 5 3 3 > outfile.ar3a
```


<!-- !氷の場合 -->
<!-- 得られた酸素位置に対して、水素結合を定義し、プロトンディスオーダ氷を作るには、[matto](/matto)/ProtonXferMCに含まれるpdiceを使ってください。 -->



## アルゴリズムについて



内部では、エラトステネスのふるいを3次元の格子に拡張したアルゴリズムを使 用しています。


## Program

[](http://theochem.chem.okayama-u.ac.jp/vitroid/Prepare a Crystal from a Unit Cell/unitcell.tar.gz)






## Comments and Suggestions

Please leave some messages if you felt it useful.

<!--  -->








## Linked from

* [Prepare a Crystal from a Unit Cell](/Prepare a Crystal from a Unit Cell)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Prepare a Crystal from a Unit Cell.md)

