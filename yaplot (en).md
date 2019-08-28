---
title: yaplot (en)
---
[unix#software](/unix#software)

[research](/research)


# Yaplot -- yet another plot in 3-D

-->Japanese page

![yaplot](perc.gif)

Sample image of yaplot. 

(Visualization of 3-dimensional bond percolation.)

* [yaplot](yaplot3.3.20040803.tar.gz) Source codes(2004-08-03)
* [yaplot](yaplot-3.3-1.i386.rpm) Binary package for Vine Linux(2004-08-03)
* [yaplot](yaplot_3.3-1_i386.deb) Binary package for Debian Linux(2004-08-03)

## What is yaplot?




### Features

* Simple animation, simple control.
* Simple data format.
Yaplot is an easy 3D modeller and animator  for visualizing the results of computer simulation.

You can browse the motion of the 3 dimentional wire frame model  with text labels and  some marks on the cheap PC based X terminals.

Data format is simple and intuitive.

It can also open and render several files in windows at a time.

It is useful to watch spaciotemporal data.

It is the least beautiful and not durable for presentation, but  enough quick and smooth for daily use.  (Do not expect much to yaplot!)


## Installation

Yaplot requires gtk.



First, get the source code and expand. On linux, compile them with the following commands.

```
           prompt% ./configure
           prompt% make
```
If configure fails even when gtk is installed correctly, try the following.

```
           prompt% aclocal
           prompt% autoconf
           prompt% ./configure
           prompt% make
```
When it is compiled successfully, install them to the appropriate places.

```
           prompt# make install
```
On windows, edit Makefile.dos and try "make". Some features of yaplot are missing on Windows.




## Usage



```
     usage : yaplot [options] infile [infile ...]
       -e x,y,z        Set the coordinate of the eye point.
       -l x,y,z        Set the coordinate of the look point.
       -u x,y,z        Set the up-vector.
       -c filename     Specify palette file.
       -q n            Specify n frames are cached in memory.(default=1)
       -d              Debug mode.
       infile          Yaplot command file.
```
Currently all options are unavailable on DOS.



Yaplot has the concept of layers. It has 12 layers by default. You can show/hide each layer by function keys.



When "-" is specified as the command file name, commands are read from standard input.



When multiple command files are specified, they are rendered in different windows. There are two modes of control, which are synchronous mode and asynchronous mode. When the mouse focuses to a windows in synchronous mode, your control (with mouse or keyboard) are reflected to all other windows. In asynchronous mode, on the other hand, your control are reflected only to the window where mouse is focusing.



You can alter modes by "s" key. All the windows are in synchronous mode by default.



If no command file is specified, help file is displayed.



By specifying "RECORD" option in Makefile, recording feature becomes available. When "r" key is pressed, hardcopies of the windows are saved in yaplotxx_yyyyy.gif(xx is window No.、yyyyy is frame No.) To stop recording, press "r" again.



If  "u" is pressed, current view information (eye position, field of view, etc.) is saved in ".yapviewstack" file of the current directory. If "o" is pressed, last view information is recovered from ".yapviewstack" file. It is useful to share the view information on multiple yaplot. (This feature is not available on DOS)



When no palette file is specified, yaplot searches the palette file in the following order:

1. yaplot.col file in current directory.
1. the file specified in YAPLOTCOL environment variable.
1. yaplot.col file in your home directory.
1. System default palette file.


Several sample command files are included in source code package.


## User interface

You can control yaplot by mouse and keys.



Key assignments are listed below.

Commands marked with "!" mark are "repeatable commands". Pressing number keys before repeatble command key makes the same effect as pressing the command key repeatedly. For example, pressing  "5" "N" is the same as pressing "NNNNN" (animate in 5fps).

When you mistype the number, press ESC key to escape.

All the repeatable commands ( except "g" and "f" ) are relative, i.e., pressing "10N5P" is the same as "5N".



<dl>
  <dt>Up and down arrow, or "j" and "k"</dt><dd>Pitching rotation.
</dd>
  <dt>Left and right arrow, or "h" and "l"</dt><dd>Heading rotation.
</dd>
  <dt>Mouse drag with left button</dt><dd>Rotate immediately
</dd>
  <dt>Pause or "!"</dt><dd>Stop automatic rotation.
</dd>
  <dt>Tab</dt><dd>Undo rotation.
</dd>
  <dt>"*" and "/"</dt><dd>Scale up and down
</dd>
  <dt>"[" and "](" and ")"</dt><dd>Zoom in and out
</dd>
  <dt>"r"</dt><dd>Start/stop recording.
</dd>
  <dt>"u"</dt><dd>pUsh; Push current view information in the view stack.
</dd>
  <dt>"o"</dt><dd>pOp; Pop current view information from the view stack.
</dd>
  <dt>PageDown or "n"</dt><dd>Next frame.
</dd>
  <dt>PageUp or "p"</dt><dd>Previous frame.
</dd>
  <dt>Numeric keys followed by PageDown or "n" with shift</dt><dd> Prograde animation. 
</dd>
  <dt>Numeric keys followed by PageUp or "p" with shift</dt><dd>Retrograde animation.
</dd>
  <dt>Numeric keys followed by "g" or Enter</dt><dd>Jump to the frame specified by numeric keys. Single "g" to the first frame, single "G" to the last frame.
</dd>
  <dt>SPACE</dt><dd>Stop all automatic actions(Rotation and animation)
</dd>
  <dt>"+" and "-"</dt><dd>Change rendering fidelity.
</dd>
  <dt>Insert and Delete, or "(" and ")"</dt><dd>Gradate line thickness.
</dd>
  <dt>Function keys, or numeric keys followed by "F"</dt><dd>Toggle show/hide of the layer.
</dd>
  <dt>"v"</dt><dd>Change verbosity.
</dd>
  <dt>"s"</dt><dd>Toggle synchronous/asynchronous modes.
</dd>
  <dt>"q" or Break</dt><dd>Quit yaplot.
</dd>
</dl>

## Command file format

One line of the command files corresponds to one command. A command consists of a single command character followed by parameters separated by at least one space character, Any parameters are not omittable.

<dl>
  <dt>r {radius}</dt><dd>Specify the radius of circles, rings, and sticks.
</dd>
  <dt>l {x} {y} {z} {x} {y} {z}</dt><dd>Draw a line.
</dd>
  <dt>s {x} {y} {z} {x} {y} {z}</dt><dd>Draw a stick,
</dd>
  <dt>p {n} {x} {y} {z} {x} {y} {z} {x} {y} {z} ...</dt><dd>Draw a polygon
</dd>
  <dt>c {x} {y} {z}</dt><dd>Draw a circle.
</dd>
  <dt>o {x} {y} {z}</dt><dd>Draw a ring sign.
</dd>
  <dt>3 {x} {y} {z}</dt><dd>Draw a triangle sign.
</dd>
  <dt>4 {x} {y} {z}</dt><dd>Draw a square sign.
</dd>
  <dt>5 {x} {y} {z}</dt><dd>Draw a pentagon sign.
</dd>
  <dt>6 {x} {y} {z}</dt><dd>Draw a hexagon sign.
</dd>
  <dt>t {x} {y} {z} {text....}</dt><dd>Draw a string.
</dd>
  <dt>@ {n}</dt><dd>Specify palette No. (Palette colors are specified in palette file.)
</dd>
  <dt>@ {n} {r} {g} {b}</dt><dd>Specify color of the n'th palette. r,g,b are integer between 0 to 255.
</dd>
  <dt># {comment}</dt><dd>Comment. (Ignored.)
</dd>
  <dt>y {layer}</dt><dd>Change current layer(default layer=1)
</dd>
  <dt>Empty line</dt><dd>End of a frame.
</dd>
</dl>

## Palette file format

Each line of the palette file specifies the Red, Green and Blue  intensity of the pallete. First line describes the color for  palette 0. As the palettes 0 to 2 are reserved for system color  (Black, Gray, and White), you should not modify them.


## Internal behavior

<!-- yaplotは、ファイル読み込み時に、ハッシュ表を用いてコマンドファイ  ルで指定された座標が縮退しているかどうかを調べ、同一の座標の座標  変換計算を減らしています。このため、読みこみに少々余分な時間がか  かりますが、ユーザは座標が縮退しているかどうかを心配する必要はあ  りません。 -->


<!-- キャッシュ戦略にはLRUを使用していますが、先読みは行っていません。  このため、単に順方向/逆方向にアニメーション表示する場合にはあま  りキャッシュは有効に働きません。すべてのフレームを読みこめるぐら  い大きくキャッシュをとる場合、あるいは特定部分のみ繰り返し再生す  るようなケースではキャッシュが有効に機能します。 -->

## Related materials

* [MDView](http://www.chem.nagoya-u.ac.jp/bar/mdview/index.html) Molecular Dynamics Viewer.




----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/yaplot (en).md)

