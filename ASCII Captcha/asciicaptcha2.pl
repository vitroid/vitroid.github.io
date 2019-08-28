#!/usr/bin/env perl

#
#GPL
#

use strict;
use Font::BDF::Reader;
#use Data::Dumper;

my %bits = (
    '0'=>[ 0,0,0,0 ],
    '1'=>[ 0,0,0,1 ],
    '2'=>[ 0,0,1,0 ],
    '3'=>[ 0,0,1,1 ],
    '4'=>[ 0,1,0,0 ],
    '5'=>[ 0,1,0,1 ],
    '6'=>[ 0,1,1,0 ],
    '7'=>[ 0,1,1,1 ],
    '8'=>[ 1,0,0,0 ],
    '9'=>[ 1,0,0,1 ],
    'A'=>[ 1,0,1,0 ],
    'B'=>[ 1,0,1,1 ],
    'C'=>[ 1,1,0,0 ],
    'D'=>[ 1,1,0,1 ],
    'E'=>[ 1,1,1,0 ],
    'F'=>[ 1,1,1,1 ],
);


my @lightletters = ( ',', '.', ' ', '`' );
my @heavyletters = ( '#', 'W', 'G', '@' );


# See http://search.cpan.org/~dclee/Font-BDF-Reader-0.01/Reader.pm
my $BDF = Font::BDF::Reader->new( "helvR14.bdf" );

my @encs         = $BDF->get_all_ENCODING;

#my ( $banner, $answer ) = asciicaptcha1();
my ( $banner, $answer ) = asciicaptcha2();

print $banner;
print $answer, "\n";


sub asciicaptcha1{
    my $v1 = int rand 10;
    my $v2 = int rand 10;
    my $answer = $v1 * $v2;
    my $string = $v1 . "x" . $v2 . "=?";

    my ( $width, @pos ) = letters( $string, 2 );
    my $banner = toBanner( $width, @pos );
    ( $banner, $answer );
}



sub asciicaptcha2{
    my @chars = ( 'a' .. 'z' );
    my $v1 = $chars[ int rand 26 ];
    my $v2 = $chars[ int rand 26 ];
    my $v3 = $chars[ int rand 26 ];
    my $v4 = $chars[ int rand 26 ];
    my $v5 = $chars[ int rand 26 ];
    my $answer = $v1.$v2.$v3.$v4.$v5;
    my $string = $answer;

    my ( $width, @pos ) = letters( $string, 2 );
    my $banner = toBanner( $width, @pos );
    ( $banner, $answer );
}



sub toBanner{
    my ( $width, @pos ) = @_;
    my @map;
    my ( $columns, $rows, $xoffset, $yoffset ) = 
	split /\s+/, $BDF->{METADATA}{FONTBOUNDINGBOX};
    foreach my $xy ( @pos ){
	my $x = $xy->[0] - $xoffset;
	my $y = $xy->[1] - $yoffset;
	$map[$y][$x] = 1;
    }

    my $lines;
    for(my $y=$rows-1; $y>=0;$y-- ){
	for(my $x=0; $x<=$width - $xoffset; $x++){
	    $lines .= pix($map[$y][$x]);
	    $lines .= pix($map[$y][$x]);
	}
	$lines .= "\n";
    }
    $lines;
}



sub pix{
    my ( $v ) = @_;
    if ( $v ){
	$heavyletters[ rand( $#heavyletters + 1 ) ];
    }
    else{
	if ( rand() < 0.05 ){
	    $heavyletters[ rand( $#heavyletters + 1 ) ];
	}
	else{
	    $lightletters[ rand( $#lightletters + 1 ) ];
	}
    }
}




    
sub letters{
    my ( $string, $fluc ) = @_;
    my $xoffset = 0;
    my @pos;
    
    foreach my $letter ( split //, $string ){
	my ( $width, @p ) = letter( $letter, $fluc );
	foreach my $xy ( @p ){
	    $xy->[0] +=  $xoffset;
	    push @pos, $xy;
	}
	$xoffset += $width;
    }
    ( $xoffset, @pos );
}


#
#文字のピクセルの座標の対リストと文字幅を、各文字の原点からの座標系で返す。
#
sub letter{
    my ( $code, $fluc ) = @_;
    $code = ord( $code );
    my $char = $BDF->get_font_info_by_ENCODING( $code );

    my $width = $char->{DWIDTH}[0];
    my $firstline = $char->{BBX}[1] + $char->{BBX}[3] + int(rand($fluc*2+1)-$fluc);
    my $lines     = $char->{BBX}[1];
    my $xoffset   = $char->{BBX}[2];


    my @pos;
    foreach my $y ( 0 .. $lines - 1 ){
	my $line = $char->{BITMAP}[$y];
	my @chars = split //, $line;
	my @bits;
	foreach my $letter ( @chars ){
	    push @bits, @{$bits{$letter}};
	}
	for(my $x=0; $x<=$#bits; $x++){
	    if ( $bits[$x] ){
		push @pos, [ $x + $xoffset, $firstline - $y ];
	    }
	}
    }
    ( $width, @pos );
}
