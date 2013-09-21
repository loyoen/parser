# -*- coding: utf-8 -*-

import urllib2
import re
from BeautifulSoup import BeautifulSoup

import sqlite3
import time
import os


import MySQLdb




#————————————————————————————————————————————————————————————————

##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    #blank_line=re.compile('\n+')
    #s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s
 
##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
    
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
 
def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)

#————————————————————————————————————————————————————————————————

def huanhang(x):
    for i in range(0,x):
        print


def caiji(wz):#caij
    num=1
    while 1:
        print wz
        urlopen=urllib2.urlopen(wz)
        nr=urlopen.read()
        if re.search(r'''<div id="intitle">''',nr) is not None:
            time.sleep(num)
            print 'sleep'+str(num)
            num+=1
        else:
            return nr

def ruku(CompanyCode,CompanyName,BaikeFieldName,BaikeText,MuluDict,PicDict,ckzl,ctbqs,xgcts,DateFrom,AddTime):#放入数据库
    BaikeFieldName=BaikeFieldName
    BaikeText=BaikeText
    num=1
    while 1:
        try:
            conn=MySQLdb.connect(host='s1.cisimi.com',user='root',passwd='good7788',db='cisimi',port=3306,charset='utf8')
            cur=conn.cursor()
            #cur.execute("insert into baiketbl (CompanyCode,CompanyName,BaikeFieldName,BaikeText,DataFrom,AddTime)\
        #VALUES ('"+CompanyCode+"','"+CompanyName+"','"+BaikeFieldName+"','"+BaikeText+"','"+DataFrom+"','"+AddTime+"')")
            cur.execute("insert into baike_company_main (CompanyCode,CompanyName,BaikeFieldName,BaikeText,DateFrom,AddTime)\
        VALUES (%s,%s,%s,%s,%s,%s)",(CompanyCode,CompanyName,BaikeFieldName,BaikeText,DateFrom,AddTime))
            baike_company_detail_list='CompanyCode,CompanyName,TiaoMuMingCheng,TiaoMuNeiRong,ChunTiaoMuNeiRong,DateFrom,AddTime'
            for key in MuluDict:
                MuLuMing='【详细介绍】'+key
                MuLuNeiRong=MuluDict[key]
                ChunMuLuNeiRong=filter_tags(MuLuNeiRong)
                cur.execute("insert into baike_company_detail ("+baike_company_detail_list+")\
        values (%s,%s,%s,%s,%s,%s,%s)",(CompanyCode,CompanyName,MuLuMing,MuLuNeiRong,ChunMuLuNeiRong,DateFrom,AddTime))
            for key in PicDict:
                pic_name='【图片】'+key
                pic_url=PicDict[key]
                cur.execute("insert into baike_company_detail ("+baike_company_detail_list+")\
        values ('"+CompanyCode+"','"+CompanyName+"','"+pic_name+"','"+pic_url+"','"+pic_url+"','"+DateFrom+"','"+AddTime+"')")
            cur.execute("insert into baike_company_detail ("+baike_company_detail_list+")\
        values ('"+CompanyCode+"','"+CompanyName+"','【参考资料】','"+ckzl+"','"+filter_tags(ckzl)+"','"+DateFrom+"','"+AddTime+"')")
            cur.execute("insert into baike_company_detail ("+baike_company_detail_list+")\
        values ('"+CompanyCode+"','"+CompanyName+"','【词条标签】','"+ctbqs+"','"+ctbqs+"','"+DateFrom+"','"+AddTime+"')")
            cur.execute("insert into baike_company_detail ("+baike_company_detail_list+")\
        values ('"+CompanyCode+"','"+CompanyName+"','【相关词条】','"+xgcts+"','"+xgcts+"','"+DateFrom+"','"+AddTime+"')")
            conn.commit()
            cur.close()
            conn.close()
            break
        except Exception,ex:
            if re.search(r'''2013, 'Lost connection to MySQL server during query''',str(ex)) is not None:
                print 'mysql入库连接断开，sleep'+str(num)+'秒'
                time.sleep(num)
                num+=1
            else:
                print 'mysql入库有其他错误，错误信息为：'+str(ex)
                break


def caijibaike(CompanyCode,CompanyName):
    #公司名查重
    count=''
    num=1
    while 1:
        try:
            conn=MySQLdb.connect(host='s1.cisimi.com',user='root',passwd='good7788',db='cisimi',port=3306,charset='utf8')
            cur=conn.cursor()
            count=cur.execute("select * from baike_company_main where CompanyName='"+CompanyName+"'")
            cur.close()
            conn.close()
            break
        except Exception,ex:
                if re.search(r'''2013, 'Lost connection to MySQL server during query''',str(ex)) is not None:
                    print 'mysql查重连接断开，sleep'+str(num)+'秒'
                    time.sleep(num)
                    num+=1
                else:
                    print 'mysql查重有其他错误，错误信息为：'+str(ex)
                    break

    if count==0:
        baidusousuo=caiji('http://www.baidu.com/s?wd='+CompanyName)
        baikewz_list=re.findall(r'''<a.*?href="(.*?)".*?><em>'''+CompanyName+'''</em>_百度百科</a>''',baidusousuo)
        if len(baikewz_list)==1:
            baikewz=baikewz_list[0]
            DateFrom=baikewz#数据库字段-DateFrom
            baikenr=caiji(baikewz)
            mc=re.findall(r'''<h1 class="title".*?>(.*?)</h1>''',baikenr)[0]

            soup=BeautifulSoup(baikenr)

            try:
                BaikeFieldName=str(soup('div',{'id':'card-container'})[0])#百科名片 数据库字段-BaikeFieldName
            except:
               BaikeFieldName='' 

            xxjs=str(soup('div',{'id':'lemmaContent-0'})[0])

            #去掉 编辑本段 内容
            bjbd_list=re.findall(r'''(<span class="text_edit editable-title".*?</span>)''',xxjs)
            for bjbd in bjbd_list:
                xxjs=xxjs.replace(bjbd,'')
                
            #去掉图片
            for text_pic_right in soup('div',{'class':'text_pic layoutright'}):#去掉右图片
                xxjs=xxjs.replace(str(text_pic_right),'')
            for text_pic_left in soup('div',{'class':'text_pic layoutleft'}):#去掉左图片
                xxjs=xxjs.replace(str(text_pic_left),'')
            for lazyload_map in soup('div',{'class':'lazyload map-view layoutright'}):#去掉地图
                xxjs=xxjs.replace(str(lazyload_map),'')
            hidefocuslist=re.findall(r'''(<a hidefocus="true".*?</a>)''',xxjs)
            for hidefocus in hidefocuslist:#去掉hidefocus图片
                xxjs=re.sub(hidefocus,'',xxjs)
            BaikeText=xxjs#详细介绍 数据库字段-BaikeText

            #以下是按目录截取的详细介绍
            fenduan_list=xxjs.split(r'''<h2 class="headline-1">''')
            MuluDict={}#创建目录空字典
            for num in range(1,len(fenduan_list)-1):
                fenduan='''<h2 class="headline-1">'''+fenduan_list[num]
                muluming=re.findall(r'''<h2 class="headline-1">.*?<span class="headline-content">(.*?)</span></h2>''',fenduan)[0]\
                          #数据库字段-CompanyAll相关目录名
                mulunr_para_list=re.findall(r'''(<div class="para">[\s\S]*?</div>)''',fenduan)
                mulunr=''
                for mulunr_para in mulunr_para_list:
                    mulunr+=mulunr_para#数据库字段-CompanyAll相关目录内容
                MuluDict[muluming]=mulunr#添加到字典：键为muluming，值为mulunr。
            
            cttcwz_list=re.findall(r'''<a id="view-album-morealbum".*?href="(.*?)"''',baikenr)
            PicDict={}#创建图片空字典
            if len(cttcwz_list)==1:
                cttcwz='http://baike.baidu.com'+cttcwz_list[0]
                #cttcnr=caiji('http://baike.baidu.com/albums/15491/6468542/0/0.html#.')
                cttcnr=caiji(cttcwz)
                pic_id_desc_list=re.findall(r'''\{"imgId"\:"(.*?)"\,"owner"\:".*?"\,"imgDesc"\:"(.*?)"''',cttcnr)
                if len(pic_id_desc_list)>0:
                    for pic_id_desc in pic_id_desc_list:
                        pic_url=r'http://hiphotos.baidu.com/baike/pic/item/'+pic_id_desc[0]+'.jpg'#图片网址
                        pic_name=pic_id_desc[1].decode('unicode_escape').encode('utf-8')#图片名称
                        if pic_name=='':
                            pic_name=pic_url
                        if pic_name not in PicDict:
                            if pic_name+'1' not in PicDict:
                                PicDict[pic_name]=pic_url#添加到字典：键为图片名称，值为图片网址。
                            else:
                                num=1
                                while True:
                                    num+=1
                                    if pic_name+str(num) not in PicDict:
                                        PicDict[pic_name+str(num)]=pic_url#添加到字典：键为图片名称，值为图片网址。
                                        break
                        else:
                            pic_url1=PicDict[pic_name]
                            del PicDict[pic_name]
                            PicDict[pic_name+'1']=pic_url1#修改重名的键
                            PicDict[pic_name+'2']=pic_url#添加到字典：键为图片名称，值为图片网址。
            try:
                ckzl=str(soup('dl',{'class':'viewRefer nslog-area log-set-param'})[0])#参考资料
            except:
                ckzl=''

            try:
                ctbqym=str(soup('dl',{'id':'viewExtCati'})[0])#词条标签源码
                ctbq_list=re.findall(r'''<a class="taglist" href=".*?" target="_blank">(.*?)</a>''',ctbqym)
                ctbqs=''
                for ctbq in ctbq_list:
                    if ctbqs!='':
                        ctbqs+='，'+ctbq
                    else:
                        ctbqs=ctbq
            except:
                ctbqs=''

            try:
                xgctym=str(soup('dl',{'id':'relatedLemmaDown'})[0])#相关词条源码
                xgct_list=re.findall(r'''<a title=.*?target="_blank">(.*?)</a>''',xgctym)
                xgcts=''
                for xgct in xgct_list:
                    if xgcts!='':
                        xgcts+='，'+xgct
                    else:
                        xgcts=xgct
            except:
                xgcts=''
            
            AddTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#当前时间 数据库字段-AddTime

            ruku(CompanyCode,CompanyName,BaikeFieldName,BaikeText,MuluDict,PicDict,ckzl,ctbqs,xgcts,DateFrom,AddTime)

    #else:
        #print CompanyCode+'有重复'



def minglu():#按名录采集
    fp=open(r'companyall.txt'.decode('utf-8').encode('cp936'),'r+')
    nr=fp.readlines()
    fp.close()
    for linen in nr:
        line=linen.replace('\n','').decode('cp936').encode('utf-8')
        print line
        CompanyCode=''#数据库字段-CompanyCode
        CompanyName=line#数据库字段-CompanyName
        caijibaike(CompanyCode,CompanyName)
        #break

def search_bd():
    page=1
    while 1:
        print '第'+str(page)+'页'
        page10=str(page*10)
        bdssnr=caiji('http://www.baidu.com/s?wd=%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&pn='+page10+'&tn=baiduhome_pg&ie=utf-8&usm=3')
        Company_list=re.findall(ur'''<h3 class="t"><a[\s\S]*?href="(.*?)"[\s\S]*?>([\u4e00-\u9fa5A-Za-z0-9]*?)<em>有限公司</em>.*?</a></h3>''',bdssnr.decode('''utf-8'''))
        for Company in Company_list:
            CompanyUrl=Company[0]
            CompanyName=Company[1].encode('utf-8')+'有限公司'
            if CompanyName!='':
                CompanyCode=''
                print CompanyName
                caijibaike(CompanyCode,CompanyName)
        page_id=re.findall(r'''(<p id="page" >[\s\S]*?</p>)''',bdssnr)[0]
        if re.search(r'''下一页''',page_id) is None:
            print 'over'
            break
        else:
            page+=1


def baike_start():
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    minglu()
    search_bd()
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
