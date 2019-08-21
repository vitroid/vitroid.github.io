#Datatypes
A datatype to list all the subgraphs of a kind in a given large graph. Suffix ".frag" is recommended.
## Format
|Value|Type|Description
|-----|-----|-----
|@FRAG| string| 5-letter tag
|m n |a pair of integers separated by space|m: number of vertices in the fragment graph. n: number of vertices in the large graph.
|-----|-----|-----
|a1 a2 a3 ... am|m integers separated by spaces|Label of vertices in the large graph. Label order must correspond to that in the subgraph.
|...|(repeat)|
|-----|-----|-----
|-1 -1 -1 ... |m integers separated by spaces|Terminator.
```
@FRAG
m n
a1 a2 a3 a4 ... am
a1 a2 a3 a4 ... am
a1 a2 a3 a4 ... am
....（arbitrary number of lines）
-1 -1 -1 -1 .... -1 (repeat m times)
```
## Example
Two subgraphs of 12 vertices in a large 512-vertex graph.
```
@FRAG
12 512
12 74 189 253 433 491 420 351 279 35 488 171 
329 194 475 84 457 21 151 407 366 445 138 146 
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 
```
----


