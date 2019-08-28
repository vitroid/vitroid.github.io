#!/usr/bin/env python
# coding: utf-8
import poplib, email, email.Header
import email.Message
import base64
import quopri


def _get_email_body(self):
    check = self.get_content_type()
    if check=="text/plain":
        dirty=self.get_payload()
        charset = self.get_content_charset()
        #print charset,dirty
        enc = self['Content-Transfer-Encoding']
        if enc == "base64":
            dirty = base64.decodestring(dirty)
        elif enc == "quoted-printable":
            dirty = quopri.decodestring(dirty)
        #print dirty,enc
        dirty = unicode(dirty, charset)
        return dirty
    part=self.get_payload()
    return _get_email_body(part[0])

def pop():
    msgs = []
    M = poplib.POP3_SSL('pop.gmail.com')
    M.user("cpmljp@gmail.com")
    M.pass_("!!!!!!!!!!!!!")   # plain text
    numMessages = len(M.list()[1])
    for i in range(numMessages):
        lines=M.retr(i+1)[1]
        fulltext = "\n".join(lines)
        mail = email.message_from_string(fulltext)
        #Get subject in plain text
        subject = ""
        for header,encoding in email.Header.decode_header(mail["Subject"]):
            if encoding != None:
                subject += unicode(header,encoding) + " "
            else:
                subject += header + " "
        #Get body in plain text
        body = _get_email_body(mail)
        #Compose one-line message.
        msgs.append(subject + "|" + body)
        M.dele(i+1)
    M.quit()
    return msgs

# App config
TWITTER_CONSUMER_KEY    = '##################'
TWITTER_CONSUMER_SECRET = '*****************'
#easy_install python-twitter
import twitter   #additional
import time
import re


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
        print tweet
        time.sleep(1)


msgs = pop()
#print msgs
tweet(msgs,"@@@@@@@@@@@@@@@@@@@@@@@@","%%%%%%%%%%%%%%%%%%%%",u" #cpml")
