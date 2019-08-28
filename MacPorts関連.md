---
title: MacPorts関連
---
[tips](/tips)

[mac](/mac)

<dl>
  <dt>variantsを調べる</dt><dd>[http://d.hatena.ne.jp/hakobe932/20061208/1165646618](http://d.hatena.ne.jp/hakobe932/20061208/1165646618)
</dd>
  <dt>pTeXの導入</dt><dd>[http://www.numericalfactor.org/wp/archives/203](http://www.numericalfactor.org/wp/archives/203)
</dd>
</dl>
```
a2ping is being used by the active teTeX port.  Please deactivate this port first, or use the -f flag to force the activation.
```
と言われた。[http://ohsawa-mac.blogspot.com/2006_06_01_archive.html](http://ohsawa-mac.blogspot.com/2006_06_01_archive.html) を参考に、

```
sudo port -d selfupdate
sudo port deactivate tetex
```
をして再挑戦。







----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/MacPorts関連.md)
