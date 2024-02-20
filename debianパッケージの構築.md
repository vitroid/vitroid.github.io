---
title: debianパッケージの構築
---
[unix](/unix)


## [debianパッケージの構築](/debianパッケージの構築)

覚え書き。元ネタは[http://park15.wakwak.com/~unixlife/linux/de-deb.html](http://park15.wakwak.com/~unixlife/linux/de-deb.html)

```
% mkdir ~/deb
% cd ~/deb
% mkdir yaplot-3.3
% cd yaplot-3.3
% dh_make -e matto@chem.nagoya-u.ac.jp -f SOMEWHERE/yaplot-3.3.tar.gz
Type of package: single binary, multiple binary, library, or kernel module?
 [s/m/l/k] s

Maintainer name : Masakazu MATSUMOTO
Email-Address   : matto@chem.nagoya-u.ac.jp 
Date            : Tue,  3 Aug 2004 14:28:32 +0900
Package Name    : yaplot
Version         : 3.3
Type of Package : Single
Hit <enter> to confirm: 
Done. Please edit the files in the debian/ subdirectory now. yaplot
uses a configure script, so you probably don't have to edit the Makefiles.
% cd debian
% edit copyright, control
% cd ~/deb/yaplot-3.3
% dpkg-buildpackage -rfakeroot 
```





## Contents of control

```
Source: yaplot
Section: main
Priority: optional
Maintainer: Masakazu MATSUMOTO <matto@chem.nagoya-u.ac.jp>
Build-Depends: debhelper (>= 4.0.0)
Standards-Version: 3.6.0

Package: yaplot
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}
Description: Yet another plotter in 3-D.
     Yaplot is an easy 3D modeller and animator
     for visualizing the results from computer
     simulation easily.
     You can browse the motion of the 3 dimentional wire frame model
     with text labels and
     some marks on the cheap PC based X terminals.
     Data format is simple and intuitive.
     It is the least beautiful and not durable for presentation, but
     quick and smooth enough for daily use.
```

## Contents of copyright

```
This package was debianized by Masakazu MATSUMOTO <matto@chem.nagoya-u.ac.jp> on
Tue,  3 Aug 2004 14:28:32 +0900.

It was downloaded from http://www.chem.nagoya-u.ac.jp/og/wiki/wiki.cgi/matto?page=yaplot+%28en%29

Upstream Author(s): Masakazu MATSUMOTO <matto@chem.nagoya-u.ac.jp>

Copyright (C) 1989, 1991 Free Software Foundation, Inc.

You are free to distribute this software under the terms of the GNU General Public License.
On Debian systems, the complete text of the GNU General Public License can be found in the file `/usr/share/common-licenses/GPL'.
```




## Linked from

* [debianパッケージの構築](/debianパッケージの構築)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/debianパッケージの構築.md)

