#!/usr/bin/env perl

use strict;
use CGI;
use CGI::Session;
use Data::ICal;
use Data::ICal::Entry::Event;
use Date::ICal;

use encoding "utf8";

my $myurl = "ta+ical.cgi";
my $webcalurl = "webcal://www2.chem.nagoya-u.ac.jp/theochem/matto/$myurl";

my $cgi = CGI->new();

# CGI::Sessionオブジェクトを生成（クッキーにセッションIDがセットされていれば前回の状態を復元）
my $id = $cgi->param( "CGISESSID" ) || $cgi->cookie( "CGISESSID" ) || undef;
my $session = CGI::Session->new("driver:File;serializer:Storable", $id, {Directory=>'/tmp'});
my $id = $session->id();
$cgi->param( "CGISESSID", $id );


my @colors = ( "black", "#ff0000", "#aa5500", "#55aa00", "#00ff00", "#00aa55", "#0055aa", "#0000ff", "#5500aa", "#aa0055" );
my @samples = ( "使途不明", "家事", "休憩・食事・睡眠", "身支度・入浴", "通勤・無駄時間", "雑務", "仕事段取", "仕事", "趣味", "その他" );

my $cgi = new CGI;

foreach my $i ( 0..9 ){
    $cgi->param( "text$i" ) || $cgi->param( "text$i", $samples[$i] );
}


if ( defined $cgi->param( "kind" ) ){
    my $kind = $cgi->param( "kind" );
    Record( $cgi->param("from.hour"), $cgi->param("from.min"),
	    $kind, $cgi->param( "text$kind" ), $session );
}
if ( defined $cgi->param( "direct" ) ){
    my $kind = $session->param( "dic" . $cgi->param( "direct" ) );
    Record( $cgi->param("from.hour"), $cgi->param("from.min"),
	    $kind, $cgi->param( "direct" ), $session );
}
if ( defined $cgi->param( "undo" ) ){
  my $time = LastAccess( $session );
  $session->clear( $time );
}
if ( defined $cgi->param( "icall" ) ){

    print WriteICal( $cgi, $session );
    $session->close;
    exit 0;
}
if ( defined $cgi->param( "rdfical" ) ){

    print WriteRDFical( $cgi, $session );
    $session->close;
    exit 0;
}

#
#UIはシンプルに、i-modeでも使えるように。
#
print Header( $cgi, "TimeAccount", $session );
print Dialog( $cgi, $session, GetHistory( $session ) );
print ShowHistory( $cgi );
print Footer( $cgi );
$session->close;
exit 0;



sub WriteICal{
    my ( $cgi, $session ) = @_;
    my @category;
    foreach my $cat ( $cgi->param( "ikind" ) ){
	$category[$cat+0] = 1;
    }
    use Data::ICal;

    my $calendar = Data::ICal->new();

    my $hashref = $session->param_hashref();
    my @history = (sort {$b<=>$a} ( keys %{$hashref} ));
    my $now = time;
    my $histlen = $cgi->param( "histlen" ) || 1;
    $histlen *= 24 * 3600;
    foreach my $endtime ( @history ){
	#
	#一週間以内のアカウントを抽出。
	#
	if ( $now - $histlen < $endtime ){
	    my ( $starttime, $kind, $description ) = @{$session->param( $endtime )};
	    next unless $category[$kind];
	    my $vevent = Data::ICal::Entry::Event->new();
	    $vevent->add_properties(
		summary => $description,
		dtstart   => Date::ICal->new( epoch => $starttime )->ical,
		dtend     => Date::ICal->new( epoch => $endtime )->ical,
		);
	    $calendar->add_entry( $vevent );
	    #
	    #update downloaded time
	    #
	    $session->param( $endtime, [ $starttime, $kind, $description ] );
	}
    }
    my $output;
    $output .= "Content-type: text/calendar\n";
    $output .= "Content-Disposition: attachment; filename=ta.ics\n\n";
    $output .= $calendar->as_string;
    $output;
}




sub WriteRDFical{
    my ( $cgi, $session ) = @_;
    my @category;
    foreach my $cat ( $cgi->param( "ikind" ) ){
	$category[$cat+0] = 1;
    }
    use DateTime::Format::W3CDTF;
    use DateTime;
    use XML::Generator;

    my $w3cdtf = DateTime::Format::W3CDTF->new;
    my $gen    = new XML::Generator;
    
    my $hashref = $session->param_hashref();
    my @history = (sort {$b<=>$a} ( keys %{$hashref} ));
    my $now = time;
    my $histlen = $cgi->param( "histlen" ) || 7;
    $histlen *= 24 * 3600;

    my $html;
    $html .= $gen->prodid( "-//chem.nagoya-u.ac.jp//TimeAccount 1.0//EN" );
    $html .= $gen->version( "2.0" );
    foreach my $endtime ( @history ){
	if ( $now - $histlen < $endtime ){
	    my ( $starttime, $kind, $description ) = @{$session->param( $endtime )};
	    $html .= $gen->component(
		$gen->Vevent(
		    $gen->dtstart( $w3cdtf->format_datetime( DateTime->from_epoch( epoch=> $starttime ))),
		    $gen->dtend( $w3cdtf->format_datetime( DateTime->from_epoch( epoch=> $endtime ))),
		    $gen->summary( $description ),
		    $gen->categories( "TimeAccount,$kind" )
		));
	}
    }
    my $output;
    $output .= "Content-type: text/xml\n";
    $output .= "Content-Disposition: attachment; filename=$now.xml\n\n";
    $output .= $gen->Vcalendar( $html );
    $output;
}





#
#最後のlogの時刻をとりだす。
#
sub LastAccess{
    my $hashref = $session->param_hashref();
    #
    #Hash keyをソートし、最大の値のもの(最新の時刻)を返す。
    #
    my $last = (sort {$b<=>$a} ( keys %{$hashref} ))[0];
    #
    #記録がなければ現在時刻を返す。
    #
    $last = time if $last == 0;
    $last;
}


sub time2text{
    my ( $time ) = @_;

    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
    "$hour:$min";
}


sub TimeSelector{
    my ( $cgi, $name, $time ) = @_;

    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
    my %hour;
    foreach my $i ( 0..23 ){
	$hour{$i}=$i;
    }
    my %min;
    foreach my $i ( 0..59 ){
	$min{$i}=$i;
    }
    my $html;
    $cgi->param( "$name.hour", $hour );
    $cgi->param( "$name.min", $min );
    $html  = CGISelect0( $cgi, "$name.hour", \%hour );
    $html .= ":";
    $html .= CGISelect0( $cgi, "$name.min", \%min );
    $html;
}


sub CGISelect0{
    my ( $cgi, $name,$labels)=@_;
    my $html;
    my @keys = keys %{$labels};
    $html = $cgi->popup_menu(-name=>$name,
		       -values=>[ sort { $a<=>$b } @keys ],
		       -labels=>$labels);
}

sub Footer{
    my ( $cdi ) = @_;
    my $html;
    $html .= $cgi->end_form();
    $html .= $cgi->end_html();
    $html;
}

sub Header
{
    my ( $cgi, $title, $session )=@_;
    my $html;
    #
    #record session id as a cookie.
    #
    $html .= $session->header(-charset=>"utf-8" );
    $html .= $cgi->start_html(-title=>"$title",
			    -lang =>"ja",
			    -head =>[]
			    );
    $html .= $cgi->start_form(-method=>"POST",
			    -action=>"$myurl?CGISESSID=".$id,
			    -enctype=>"multipart/form-data"
			    );
    $html;
}

#
#アクションを記録する。
#
sub Record{
    my ( $fromhour, $frommin, $type, $description, $session ) = @_;
    my $endtime = time;
    #
    #round secounds
    #
    $endtime = int( $endtime / 60 ) * 60;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($endtime);
    my $deltahour = $hour - $fromhour;
    my $deltamin  = $min  - $frommin ;
    if ( $deltahour < 0 || ( $deltahour == 0 && $deltamin < 0 ) ){
	$deltahour += 24;
    }
    my $starttime = $endtime - $deltahour * 3600 - $deltamin * 60;
    return if $starttime == $endtime;
    #
    #Record history in the session variables.
    #
    while ( defined $session->param( $starttime ) ){
	#
	#last record
	#
	my ( $lastfrom, $lasttype, $lastdescription ) = @{$session->param( $starttime )};
	#
	#Same kind, same description, and not downloaded
	#
	if ( $lasttype == $type && $lastdescription eq $description ){
	    #
	    #Merge with the last record.
	    #
	    $session->clear( $starttime );
	    $starttime = $lastfrom;
	    next;
	}
	else{
	    last;
	}
    }
    $session->param( $endtime, [ $starttime, $type, $description, 0 ] );
}

sub ShowHistory{
    my ( $cgi ) = @_;
    my $now = time;
    my $html;

    my $histlen = $cgi->param( "histlen" ) || 1;
    $histlen *= 3600 * 24;

    my $hashref = $session->param_hashref();
    my @history = (sort {$b<=>$a} ( keys %{$hashref} ));
    my @share;
    my $last;
    my $first = 1;
    foreach my $endtime ( @history ){
	#
	#session変数のなかには、CGI::Sessionが設定したものもあるので、
	#キーが数値なもの(つまり0と比較してfalseなもの)のみを抽出
	#
	if ( $last ){
	    #
	    #1 week以前の古いレコードを消す。
	    #
	    if ( $endtime != 0 && $endtime + 7*86400 < $now ){
		$session->clear( $endtime );
	    }
	}
	elsif ( $endtime != 0 ){
	    #
	    #
	    #
	    my ( $starttime, $kind, $description ) = @{$session->param( $endtime )};
	    $html .= time2text($starttime);
	    $html .= "-";
	    $html .= time2text($endtime);
	    $html .= colored( $cgi, $kind, $description );
	    if ( $first ){
	      $html .= $cgi->submit( -name=>"undo" );
	      $first = 0;
	    }
	    $html .= $cgi->br;
	    if (  $starttime < $now - $histlen ){
		$starttime = $now - $histlen;
		$last = 1;
	    }
	    $share[$kind] += ( $endtime - $starttime );
	}
    }
    my $worktime = 0;
    foreach my $i ( 1..9 ){
	$worktime += $share[$i];
    }
    $share[0] = $histlen - $worktime;
    $html = bargraph( $cgi, @share ) . $cgi->br . $html;
    $html;
}




#
#Read log and make dictionary of recently used words.
#
sub GetHistory{
    my ( $session ) = @_;
    my $history;
    my %dict;

    my $hashref = $session->param_hashref();
    my @history = (sort {$b<=>$a} ( keys %{$hashref} ));
    my @share;
    my $last;
    foreach my $now ( @history ){
	#
	#session変数のなかには、CGI::Sessionが設定したものもあるので、
	#数値がキーになっているもののみを抽出
	#
	if ( $now != 0 ){
	    my ( $starttime, $kind, $description ) = @{$session->param( $now )};
	    if ( ! defined $dict{"$kind $description"} ){
		$dict{"$kind $description"}=1;
		push @{$history->[$kind]}, $description;
	    }
	}
    }
    $history;
}



sub colored{
    my ( $cgi, $color, $string ) = @_;

    $cgi->font( {-color=>$colors[$color]}, $string );
}

sub graph{
    my ( $id, @share ) = @_;
    my @data = ( [ 0 .. 9 ], [ @share ] );

    my $graph = new GD::Graph::pie( 120, 120 );

    $graph->set( #title       => "Web server Usage, March 2004",
		 dclrs       => [ @colors ],
		 pie_height  => 32,
		 start_angle => 90 );
    open F, "> /var/www/tmp/$id.png";
    print F $graph->plot(\@data)->png();
    close F;
    "/tmp/$id.png";
}



sub Dialog{
    my ( $cgi, $session, $history ) = @_;

    my $html;

    #
    #時間範囲を指定する。
    #
    $html .= TimeSelector( $cgi, "from", LastAccess( $session ) );
    $html .= "から今まで何をしていましたか?";
    $html .= $cgi->br;

    foreach my $i ( 1..9 ){
	#
	#9つのデフォルト範疇を準備する。内容は自分で設定する。
	#携帯電話のボタンに対応させる。
	#できればヒストリーが使いたい。CGI.pmのjavascript拡張とかないのかな。
	#
	$html .= $cgi->submit( -name=>"kind",
			       -value=>$i
			       );
	$html .= $cgi->textfield(-name=>"text$i", -size=>15);
	#
	#それぞれ5種類、最後に使用した項目を優先。
	#
	my $dict = $history->[$i];
	my @dict;
	if ( $dict ){
	    @dict = @{$dict};
	}
	@dict = @dict[0..4] if 4 < $#dict;
	my $line;
	foreach my $word ( @dict ){
	    my $elem;
	    $session->param( "dic$word", $i );
	    #$cgi->a()にしたいところだが、時区間の初値を指定する必要があるので難しい。
	    $elem .= $cgi->submit( -name=>"direct", -value=>$word );
	    #$elem .= $cgi->a( {-href=>"$myurl?direct=$word" }, $word );
	    #$elem .= $cgi->hidden( -name=>$word, -value=>$i ) . "\n";
	    $line .= $elem;
	    #print STDERR $elem, ":word\n";
	}
	$html .= colored( $cgi, $i, $line );
	$html .= $cgi->br() . "\n\n";
    }
    #
    #0番は「使途不明時間」
    #
    $html .= $cgi->submit( -name=>"kind",
			   -value=>0 );
    $html .= "使途不明";
    $html .= $cgi->hr(); #--------------------------------------

    #print STDERR $session->id . " 3\n";
    $cgi->param( "CGISESSID", $session->id );
    $html .= "Session ID:"
	. $cgi->textfield( -name=>"CGISESSID", -value=>$session->id, -size=>30 ) 
	. $cgi->submit( -name=>"update" ) 
	. $cgi->hr(); #--------------------------------------

    
    #$html .= $cgi->checkbox_group( -name=>"ikind",
    #				 -values=>[ 1,2,3,4,5,6,7,8,9 ],
    #				   -labels=>{ 1=>1, 2=>2, 3=>3,4=>4,5=>5,6=>6,7=>7,8=>8,9=>9 });
    #$html .= $cgi->br;
    #$html .= $cgi->submit( -name=>"icall",
    #			   -value=>"iCal形式でダウンロード"
    #	) . $cgi->br;
  $html .= "iCal(過去一週間分):";
  for(my $i=1; $i<=9; $i++ ){
    $html .= $cgi->a({ -href=>"$webcalurl?CGISESSID=" . $session->id . "&icall=1&histlen=7&ikind=$i" }, "[" . $i . "]" );
  }
    $html .= $cgi->hr; #--------------------------------------
    my $selector = CGISelect0( $cgi, "histlen", { 1=>1, 2=>2, 3=>3, 4=>4, 5=>5, 6=>6, 7=>7 } );
    $html .= "<h3>過去" . $selector . "日分の時間使途" . $cgi->submit(-name=>"update") . "</h3>";
    $html;
}


sub bargraph{
    my ( $cgi, @share ) = @_;

    my $sum;
    foreach my $i ( 0..9 ){
	$sum += $share[$i];
    }
    my $html;
    foreach my $i ( 0..9 ){
	# 15 min per a bar
	my $len = int(0.5+96*$share[$i]/$sum);
	$html .= colored( $cgi, $i, "|" x $len );
    }
    $html;
}
    
