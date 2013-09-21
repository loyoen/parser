#coding=utf-8
from sgmllib import SGMLParser
from Queue import Queue
from oneparser import *
from baike import *
import threading
import sys
import urllib2
from urllib import urlencode
import cookielib, urllib2,urllib

from myparser.models import company, jobsite
Name_List = ["前程无忧","新浪微博","elong酒店","新浪新闻"]
Url_List  = ["http://51job.com/","weibo.com","http://hotel.elong.com/","http://search.sina.com.cn/"]
class parsertest:
    def __init__(self,path):
        self.path = path
    def getMainPages(self):
        f = open(self.path,'r')
        line = []
        self.MainPages = {}
        line = f.read().split('\n')
        #print line
        for item in line:
            try:
                #print item
                Company_Code = item.split('\t')[0]
                Company_Name = item.split('\t')[1]
                self.MainPages[Company_Code] = Company_Name
            except:
                print "error"
        #print MainPages

    def parserstart(self,myid):
        i = 1
        if myid==4:
            baike_start()
            return
        if myid==2:
            cityname = "hangzhou"
            print cityname
            Site_Name = Name_List[myid]
            Site_Url = Url_List[myid]
            myurl = Site_Url+cityname
            site_existnow = jobsite.objects.filter(Site_Url = Site_Url)
            if not site_existnow:
                #print "site....."
                site = jobsite(Site_Url = Site_Url,Site_Name = Site_Name)
                site.save()
                i += 1
                woparser = myparser(site=site,baseurl=myurl)
                woparser.doParsing()
                del woparser
            else:
                site = site_existnow[0]
                i += 1
                woparser = myparser(site=site,baseurl=myurl)
                woparser.doParsing()
                del woparser
            return
        
        for item in self.MainPages:
            Company_Name = self.MainPages[item]
            #print type(item)
            Company_Code = item.decode("GBK")
            #print Company_Code,Company_Name
            Site_Name = Name_List[myid]
            Site_Url = Url_List[myid]
            site_existnow = jobsite.objects.filter(Site_Url = Site_Url)
            
            
            if not site_existnow:
                #print "site....."
                site = jobsite(Site_Url = Site_Url,Site_Name = Site_Name)
                site.save()
                print i
                print Company_Name
                i += 1
                woparser = myparser(site=site,Company_Code=Company_Code,Company_Name=Company_Name)
                woparser.doParsing()
                del woparser
            else:
                site = site_existnow[0]
                print i
                print Company_Name
                i += 1
                woparser = myparser(site=site,Company_Code=Company_Code,Company_Name=Company_Name)
                woparser.doParsing()
                del woparser





