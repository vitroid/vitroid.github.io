#!/usr/bin/env python
# coding: utf-8

#range overlap
#http://satoshi.blogs.com/life/2007/10/rubyrange.html

from icalendar import Calendar  #additional
import re
import urllib2
import time
import calendar    #additional

#http://www.gesource.jp/programming/python/code/0005.html
def geturl(url):
    fp = urllib2.urlopen(url)
    ical = fp.read()
    fp.close()
    return ical
#print ical

#http://codespeak.net/icalendar/
#http://www.zope.org/Members/ajs17/barebones_icalendar
def parse(ical):
    events = []
    cal = Calendar.from_string(ical)
    for event in cal.walk('vevent'):
        dtstart = event.get('dtstart', '')
        starttime=0
        endtime = 0
        if dtstart:
            start = event.decoded('dtstart', '')
            starttimetuple = start.timetuple()
            starttime = calendar.timegm(starttimetuple)

        dtend = event.get('dtend', '')
        if dtend:
            end = event.decoded('dtend', '')
            endtimetuple = end.timetuple()
            endtime = calendar.timegm(endtimetuple)
            if endtimetuple[8] == -1:
                endtime -= 86400

        summary = event.get('summary', '').replace('\,', ',')
        description = event.get('description', '').replace('\,', ',')
        location = event.get('location', '').replace('\,', ',')
        #no. mktime is not inverse of gmtime.
        #use calendar.timegm instead.
        events.append({'starttime':starttime,
                       'endtime':endtime,
                       'summary':summary,
                       'description':description,
                       'location':location,})
#'summary':unicode(summary,'utf-8'),
 #                      'description':unicode(description,'utf-8'),
  #                     'location':unicode(location,'utf-8')})
    return events


# App config
TWITTER_CONSUMER_KEY    = '**************'
TWITTER_CONSUMER_SECRET = '################'
#easy_install python-twitter
import twitter   #additional

def tweet(msgs,userkey,usersecret,tag):
    import oauth   #additional
    api = twitter.Api( consumer_key = TWITTER_CONSUMER_KEY,
                       consumer_secret = TWITTER_CONSUMER_SECRET,
                       access_token_key = userkey,
                       access_token_secret = usersecret,
                       input_encoding='utf8')

    #print  api.GetUser(account)
    for tweet in msgs:
        tweet = re.sub('\s+',' ',tweet)
        tweet = tweet[0:(139-len(tag))]+tag
        api.PostUpdate(tweet)
        time.sleep(1)


#iCalerndarの中に、変な日付けが含まれている場合がある。
#行を分割し、CREATED行を削除。
def Preparse(str):
    newstr = ""
    for line in str.splitlines():
        #print line
        if line.find("CREATED:0000") != 0:
            newstr += line + "\n"
        else:
            print line
    #print newstr
    return newstr


now = time.time()
timetuple = time.localtime()
todaystart   = (timetuple[0],timetuple[1],timetuple[2],0,0,0,0,0,0)
#mktime is inverse of localtime, so it is ok.
todaystart   = time.mktime(todaystart)
todayend     = todaystart + 60*60*24

msgs = []

#cpml
events = parse(Preparse(geturl("http://www.google.com/calendar/ical/o0crucuhclcj9mk4vm93ci19es%40group.calendar.google.com/public/basic.ics")))

for event in events:
    if todayend+86400 < event['starttime'] or event['endtime'] < todaystart+86400:
        pass
    else:
        msgs.append(u'明日:' + event['summary'] + "@" + event['location'])

for event in events:
    if todayend < event['starttime'] or event['endtime'] < todaystart:
        pass
    else:
        msgs.append(u'今日:' + event['summary'] + "@" + event['location'])

#print msgs
    
#deadline
events = parse(Preparse(geturl("http://www.google.com/calendar/ical/s1m3ufcpc0ol9tndp9sjtsqaio%40group.calendar.google.com/public/basic.ics")))

for event in events:
    if todayend < event['starttime'] or event['endtime'] < todaystart:
        pass
    else:
        msgs.append(u'締切:' + event['summary'] + "@" + event['location'])

#tweet all
tweet(msgs,"%%%%%%%%%%%%%%%%%%%%%%%%","@@@@@@@@@@@@@@@@@@@@@@@@@",u" #cpml")

