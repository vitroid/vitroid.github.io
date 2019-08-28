#web service

#多面体構造

#vitrite

#water


# Vitrite ( Network Motif of Water ) Database


## URL

http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi


## What is it?

Vitrite ("非晶子" in Chinese and Japanese) is the typical [network motif of water](/Network Motif of Water) at low temperature. It is defined as a graph satisfying the following conditions:

1. Each vertex must be 2- or 3-connected.
1. Each edge must be shared by two rings.
1. Consists of 3- to 8-membered rings.
1. Must satisfy the following Euler's formula for planar graph:
F - E + V = 2

where F, E, V are number of rings, edges, and vertices, respectively.



Note that not all the graphs in this database satisfy these conditions. Volume and topological volume are not shown for the graph not satisfying the conditions.



Almost all the vitrite found in low density amorphous ice is recorded in the database. It is also planned to import new vitrites into the database when it is queried.


## How to get a graph in XML.

Here is a sample URL to get a graph and its topological/geometrical attributes in XML:

* [Sample Query](http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?id=39&form=xml&field=ringset,shape)
```
vitrite.cgi?id=39&form=xml&field=ringset,shape
```
The parameter 'id' specifies the graph ID in the database. You can specify multiple attributes for 'field' parameter in comma-separated format. Currently you can specify the following fields:

* spectrum
* solid
* volume
* ringset
* crystalviewer
* isvitrite
* image
* symmetry
* ringcount
* eulerindex
* topovolume
* shape
* graph
* rd
Note that 'graph' is mandatory.

You can also search by exact graph matching. Graph topology is specified in simple notation. Here is an example query for vitrite #8.

* [Sample Query](http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?simple=A-B-C-D-E-F-A,C-G-H-F&form=xml&field=ringset)
```
vitrite.cgi?simple=A-B-C-D-E-F-A,C-G-H-F&form=xml&field=ringset
```



## How to get the results by narrowing search in XML.

To get a set of graphs satisfying a couple of conditions at a time, a sample URL is following:

* [Sample Query](http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?form=xml&field=graph,isvitrite&key1=id&op1=in&val1=3,5,7-9&key2=isvitrite&op2=eq&val2=0)
```
vitrite.cgi?form=xml&field=graph,isvitrite&key1=id&op1=in&val1=3,5,7-9&key2=isvitrite&op2=eq&val2=0
```
Number of query results can be limited by keywords 'sta'(starts) and 'rec'(records). If you need only the first 50 records out of 1000 query results, add 'sta=0&rec=50' to the URL. if you want the second 50 records, it becomes 'sta=50&rec=50'. If rec is unspecified, number of query results is limited to 1000 for fail-safe. See the following sample queries.

* [Sample Query 1 (first 10 matches)](http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?form=xml&field=isvitrite&key1=isvitrite&op1=eq&val1=0&sta=0&rec=10)
```
vitrite.cgi?form=xml&field=isvitrite&key1=isvitrite&op1=eq&val1=0&sta=0&rec=10
```
* [Sample Query 2 (second 9 matches)](http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?form=xml&field=isvitrite&key1=isvitrite&op1=eq&val1=0&sta=10&rec=9)
```
vitrite.cgi?form=xml&field=isvitrite&key1=isvitrite&op1=eq&val1=0&sta=10&rec=9
```
A condition is given by parameters key1, op1, and val1, specifying the field name, comparison operator, and the (threshold) value, respectively. Currently you can specify the following fields.

|field|explanation |
|-----|-----|
|id|Graph ID |
|volume|Volume* |
|solid|Total solid angle* of the vertices cropped by the polyhedron in 4 pi steradian. It indicates the actual number of atoms contained in the polyhedron. |
|isvitrite|Is a vitrite?(0=yes) |
|symmetry|Symmetry Number |
|ring3|3-ring |
|ring4|4-ring |
|ring5|5-ring |
|ring6|6-ring |
|ring7|7-ring |
|ring8|8-ring |
|topo0|Euler Index |
|topo1|Number of Rings |
|topo2|Number of Edges |
|topo3|Number of Vertices |
|topovolume|Topological Volume |
|rd|Residual Distortion* |
Note that '*' indicates the value is not exact (i.e. not a topological index).

Available operators are also listed.

|operator|explanation |
|-----|-----|
|lt|< value |
|gt|> value |
|eq|== value |
|ne|!= value |
|in|in ranges |

## XML

You can write some convenient tools by yourself to access the vitrite DB.

<dl>
  <dt>To get perl library in CPAN</dt><dd>http://www.cpan.org/misc/cpan-faq.html#How_install_Perl_modules
</dd>
  <dt>To parse XML by perl</dt><dd>http://search.cpan.org/dist/XML-Parser-EasyTree/EasyTree.pm
</dd>
  <dt>To dump the content of perl hash</dt><dd>http://search.cpan.org/~ilyam/Data-Dumper-2.121/Dumper.pm
</dd>
</dl>

### A sample code to convert the result XML into a simple table

* preparation
```
# perl -MCPAN -e 'install XML::Parser::EasyTree'
# perl -MCPAN -e 'install Data::Dumper'
```
* source code in perl
```
#!/usr/bin/env perl
use strict;
use XML::Parser;
use XML::Parser::EasyTree;
use Data::Dumper;

#initialize XML Parser
$XML::Parser::EasyTree::Noempty=1;
my $p=new XML::Parser(Style=>'EasyTree');

#input the string from STDIN to $xml.
#For example,
#curl 'http://vitrite.chem.okayama-u.ac.jp/cgi-bin/vitrite.cgi?form=xml&field=isvitrite&key1=isvitrite&op1=eq&val1=0&sta=0&rec=10' | dumpvitritedb.pl
my $xml = join("", <STDIN>);
my $tree=$p->parse($xml);

#Peek the contents
print STDERR Dumper($tree);

if ( $tree->[0]{name} eq 'vitrites' ){
    foreach my $element ( @{$tree->[0]{content}} ){
	print table1( $element );
    }
}
elsif ( $tree->[0]{name} eq 'vitrite' ){
    print table1( $tree->[0] );
}



sub table1{
    my ( $element ) = @_;
    my $id = $element->{attrib}{id};
    my $text;
    $text .= "id $id ";
    foreach my $field ( @{$element->{content}} ){
	my $label = $field->{name};
	my $value = $field->{content}[0]{content};
	$text .= "$label $value ";
    }
    $text .= "\n";
    return $text;
}
```



## ChangeLog

<dl>
  <dt>2014-12-25</dt><dd>Moved to a new server.
</dd>
  <dt>2008-12-03</dt><dd>"Solid", i.e. solid angle of the vertices is added to the field list. Now you can estimate the number density of one fragment.
</dd>
  <dt>2007-11-29</dt><dd>Index was missing to id field of the database, which was the reason why DB access is so slow. Fixed. [Simple notation](/simple notation) is introduced for topological search query.
</dd>
  <dt>2007-11-27</dt><dd>The algorithm of shape module, which estimates the most unstrained geometry, is improved. 
</dd>
</dl>


