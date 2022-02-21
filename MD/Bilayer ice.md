# Bilayer ice

疎水性の2枚の壁に挟まれた、極めて狭い空間で生じる氷。上下層の水分子は完全に重なり、その間に水素結合が生じる。層内は3結合のネットワークとなる。

#GenIce を使い、Stone-Wales欠陥を20%導入することで、アモルファス化させた構造を生成した。

```
genice2 bilayer[size=15,18:sw=0.2] -f svg[shadow:rotatex=15:rotatey=10] > bilayer.svg
```

![bilayer ice](img:bilayerice.png)


## References

1. Slovák, J., Koga, K., Tanaka, H. & Zeng, X. C. Confined water in hydrophobic nanopores: dynamics of freezing into bilayer ice. Phys. Rev. E Stat. Phys. Plasmas Fluids Relat. Interdiscip. Topics 60, 5833–5840 (1999)
1. Koga, K., Zeng, X. C. & Tanaka, H. Freezing of confined water: A bilayer ice phase in hydrophobic nanopores. Phys. Rev. Lett. 79, 5262–5265 (1997)

#GenIce #ice #氷の多形 #water
