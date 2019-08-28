#!/usr/bin/env perl
#
#新着チャンネルのみをリストするCGI
#NewsClip APIの使用例
#

use strict;
use LWP::Simple;
use CGI;

my $q = new CGI;

my @Categories=(" すべて"," 未分類","期間限定","巡回停止","その他","",
		"非公開"," オフィシャル","","","携帯端末",
		"コラム/エッセィ","ニュース(技術系)","新聞/ニュース",
		"乗り物","Mac","スポーツ","天気","定点観測","レビュー",
		"政治経済","Unix/Internet","映画とゲーム","掲示板",
		"音楽芸術","語学");
my $newer  = time - 24*3600;
my $output = (1<<0) + (1<<8) + (1<<9) + (1<<12) + (1<<13) + (1<<20) + (1<<27);
my $NEWSCLIP = "http://newsclip.chem.nagoya-u.ac.jp";
my $BASEURL = "$NEWSCLIP/cgi-bin/newsclip.cgi";
my $URL = "$BASEURL?id=guest-guest-guest&Query=TAB&newer=$newer&output=$output";
my $table = get($URL);
print $q->header(-charset=>"Shift_JIS");
print $q->start_html(-title=>"新着チャンネル情報",
		     -lang =>"ja",
		     -head =>[
			      $q->meta({'http-equiv' => 'Content-Type',
				    -content=>"text/html; charset=Shift_JIS"})
			      ]
		     );
#print $table;
print $q->a( {-href=>"$NEWSCLIP/cgi-bin/palmbasket.cgi?c05931=1"},
	    $q->img( {-src=>"$NEWSCLIP/palmbasket/PalmBasket_small.png",
		      -alt=>"このページをPalm:Basketに入れる",
		      -border=>0 } ) );

my @lines = split( /\n/, $table );
foreach my $line ( @lines ){
    my ( $code, $title, $url, $owner, $comment, $category, $headline )
	= split(/\t/, $line );
    $code = $q->a( {-href=>"$BASEURL?Info=$code"}, $code );
    $url  = $q->a( {-href=>"$url"}, $url );
    
    print $q->h2( $code, expand( $title ) );
    print CategoryString( $q, $category );
    print expand( $comment ), $q->br;
    print $q->div( {-style=>"border-style: solid"}, expand( $headline ) );
}
print $q->end_html();


#
#カテゴリービットを、HTML装飾した文字列に変換する。
#
sub CategoryString{
    my ( $q, $category ) = @_;
    my $categorystring;

    for(my $i=1;$i<=$#Categories;$i++){
	if( getbit( $category, $i) ){
	    $categorystring .= $Categories[$i]." ";
	}
    }
    $q->div({-class=>"category"}, $categorystring);
}


sub getbit{
    my ( $value, $bit ) = @_;
    return ( ( $value & (1<<$bit) ) ? 1 : 0 );
}

sub expand{
    my ( $text ) = @_;
    $text =~ s/\\r/\r/g;
    $text =~ s/\\n/\n<br>/g;
    $text =~ s/\\t/\t/g;
    $text =~ s/\\0/\0/g;
    $text =~ s/\\\\/\\/g;
    $text;
}
