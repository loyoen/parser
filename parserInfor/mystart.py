import cookielib, urllib2,urllib

url = "http://127.0.0.1:8000/doparser/1/"

ans = urllib2.urlopen(url,timeout=2).read()
