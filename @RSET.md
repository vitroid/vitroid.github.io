---
title: @RSET
---
[Datatypes](/Datatypes)


## [@RSET](/@RSET) - Set of rings

Specifies a set of rings (cyclic paths) in the graph. Label of rings should be specified in [@RNGS](/@RNGS) format in a separate file.

|Data|Type|Description |
|-----|-----|-----|
|[@RSET](/@RSET)|5 fixed characters|An identifier tag |
|N|integer|Number of rings in the graph |
|n a1 a2 a3 ... an|A list of integers separated by spaces.|Number of rings and list of ring labels. |
|...|(repeat)| |
|0|one fixed character|Terminator |

## Example

Cubic graph is described in [@NGPH](/@NGPH) format:

```
@NGPH
8
0 1
1 2
2 3
3 0
0 4
1 5
2 6
3 7
4 5
5 6
6 7
7 4
-1 -1
```
It has six tetragonal rings described in [@RNGS](/@RNGS) format:

```
@RNGS
8
4 3 7 6 2
4 3 7 4 0
4 0 3 2 1
4 2 6 5 1
4 4 7 6 5
4 1 5 4 0
0
```
And it has one cubic graph in itself, described in [@RSET](/@RSET) format:

```
@RSET
6
6 0 1 4 2 3 5
0
```

## See also

* [@NGPH](/@NGPH)
* [@RNGS](/@RNGS)
* [@FRAG](/@FRAG)


## Linked from

* [@RNGS](/@RNGS)
* [@RSET](/@RSET)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/@RSET.md)
