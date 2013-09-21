#encoding=utf-8
import BeautifulSoup
from sgmllib import SGMLParser
from Queue import Queue
import urllib2
import MySQLdb
from myparser.models import recruit,weibo,atlist,news
import re
import socket
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mypattern={}
onepattern = {}
onepattern['position'] = r"<span><em id=.+job-title.+>.+</em><i></i></span>"
onepattern['positioninner'] = [0,-1,-1]
onepattern['startdate'] = r"<li>生效时间：<span>.+</span></li>"
onepattern['startdateinner'] = [0,-1,-1,-1]
onepattern['enddate'] = r"<li>结束时间：<span>.+</span></li>"
onepattern['enddateinner'] = [0,-1,-1,-1]
onepattern['numneeded'] = r"<li>招聘人数：<span>.+</span></li>"
onepattern['numneededinner'] = [0,-1,-1,-1]
onepattern['categoryOfWork'] = r"<li>工作性质：<span>.+</span></li>"
onepattern['categoryOfWorkinner'] = [0,-1,-1,-1]
onepattern['degree'] = r"<li>学历要求：<span>.+</span></li>"
onepattern['degreeinner'] = [0,-1,-1,-1]
onepattern['description'] = r"<h5>岗位描述：</h5>[^<]*<ul>.+</ul>"
onepattern['descriptioninner'] = [1,-1,-1]
onepattern['requirement'] = r"<h5>岗位要求：</h5>[^<]*<ul>.+</ul>"
onepattern['requirementinner'] = [1,-1,-1]
onepattern['location'] = r'<dt>所在地区：</dt><dd><span>.+</span></dd>?'
onepattern['locationinner'] = [1,0,-1]
onepattern['department'] = ''
onepattern['departmentinner'] = [-2]
onepattern['addurl']=""
onepattern['baseurl'] = "/zhaopin/"

secpattern = {}
secpattern['position']=r"<h4 class=.+hrs_grayBorderTitle.+>(.|\n)+</h4>"
secpattern['positioninner']=[0,-1]
secpattern['startdate']=""
secpattern['startdateinner']=[-2]
secpattern['enddate']=""
secpattern['enddateinner']=[-2]
secpattern['department']=r"<dt>所属部门:</dt>(.|\n)*<dd>.+</dd>"
secpattern['departmentinner']=[1,-1,-1]
secpattern['location']=r"<dt>工作地点:</dt>(.|\n)*<dd>.+</dd>"
secpattern['locationinner']=[1,-1,-1,-1]
secpattern['numneeded']=r"<dt>招聘人数:</dt>(.|\n)*<dd>.+</dd>"
secpattern['numneededinner']=[1,-1,-1]
secpattern['categoryOfWork']=r"<dt>职位性质:</dt>(.|\n)*<dd>.+</dd>"
secpattern['categoryOfWorkinner']=[1,-1,-1,-1]
secpattern['degree']=""
secpattern['degreeinner']=[-2]
secpattern['description']=r"<dt>工作职责：</dt>.*<div style=.word-break:break-all;word-spacing: normal;.>.*</div>"
secpattern['descriptioninner']=[2,-1]
secpattern['requirement']=r"<dt>职位要求：</dt>.*<div style=.word-break:break-all;word-spacing: normal;.>.*</div>"
secpattern['requirementinner']=[2,-1]
secpattern['baseurl'] = "baidu"
secpattern['addurl']="http://talent.baidu.com"

thirdpattern ={}
thirdpattern["position"] = r"<td class=.+sr_bt.+ colspan=.+2.+ >.*</td>"
thirdpattern["positioninner"]=[0,-1]
thirdpattern["startdate"]=r'<tr><td class="txt_1".*>.*</tr>'
thirdpattern["startdateinner"]=[0,1,-1]
thirdpattern["location"]=r'<tr><td class="txt_1".*>.*</tr>'
thirdpattern["locationinner"]=[0,3,-1]
thirdpattern["numneeded"]=r'<tr><td class="txt_1".*>.*</tr>'
thirdpattern["numneededinner"]=[0,5,-1]
thirdpattern["years"]=r'<tr><td class="txt_1".*>.*</tr>'
thirdpattern["yearsinner"]=[1,1,-1]
thirdpattern["degree"]=r'<tr><td class="txt_1".*>.*</tr>'
thirdpattern["degreeinner"]=[1,3,-1]

thirdpattern["description"]=r'<div style="padding-bottom:30px;">.*</div>?'
thirdpattern["descriptioninner"]=[0,-1]

thirdpattern["categoryOfWork"]=r'<td colspan="6" style="width:100%" class="job_detail">.*</td>?'
thirdpattern["categoryOfWorkinner"]=[0,-1,-1,-1,-1]

thirdpattern["Com_Profession"] = r'<td><strong>.*</strong>.*</td>?'
thirdpattern["Com_Professioninner"] = [0,0,-1,-1]

thirdpattern["Com_Category"] = r'<td><strong>.*</strong>.*</td>?'
thirdpattern["Com_Categoryinner"] = [0,2,-1,-1]
thirdpattern["Com_Size"] = r'<td><strong>.*</strong>.*</td>?'
thirdpattern["Com_Sizeinner"] = [0,4,-1,-1]
thirdpattern["Com_Description"] = r'<p class="txt_font">.*</p>?'
thirdpattern["Com_Descriptioninner"] = [0,-1]

fourthpattern = {}

mypattern["http://job.alibaba.com/zhaopin/index"] = onepattern
mypattern["http://talent.baidu.com/baidu/web/index/CompbaiduPageindex"] = secpattern
mypattern["http://51jobs.com"] = thirdpattern

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
   
def findinfor(url,content,name1,name2):
    if mypattern[url][name1]=='':
        return ""
    pattern = re.compile(mypattern[url][name1])
    match = pattern.search(content.replace("\n",""))
    ans = ""
    
    
    if match:
        try:
            if name1 == "description":
                isin = False
                des_str = match.group()
                des_str = des_str.replace("\n","").replace("&nbsp;","").replace("\r","")
                endpos = des_str.find("</div>")
                i = 0
                for charitem in des_str:
                    if charitem == "<":
                        isin = True
                    elif charitem == ">" and isin:
                        isin = False
                    elif not isin:
                        ans += charitem
                    i += 1
                    if i>= endpos:
                        return ans
                return ans
            strtemp = match.group().replace("<br />","").replace("\n","").replace("&nbsp;","").replace("<br>","").replace("\r","").replace("</br>","").replace("<p>","").replace("</p>","").replace("<BR>","").replace("<P>","").replace("</P>","").replace("<HR>","").replace("<STRONG>","").replace("</STRONG>","").replace("<br/>","").replace("<B>","").replace("</B>","")
            
            mysoup = BeautifulSoup.BeautifulStoneSoup(strtemp)
            mylist = mypattern[url][name2]
            ans = mysoup
            #print ans
            
            try:
                for item in mylist:
                    if item==-1:
                        ans=ans.next
                    else:
                        ans=ans.contents[item]
            except:
                return ""
        except:
            return ""
    else:
        return ""
   
    #ans = ans.replace("\t"," ")
    return ans
        
def dealjob(url):
    ans = {}
    ans["url"] = ""
    ans["position"] = ""
    ans["startdate"] = ""
    ans["location"] = ""
    ans["numneeded"] = ""
    ans["years"] = ""
    ans["degree"] = ""
    ans["description"] = ""
    
    try:
        print url
        content = openurl(url)
        content = content.decode("GBK")
        ans["url"] = url
        position = findinfor("http://51jobs.com",content,"position","positioninner")
        print position
        ans["position"] = position
        startdate = findinfor("http://51jobs.com",content,"startdate","startdateinner")
        print startdate
        ans["startdate"] = startdate
        location = findinfor("http://51jobs.com",content,"location","locationinner")
        print location
        ans["location"] = location
        numneeded = findinfor("http://51jobs.com",content,"numneeded","numneededinner")
        print numneeded
        ans["numneeded"] = numneeded
        years = findinfor("http://51jobs.com",content,"years","yearsinner")
        print years
        ans["years"] = years
        degree = findinfor("http://51jobs.com",content,"degree","degreeinner")
        print degree
        if degree.find("<")!= -1:
            degree = ""
        ans["degree"] = degree
        description = findinfor("http://51jobs.com",content,"description","descriptioninner")
        print description
        ans["description"] = description
        
        categoryOfWork = findinfor("http://51jobs.com",content,"categoryOfWork","categoryOfWorkinner")
        print categoryOfWork
        print "------------------------------"
        #category = findinfor("http://51jobs.com",content,"category","categoryinner")
        #print category
        return ans
          
    except:
        return ans
class Basegeturls(SGMLParser):   #这个Basegeturls类作用是分析下载的网页，把网页中的所有链接放在self.url中。
    def reset(self):
        self.url = []
        SGMLParser.reset(self)
    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.url.extend(href)

class getInfor:
    def __init__(self,Company_Page):
        self.Company_Page = Company_Page
        self.innercontent = openurl(Company_Page)
        
    def CompanyInfor(self):
        ans = {}
        content = self.innercontent
        content = content.decode("GBK")
        
        print "companyinfor......"
        #print content
        Profession = findinfor("http://51jobs.com",content,"Com_Profession","Com_Professioninner")
        Category = findinfor("http://51jobs.com",content,"Com_Category","Com_Categoryinner")
        Company_Size = findinfor("http://51jobs.com",content,"Com_Size","Com_Sizeinner")
        Description = findinfor("http://51jobs.com",content,"Com_Description","Com_Descriptioninner")
        
        ans["Profession"] = Profession
        
        ans["Category"] = Category
        
        ans["Company_Size"] = Company_Size
       
        ans["Description"] = Description
        
        print ans
        #print "____________________________________"
        return ans
    
    
    def getjobInfor(self,onecompany):
        queue=Queue()
        Pagebelong = {}
        Pagebelong[self.Company_Page] = True
        Jobbelong = {}
        rec_num = 0
        existJob = recruit.objects.filter(companyname_id = onecompany.id)
        #print "pppppppppppppppppppppp...."
        #print existJob
        for eachjob in existJob:
            Jobbelong[eachjob.url] = True
            #print "is in ......"
        queue.put(self.Company_Page)
        current_url = ""
        while True:
            try:
                print "url start...."
                try:
                    if queue.empty():
                        print "kong le....."
                        return rec_num
                    else:
                        current_url = queue.get()
                except:
                    print "jiushini"
                    return rec_num
                print "myurl", current_url
                
                try:
                    content = openurl(current_url)
                    content = content.decode("GBK")
                    rec_num += self.getJobDetail(content,Jobbelong,onecompany)
                    print "jobdetail......"
                    self.getJobPage(content,queue,Pagebelong)
                    print "jobpage..........."
                except:
                    print "ddddddddd....."
                    continue
            except:
                print "..............end........."
                #break
                return rec_num
            
    def getJobDetail(self,content,belong,onecompany):
        rec_num = 0
        pos1 = content.find("<td class=\"txt_5 td0\">")
        content = content[pos1:]
        pos2 = content.find("每页显示")
        print pos1,pos2
        enddate = []
        print "mmmmm......"
        if pos1!=-1 and pos2!=-1:
            content = content[:pos2]
            print "aaaa......"
            pattern=r'<td class="txt_5 td3">\d\d\d\d-\d\d-\d\d</td>'
            for match in re.findall(pattern,content):
                mysoup = BeautifulSoup.BeautifulStoneSoup(match)
                ans = mysoup.contents[0].next
                enddate.append(ans)
                #print "Found %s" % ans
            print "ccccc......"
            parser = Basegeturls()
            try:
                parser.feed(content)
            except:
                print "cannot parser"
                return 0
            #print "url queue...",parser.url
            print "bbbbb......" 
            i = 0
            for item in parser.url:
                myenddate = enddate[i]
                i += 1
                print item
                #print "~~~~~~~~~",jobinfor 
                try:
                    isbelong = belong[item]
                    if isbelong:
                        continue
                except:
                    belong[item] = True
                    jobinfor = dealjob(item)
                    print "deal..............."
                    try:
                        onejob = recruit(url=jobinfor["url"], position=jobinfor["position"], description=jobinfor["description"], requirement="", numneeded=jobinfor["numneeded"], categoryOfWork="", yearsForWork=jobinfor["years"], degree=jobinfor["degree"], startdate=jobinfor["startdate"], enddate=myenddate, location=jobinfor["location"],companyname=onecompany)
                        onejob.save()
                        rec_num += 1
                    except Exception,e:
                        print e
                        print "nimeimeimei............"
            del parser
        return rec_num
    
    def getJobPage(self,content,queue,belong):
        pos1 = content.find("class=\"orange1\"")
        content = content[pos1:]
        pos2 = content.find("职位名称")
        print pos1,pos2
        if pos1!=-1 and pos2!=-1:
            content = content[:pos2]
            parser = Basegeturls()
            try:
                parser.feed(content)
            except:
                print "cannot parser"
                return 0
            #print "url queue...",parser.url
            for item in parser.url:
                #print item
                #print "~~~~~~~~~",jobinfor 
                try:
                    isbelong = belong[item]
                    if isbelong:
                        continue
                except:
                    belong[item] = True
                    queue.put(item)
            del parser
        return 0
    
    def getWeiboNextpage(self,weibo_content,onecompany):
        rec_num = 0
        from BeautifulSoup import BeautifulSoup
        if weibo_content=="":
            return
        soup = BeautifulSoup(''.join(weibo_content))
        htmldata = soup.findAll("div", {"class" : "weibo_detail"})
        for eachWeibo in htmldata:
            weibocontent = eachWeibo.next
            author = weibocontent.findAll("a", {"name" : "weibo_rootnick"})
            is_v = weibocontent.findAll("span")
            publish_infor =  eachWeibo.findAll("div", {"class" : "m"})
            atwho = weibocontent.findAll("a", {"name" : "weibo_nick"})
            is_v = "0"
            try:
                if is_v[0]["class"]=="weibo_level_icon weibo_level_icon_1":
                    is_v = "1"
                elif is_v[0]["class"]=="weibo_level_icon weibo_level_icon_2":
                    is_v = "2"
            except:
                is_v = "0"
            
            publish_date = publish_infor[0].next.text
            #except:
                    
            author_name = author[0].text
            author_url = author[0]["href"]
            weibo_content = weibocontent.text
            myweibo = None
            try:
                weibo_img = eachWeibo.findAll("div", {"class" : "weibo_img_small"})[0].next
                smimg = weibo_img["src"]
                mdimg = weibo_img["data-mdimg"]
                bgimg = weibo_img["data-bgimg"]
                myweibo = weibo(author=author_name,isV=is_v,url=author_url,content=weibo_content,smimg=smimg,mdimg=mdimg,bgimg=bgimg,adddate=datetime.datetime.now(),publish_date=publish_date,companyname=onecompany)
                myweibo.save()
                rec_num += 1
            except:
                smimg = ""
                mdimg = ""
                bgimg = ""
                myweibo = weibo(author=author_name,isV=is_v,url=author_url,content=weibo_content,smimg=smimg,mdimg=mdimg,bgimg=bgimg,adddate=datetime.datetime.now(),publish_date=publish_date,companyname=onecompany)
                myweibo.save()
                rec_num += 1
                
            for item in atwho:
                atname = item.text
                aturl = item["href"]
                myatlist = atlist(name=atname,url=aturl,blong=myweibo)
                myatlist.save()
            print author_name
            print "......................."
        return rec_num
    
    def getWeiboInfor(self,onecompany):
        from BeautifulSoup import BeautifulSoup
        #print self.innercontent
        rec_num = 0
        if self.innercontent=="":
            self.innercontent = openurl(self.Company_Page)
        myweibocontent = self.innercontent
        rec_num += self.getWeiboNextpage(myweibocontent,onecompany)
        page = 10
        lastpage = True
        while myweibocontent.find("下一页")!=-1:
            lastpage = False
            newurl = self.Company_Page + "&pn=" + str(page)
            myweibocontent = openurl(newurl)
            rec_num += self.getWeiboNextpage(myweibocontent,onecompany)
            page += 10
            
        return rec_num
    
        
    def getHotelInfor(self,site):
        from BeautifulSoup import BeautifulSoup
        print self.innercontent
        print self.Company_Page
        print self.innercontent.find("roomTypes")
        soup = BeautifulSoup(''.join(self.innercontent))
        htmldata = soup.findAll("li", {"sid" : "22165"})
        print htmldata
        
        for item in htmldata:
            print item["rpid"]
        return
    
    def getNewsInfor(self,onecompany,onesite):
        from BeautifulSoup import BeautifulSoup
        #print self.innercontent
        rec_num = 0
        if self.innercontent=="":
            self.innercontent = openurl(self.Company_Page)
        print self.Company_Page
        #print self.innercontent
        myNewsContent = self.innercontent
        soup = BeautifulSoup(''.join(self.innercontent))
        pagedata = soup.findAll("div", {"class" : "pagebox"})
        rec_num += self.getNewsNextpage(myNewsContent,onecompany,onesite)
        page = 2
        lastpage = True
        if not pagedata:
            return rec_num
        while pagedata.text.find("下一页")!=-1:
            lastpage = False
            newurl = self.Company_Page + "&page=" + str(page)
            myNewsContent = openurl(newurl)
            rec_num += self.getNewsNextpage(myNewsContent,onecompany,onesite)
            page += 1
            
        return rec_num
    
    def getNewsNextpage(self,news_content,onecompany,onesite):
        print "lllll....."
        rec_num = 0
        from BeautifulSoup import BeautifulSoup
        import re
        match = re.compile(r'<div class="box-result clearfix" .*?>.*?</div>')
        if news_content=="":
            print "kong...."
            return rec_num
        
        news_content = news_content.decode("GBK","ignore").encode("utf-8")
        #mynews_content = news_content[:news_content.find("<!-- ie6")-1] + "</body></html>"
        #soup = BeautifulSoup(''.join(mynews_content))
        
        htmldata = match.findall(news_content.replace("\n","").replace("\r",""))
        #htmldata = soup.findAll("div", {"class" : "box-result clearfix"})
       
       
        print len(htmldata),"==========="
        for eachNews in htmldata:
            print "tttt....."
            soup = BeautifulSoup(''.join(eachNews))
            mynews = soup.findAll("div", {"class" : "r-info r-info2"})
            if not mynews:
                print "bushiba"
                mynews = soup.findAll("div", {"class" : "r-info"})
            myimg = soup.findAll("div", {"class" : "r-img"})
            try:
                newstime = mynews[0].findAll("span", {"class" : "fgray_time"})[0].text
                news_url = mynews[0].findAll("a", {"target" : "_blank"})[0]["href"]
                mytitle = mynews[0].findAll("a", {"target" : "_blank"})[0].text
                mycontent = mynews[0].findAll("p", {"class" : "content"})[0].text
            except:
                continue
            if myimg:
                img_url = myimg[0].findAll("img", {"class" : "left_img"})[0]["src"]
                mynews = news(newsTitle=mytitle, newsContent=mycontent, newsUrl=news_url, newsDate=newstime, imgUrl=img_url, DataFrom=onesite, companyname=onecompany)
                mynews.save()
                rec_num += 1
            else:
                print mytitle
                print mycontent
                print news_url
                print newstime
                
                mynews = news(newsTitle=mytitle, newsContent=mycontent, newsUrl=news_url, newsDate=newstime, imgUrl="", DataFrom=onesite, companyname=onecompany)
                mynews.save()
                rec_num += 1
            
        return rec_num
        
        
            


            
        
        
