---
title: Twitter関連
---
[software](/software)


## Pop and tweet

Tweet arrived mails in the POP3 mailbox. Tweeted mails wil be removed. Modify the source if you do not want the mails deleted.

[](http://theochem.chem.okayama-u.ac.jp/vitroid/Twitter関連/PopAndTweet.py)


## iCalendar to tweet

Feed iCalendar and tweet today's events.

[](http://theochem.chem.okayama-u.ac.jp/vitroid/Twitter関連/icalandtweet.py)


## Required packages

* ~~twitter [http://mike.verdone.ca/twitter/~~](http://mike.verdone.ca/twitter/~~)
* simplejson [http://pypi.python.org/pypi/simplejson/](http://pypi.python.org/pypi/simplejson/)
* icalendar (for icalandtweet.py only) [http://codespeak.net/icalendar](http://codespeak.net/icalendar)

## Usage

Put the following line in your crontab.

```
0,10,20,30,40 * * * * python /your/home/PopAndTweet.py
0 0 * * * python /your/home/icalandtweet.py
```

## License

GPL


## ChangeLog

* 2011-8-17 OAuth is implemented.
* 2009-11-20 Treatment of allday events was improved.
* 2009-11-25 modified to decode  base64-encoded body in PopAndTweet.py . [松本](/松本) - [matto](/matto) 
<!--  -->




## Linked from

* [Twitter関連](/Twitter関連)


----

[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Twitter関連.md)

