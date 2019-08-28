#!/usr/bin/env perl

use strict;
use encoding "utf8";

my %frag;

my $wordlen = $ARGV[0] || 2;

while(<STDIN>){
    chomp;
    split;
    my $kami = $_[0].$_[1].$_[2];
    my $simo = $_[3].$_[4];
    my @chars = split(//, $kami);
    my $len = length($kami);
    for(my $j=0; $j<=$len - $wordlen; $j++){
	my $sub = substr( $kami, $j, $wordlen );
	if ( ! defined $frag{$sub} ){
	    $frag{$sub} = $simo;
	}
	else{
	    $frag{$sub} ++;
	}
    }
}

foreach my $key ( keys %frag ){
    if ( $frag{$key} == 0 ){
	print "$key $frag{$key}\n";
	#print " $key\n";
    }
}
