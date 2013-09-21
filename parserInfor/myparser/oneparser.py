# -*- coding: utf-8 -*-
from Queue import Queue
import threading
import sys
import urllib2
from getInfor import *
from myparser.models import company,room,hotel,comment,record
import datetime
from django.db import connection
import socket
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import cookielib, urllib2,urllib
import re
import httplib,urllib
import simplejson
connection.text_factory = str

search_url = {}
search_url["http://51job.com/"] = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&funtype=0000&industrytype=00&keywordtype=0&lang=c&stype=1&postchannel=0000&fromType=1&keyword="
search_url["weibo.com"] = "http://s.weibo.com/weibo/mykeyword&Refer=index"
def openurl(url):
    try:
        ans = urllib2.urlopen(url,timeout=2).read()
        return ans
    except (urllib2.URLError, socket.timeout) as e:
        if hasattr(e, 'reason'):
            reason = str(e.reason)
        else:
            reason = 'N/A'
        if reason == 'timed out':
            return openurl(url)
        else:
            return ""
    return ""
        
def findpage(url,keyword):
    
    content = openurl(url)

    mykeyword = ">"+keyword+"<"
    pos = content.find(mykeyword)
    number = 2
    if pos!=-1:
        while number!=0:
            while content[pos]!='<':
                pos -= 1
            number -= 1
            pos -= 1
    else:
        return ""
    while content[pos]!="\"":
        pos += 1
    pos += 1
    ans = ""
    #print "here...",content[pos:pos+100]
    while content[pos]!="\"":
        ans += content[pos]
        pos += 1
    #print "ans...",ans
    return ans
   

            
class myparser:
    def __init__(self,site,baseurl="NULL",Company_Code="NULL",Company_Name="NULL"):
        self.site = site
        self.Company_Code = Company_Code
        self.Company_Name = Company_Name
        self.baseurl = baseurl
        #print "it is ma...",self.Company_Name
        
        
    def doParsing(self):
        #print "start ......aaaaa...."
        
        if self.site.Site_Url=="http://51job.com/":
            start_url = search_url[self.site.Site_Url] + self.Company_Name
            Company_Page = findpage(start_url,self.Company_Name)
            print Company_Page,"...."
            if Company_Page!="":
            
                mycompany = company.objects.filter(Company_Code=self.Company_Code)
                
                myInfor = getInfor(Company_Page)
                if not mycompany:
                    CompanyInfor = myInfor.CompanyInfor()
                    print "!!!!!!!.....",CompanyInfor
                    mycompany = company(Company_Code=self.Company_Code, Company_Name=self.Company_Name.decode("cp936").encode("utf-8"), AddDate=datetime.datetime.now(), Description=CompanyInfor["Description"], Profession=CompanyInfor["Profession"], Category=CompanyInfor["Category"], Company_Size=CompanyInfor["Company_Size"], DataFrom=self.site, UpDate=datetime.datetime.now())
                    mycompany.save()
                else:
                    mycompany = mycompany[0]
                    mycompany.UpDate = datetime.datetime.now()
                    mycompany.save()

                rec_num = myInfor.getjobInfor(mycompany)
                try:
                    myrecord = record(update=datetime.datetime.now(), parsertype="51job招聘信息", res = str(rec_num), name=mycompany)
                    myrecord.save()
                except:
                    print "record err"
                del myInfor
                return
        elif self.site.Site_Url=="weibo.com":
            mystarturl = "http://www.baidu.com/s?cl=2&tn=baiduwb&ie=utf-8&rtt=2&wb=4&wd="
            start_url = mystarturl + self.Company_Name.decode("cp936")
            
            mycompany = company.objects.filter(Company_Code=self.Company_Code)
            
            
            myInfor = getInfor(start_url)
            if not mycompany:
                mycompany = company(Company_Code=self.Company_Code, Company_Name=self.Company_Name.decode("cp936").encode("utf-8"), AddDate=datetime.datetime.now(), Description="", Profession="", Category="", Company_Size="", DataFrom=self.site, UpDate=datetime.datetime.now())
                mycompany.save()
            else:
                mycompany = mycompany[0]
                mycompany.UpDate = datetime.datetime.now()
                mycompany.save()
                
            
            rec_num = myInfor.getWeiboInfor(mycompany)
            try:
                myrecord = record(update=datetime.datetime.now(), parsertype="weibo信息", res = str(rec_num), name=mycompany)
                myrecord.save()
            except:
                print "record err"
            
        elif self.site.Site_Url=="http://hotel.elong.com/":
            
            mystart_url = "http://hotel.elong.com/" + "hangzhou"
            start_content = openurl(mystart_url)
            print start_content
            soup = BeautifulSoup(''.join(start_content))
            htmldata = soup.findAll("strong", {"id" : "HotelCountN"})
            try:
                HotelCount = htmldata[0].text
            except:
                HotelCount = "10"
            print "HotelCount:",HotelCount
            htmldata = soup.findAll("input", {"class" : "intxt city"})
            try:
                cityId = htmldata[0]["name"]
                cityName = htmldata[0]["value"]
            except:
                return
            
            print "city:",cityId
            
            
            headers = {
                "Accept":"application/json, text/javascript, */*",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
               
                "Content-Length":"1251",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Origin":"http://hotel.elong.com",
                "Proxy-Connection":"keep-alive",
                "Referer":"http://hotel.elong.com/hangzhou/",
      
                "X-Requested-With":"XMLHttpRequest"   
                }
            body = {
                "isSquare":"false",
                "citynameen":"hangzhou",
                "viewpath":"~/Views/HotelListC/hotellist.aspx",
                "hsr.RankType":"-1",
                "hsr.CityId":cityId,
                "hsr.CityName":cityName,
                "hsr.NationalCityName":cityName,
                "hsr.CheckInDate":"2013/9/20 0:00",
                "hsr.CheckOutDate":"2013/9/21 0:00",
                "hsr.HotelName":"",
                "hsr.Keywords":"",
                "hsr.KeywordsType":"None",
                "hsr.ReturnKeywordsType":"None",
                "hsr.ReturnKeywords":"",
                "hsr.AreaId":"",
                "hsr.AreaName":"",
                "hsr.AreaType":"0",
                "hsr.PoiId":"0",
                "hsr.PoiName":"",
                "hsr.LowPrice":"0",
                "hsr.HighPrice":"0",
                "hsr.StarLevel":"None",
                "hsr.BrandId":"0",
                "hsr.BrandName":"",
                "hsr.StarLevels":"",
                "hsr.BrandIds":"",
                "hsr.TagId":"",
                "hsr.FacilityIds":"",
                "hsr.SupplierIds":"",
                "hsr.Distance":"10",
                "hsr.StartLat":"0",
                "hsr.StartLng":"0",
                "hsr.EndLat":"0",
                "hsr.EndLng":"0",
                "hsr.IsBigBed":"false",
                "hsr.IsDoubleBed":"false",
                "hsr.IsFreeBreakfast":"false",
                "hsr.IsFreeNet":"false",
                "hsr.IsCoupon":"false",
                "hsr.IsCashback":"false",
                "hsr.IsNoGuarantee":"false",
                "hsr.IsPrePay":"false",
                "hsr.PaymentType":"All",
                "hsr.IsLimitTime":"false",
                "hsr.IsNotReturnNoRoomHotel":"false",
                "hsr.ThemeIds":"",
                "hsr.HotelSort":"ByDefault",
                "hsr.PageIndex":"1",
                "hsr.PageSize":HotelCount,
                "hsr.ShowPageSize":"20",
                "hsr.HotelCount":HotelCount,
                "hsr.ListType":"Common",
                "hsr.Language":"CN",
                "hsr.CardNo":"192928",
                "hsr.MemberLevel":"Common",
                "hsr.ApCardNo":"",
                "hsr.Campaign_Id":"",
                "hsr.ChannelCode":"0000",
                "hsr.OrderFromId":"50",
                "hsr.HotelChannel":"Hotel",
                "hsr.IsNotAcceptRecommend":"false",
                "hsr.IsNotChange":"false",
                "hsr.IsMystical":"false"
                    
                    }
                    
            
            
            body = urllib.urlencode(body)
            #headers = urllib.urlencode(headers)
            #与网站构建一个连接
            conn = httplib.HTTPConnection("hotel.elong.com");
            #开始进行数据提交   同时也可以使用get进行
            conn.request(method="POST",url="/isajax/List/Search",body=body,headers=headers);
            #返回处理后的数据
            response = conn.getresponse()
            import StringIO
            compressedstream = StringIO.StringIO(response.read())   
            import gzip
            gzipper = gzip.GzipFile(fileobj=compressedstream)      
            data = gzipper.read().encode("utf-8")
            conn.close()
            json = simplejson.loads(data)
            
            i = 1
            for eachHotel in json["value"]["ListStaticInfos"]:
                print i
                i += 1
                print eachHotel["HotelId"]
                try:
                    image_url = eachHotel["ImageUrl_350"]
                except:
                    image_url = "empty"
                if image_url=="":
                    image_url = "empty"
                if not image_url:
                    image_url = "empty"
                try:
                    myhotel = hotel(address=eachHotel["HotelAddress"],name=eachHotel["HotelNameCn"],image_url=image_url,DataFrom=self.site)
                    myhotel.save()
                except:
                    continue
                try:
                    getHotelInfo(eachHotel["HotelId"],eachHotel["Commerical"]["HotelAreaId"],cityName,cityId,myhotel)
                    getComment(eachHotel["HotelId"],eachHotel["TotalComment"],myhotel)
                except:
                    continue
                
        elif self.site.Site_Url=="http://search.sina.com.cn/":
            mystarturl = "http://search.sina.com.cn/?c=news&from=channel&col=&range=&source=&country=&size=&time=&pf=2131425458&ps=2134309112&dpc=1&q="
            start_url = mystarturl + self.Company_Name.decode("cp936")
            
            mycompany = company.objects.filter(Company_Code=self.Company_Code)
            
            
            myInfor = getInfor(start_url)
            if not mycompany:
                mycompany = company(Company_Code=self.Company_Code, Company_Name=self.Company_Name.decode("cp936").encode("utf-8"), AddDate=datetime.datetime.now(), Description="", Profession="", Category="", Company_Size="", DataFrom=self.site, UpDate=datetime.datetime.now())
                mycompany.save()
            else:
                mycompany = mycompany[0]
                mycompany.UpDate = datetime.datetime.now()
                mycompany.save()
                
            
            rec_num = myInfor.getNewsInfor(mycompany,self.site)
            try:
                myrecord = record(update=datetime.datetime.now(), parsertype="新闻信息", res = str(rec_num), name=mycompany)
                myrecord.save()
            except:
                print "record err"
def getComment(hid,totalComment,myhotel):
    mycur_url = "/isajax/HotelDetailNew/GetHotelReviews?pageSize=10&pageIndex=1&recommentType=2&cityNameEn=hangzhou&viewpath=~%2Fviews%2FHotelDetailC%2FHotelDetail.aspx&issquare=False"
    hotel_id_str = "&"+"hotelId="+str(hid)
    hereurl = mycur_url + hotel_id_str
    headers = {
                "Accept":"application/json, text/javascript, */*",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Connection":"keep-alive",
                "Referer":"http://hotel.elong.com/hangzhou/"+str(hid)+"/",
                "X-Requested-With":"XMLHttpRequest",
                "Host":"hotel.elong.com"
            }
    body={}
    conn = httplib.HTTPConnection("hotel.elong.com");
            #开始进行数据提交   同时也可以使用get进行
    #print "ppppp....."
    conn.request("GET",hereurl,'',headers)
            #返回处理后的数据
    #print "tttt....."
    response = conn.getresponse()
    
    import StringIO
    compressedstream = StringIO.StringIO(response.read())   
    import gzip
    gzipper = gzip.GzipFile(fileobj=compressedstream)      
    comment_data = gzipper.read().encode("utf-8")
    conn.close()
   
    print "open end..."
    #print comment_data
    #print "ssssss...."
    json = simplejson.loads(comment_data)
    print comment_data
    
    for eachcomment in json["CommentList"]:
        mycomment = comment(date=str(eachcomment["CreatedTime"]),content=eachcomment["Content"],roomtype=eachcomment["RoomTypeName"],hotelFrom=myhotel)
        mycomment.save()
    
    
def getHotelInfo(hid,areaid,cityname,cityid,myhotel):
    referer = "http://hotel.elong.com/hangzhou/"+hid+"/"
    headers = {
        "Accept":"application/json, text/javascript, */*",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
               
        "Content-Length":"1673",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"hotel.elong.com",
        "Origin":"http://hotel.elong.com",
        "Referer":referer,
      
        "X-Requested-With":"XMLHttpRequest"   
        }
    body = {
        "hotelId":hid,
        "prepay":"false",
        "cityNameEn":"hangzhou",
        "viewpath":"~/views/HotelDetailC/HotelDetail.aspx",
        "issquare":"False",
        "requestInfo.RankType":"0",
        "requestInfo.CityId":cityid,
        "requestInfo.CityName":cityname,
        "requestInfo.CheckInDate":"2013/9/20 0:00",
        "requestInfo.CheckOutDate":"2013/9/21 0:00",
        "requestInfo.HotelName":"",
        "requestInfo.Keywords":"",
        "requestInfo.KeywordsType":"None",
        "requestInfo.ReturnKeywordsType":"None",
        "requestInfo.ReturnKeywords":"",
        "requestInfo.AreaId":areaid,
        "requestInfo.AreaName":"",
        "requestInfo.AreaType":"1",
        "requestInfo.PoiId":"0",
        "requestInfo.LowPrice":"0",
        "requestInfo.HighPrice":"0",
        "requestInfo.StarLevel":"35",
        "requestInfo.BrandId":"0",
        "requestInfo.StarLevels":"",
        "requestInfo.BrandIds":"",
        "requestInfo.TagId":"",
        "requestInfo.FacilityIds":"",
        "requestInfo.SupplierIds":"",
        "requestInfo.Distance":"10",
        "requestInfo.StartLat":"0",
        "requestInfo.StartLng":"0",
        "requestInfo.EndLat":"0",
        "requestInfo.EndLng":"0",
        "requestInfo.IsBigBed":"false",
        "requestInfo.IsDoubleBed":"false",
        "requestInfo.IsFreeBreakfast":"false",
        "requestInfo.IsFreeNet":"false",
        "requestInfo.IsCoupon":"false",
        "requestInfo.IsCashback":"false",
        "requestInfo.IsNoGuarantee":"false",
        "requestInfo.IsPrePay":"false",
        "requestInfo.PaymentType":"All",
        "requestInfo.IsLimitTime":"false",
        "requestInfo.IsNotReturnNoRoomHotel":"false",
        "requestInfo.ThemeIds":"",
        "requestInfo.HotelSort":"ByDefault",
        "requestInfo.PageIndex":"1",
        "requestInfo.PageSize":"20",
        "requestInfo.ShowPageSize":"60",
        "requestInfo.HotelCount":"0",
        "requestInfo.ListType":"Common",
        "requestInfo.Language":"CN",
        "requestInfo.CardNo":"192928",
        "requestInfo.MemberLevel":"Common",
        "requestInfo.ApCardNo":"",
        "requestInfo.Campaign_Id":"",
        "requestInfo.ChannelCode":"0000",
        "requestInfo.OrderFromId":"50",
        "requestInfo.HotelChannel":"Hotel",
        "requestInfo.IsNotAcceptRecommend":"false",
        "requestInfo.IsNotChange":"false",
        "requestInfo.IsMystical":"false"
        }
    body = urllib.urlencode(body)
    conn = httplib.HTTPConnection("hotel.elong.com");
    #开始进行数据提交   同时也可以使用get进行
    try:
        conn.request(method="POST",url="/isajax/HotelDetailNew/GetHotelRoomset",body=body,headers=headers)
    except:
        conn.close()
        return -1
    #返回处理后的数据
    response = conn.getresponse()
    import StringIO
    compressedstream = StringIO.StringIO(response.read())   
    import gzip
    gzipper = gzip.GzipFile(fileobj=compressedstream)      
    data = gzipper.read().encode("utf-8")
    conn.close()
    json = simplejson.loads(data)
    #print json["value"]
    for myroom in json["value"]["HotelRoomList"]:
        print myroom["RoomName"] 
        image_url = "empty"
        try:
            image_url = myroom["RoomImageList"][0]["ImageUrl"]
        except:
            image_url = "empty"
            
        if image_url=="":
            image_url = "empty"
        myroom["RatePlanList"][0]["AvgPrice"]
        print "................"
        oneroom = room(name=myroom["RoomName"],image_url=image_url,area=myroom["Area"],bed=myroom["Bed"],net=myroom["Net"],price=myroom["RatePlanList"][0]["AvgPrice"],hotelFrom=myhotel)
        oneroom.save()
    
    return 1
