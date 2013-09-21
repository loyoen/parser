# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sys
from myparser.models import company,recruit, favor, keyword
from myparser.oneparser import *
from myparser.getInfor import *
from myparser.test import parsertest
import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import simplejson
import re
from pymmseg import mmseg

COMPANYS_NUM = 20
JOBS_NUM = 20

def index(req):
    #print req.user.id,"qqqqqqqq...."
    if req.user.is_authenticated():
        infor = favor.objects.filter(who_id=req.user.id)
        a = {}
    #print infor
        a['favor_companys'] = infor
        req.user.is_authenticated = True
        a['user'] = req.user
        return render_to_response("home.html",a)
    else:
        return render_to_response("index.html")

def doparser(req,parser_id=''):
    print "dddddd"
    test = parsertest("companyall.txt")
    myid = int(parser_id)
    
    
    test.getMainPages()
    test.parserstart(myid)
    return render_to_response('end.html')

def zhaopin(req):
    return HttpResponse("bbbb")

def company_browse(req,company_id=''):
    data = recruit.objects.filter(companyname_id=company_id)
    ans = {}
    endpos = len(data)
    if len(data)>JOBS_NUM:
        ans["manyJobs"] = True
        endpos = JOBS_NUM
    ans['infor'] = data[:endpos]
    mycompany = company.objects.filter(id=company_id)
    name = mycompany[0]
    ans['mycompany'] = name
    #print "name",name
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('company.html',ans)

def companyJobs_browse(req,company_id='',page=''):
    infor = recruit.objects.filter(companyname_id=company_id)
    ans = {}
    startpos = 0
    endpos = 0
    print page,".................",company_id
    if len(infor)>=int(page)*JOBS_NUM:
        startpos = (int(page)-1)*JOBS_NUM
        endpos = int(page)*JOBS_NUM
    elif len(infor)<page*JOBS_NUM and len(infor)>(int(page)-1)*JOBS_NUM:
        startpos = (int(page)-1)*JOBS_NUM
        endpos = len(infor)
    ans['jobs'] = infor[startpos:endpos]
    if endpos>0:
        ans['com_name'] = infor[0].companyname.Company_Name
    lastpagenum = []
    nextpagenum = []
    if len(infor)%JOBS_NUM!=0:
        totalpages = len(infor)/JOBS_NUM + 1
    else:
        totalpages = len(infor)/JOBS_NUM
    i = 0
    if int(page)-4>=1 and int(page)+4<=totalpages:
        i = int(page)-4
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=int(page)+4:
            nextpagenum.append(i)
            i += 1
    elif int(page)-4<1:
        i = 1
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=9 and i<=totalpages:
            nextpagenum.append(i)
            i += 1
    elif int(page)+4>totalpages:
        i = 1
        if totalpages-8>0:
            i = totalpages - 8
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page) + 1
        while i<=totalpages:
            nextpagenum.append(i)
            i += 1
    ans['lastpagenum'] = lastpagenum
    ans['nextpagenum'] = nextpagenum
    ans['current_page'] = int(page)
    ans['com_id'] = company_id
    if int(page)>1:
        ans['lastpage'] = int(page)-1
    
    if int(page)<totalpages:
        ans['nextpage'] = int(page)+1
    
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('companyjobs.html',ans)


def job_browse(req,job_id=''):
    data = recruit.objects.filter(id=job_id)
    ans = {}
    ans['infor'] = data[0]
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('job.html',ans)

def company_list(req,page=''):
    ans = {}
    infor = company.objects.filter()
    startpos = 0
    endpos = 0
    print page,"................."
    if len(infor)>=int(page)*COMPANYS_NUM:
        startpos = (int(page)-1)*COMPANYS_NUM
        endpos = int(page)*COMPANYS_NUM
    elif len(infor)<page*COMPANYS_NUM and len(infor)>(int(page)-1)*COMPANYS_NUM:
        startpos = (int(page)-1)*COMPANYS_NUM
        endpos = len(infor)
    ans['companys'] = infor[startpos:endpos]
    print '...............',ans['companys']
    lastpagenum = []
    nextpagenum = []
    totalpages = len(infor)/COMPANYS_NUM + 1
    i = 0
    if int(page)-4>=1 and int(page)+4<=totalpages:
        i = int(page)-4
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=int(page)+4:
            nextpagenum.append(i)
            i += 1
    elif int(page)-4<1:
        i = 1
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=9 and i<=totalpages:
            nextpagenum.append(i)
            i += 1
    elif int(page)+4>totalpages:
        i = 1
        if totalpages-8>0:
            i = totalpages - 8
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page) + 1
        while i<=totalpages:
            nextpagenum.append(i)
            i += 1
    ans['lastpagenum'] = lastpagenum
    ans['nextpagenum'] = nextpagenum
    ans['current_page'] = int(page)
    if int(page)>1:
        ans['lastpage'] = int(page)-1
   
    if int(page)<totalpages:
        ans['nextpage'] = int(page)+1
    
    
    favor_com = favor.objects.filter(who_id=req.user.id)
    test=[]
    for item in favor_com:
        test.append(item.which_id)
        
    for item in ans['companys']:
            if item.id in test:
                item.is_in_attention = True
            else:
                item.is_in_attention = False
    #item = company.objects.all[0]
    #print item.Company_Name.encode("utf-8")
    #print ans['companys']
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('company_list.html',ans)

def jobs_list(req,page=''):
    ans = {}
    infor = recruit.objects.filter()
    startpos = 0
    endpos = 0
    #print page,"................."
    if len(infor)>=int(page)*JOBS_NUM:
        startpos = (int(page)-1)*JOBS_NUM
        endpos = int(page)*JOBS_NUM
    elif len(infor)<page*JOBS_NUM and len(infor)>(int(page)-1)*JOBS_NUM:
        startpos = (int(page)-1)*JOBS_NUM
        endpos = len(infor)
    ans['jobs'] = infor[startpos:endpos]
    lastpagenum = []
    nextpagenum = []
    totalpages = len(infor)/JOBS_NUM + 1
    i = 0
    if int(page)-4>=1 and int(page)+4<=totalpages:
        i = int(page)-4
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=int(page)+4:
            nextpagenum.append(i)
            i += 1
    elif int(page)-4<1:
        i = 1
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page)+1
        while i<=9 and i<=totalpages:
            nextpagenum.append(i)
            i += 1
    elif int(page)+4>totalpages:
        i = 1
        if totalpages-8>0:
            i = totalpages - 8
        while i<int(page):
            lastpagenum.append(i)
            i += 1
        i = int(page) + 1
        while i<=totalpages:
            nextpagenum.append(i)
            i += 1
    ans['lastpagenum'] = lastpagenum
    ans['nextpagenum'] = nextpagenum
    ans['current_page'] = int(page)
    if int(page)>1:
        ans['lastpage'] = int(page)-1
    
    if int(page)<totalpages:
        ans['nextpage'] = int(page)+1
    
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('jobs_list.html',ans)

def about(req):
    ans = {}
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        ans['user'] = req.user
    return render_to_response('about.html',ans)

    
@csrf_exempt
def register(req):
    if req.method == 'POST':
        ans = {}
        name = req.POST.get('rname', '')
        mail = req.POST.get('remail', '')
        passwd = req.POST.get('rpasswd', '')
        print name,mail,passwd
        if name=="" or mail=="" or passwd=="":
            ans["empty"] = True
            ans["rname"] = name
            ans["remail"] = mail
            ans["rpasswd"] = passwd
            return render_to_response("index.html",ans)
            
        pattern = re.compile(r'([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$')
        match = pattern.match(mail)
        if not match:
            ans["notmail"] = True
            ans["rname"] = name
            ans["remail"] = mail
            ans["rpasswd"] = passwd
            return render_to_response("index.html",ans)
        userexist = User.objects.filter(username = name)
        if userexist:
            ans["userexist"] = True
            ans["rname"] = name
            ans["remail"] = mail
            ans["rpasswd"] = passwd
            return render_to_response("index.html",ans)
        user = User(username = name, email = mail)
        user.set_password(passwd)
        user.save()
        wizard = auth.authenticate(username = name, password = passwd)
        auth.login(req, wizard)
        if req.user.is_authenticated():
            req.user.is_authenticated = True
            ans['user'] = req.user
        return render_to_response("home.html",ans)
    
@csrf_exempt
def login(req):
    if req.method == 'POST':
        name = req.POST.get('lname', '')
        passwd = req.POST.get('lpasswd', '')
        print name,passwd
        wizard = auth.authenticate(username = name, password = passwd)
        if wizard:
            auth.login(req, wizard)
            a = {}
            print 'ppppppp....'
            print req.user.id
            infor = favor.objects.filter(who=req.user)
            a['favor_companys'] = infor
            if req.user.is_authenticated():
                req.user.is_authenticated = True
                a['user'] = req.user
            return render_to_response("home.html",a)
        else:
            a = {}
            a['logfail'] = True
            a['lname'] = name
            a['lpasswd'] = passwd
            return render_to_response("index.html",a)

@csrf_exempt
def addfavor(req):
    if req.method == 'POST':
        com_id = req.POST.get('myid', '')
        print req.user.username
        print "addddd.........."
        #mycom = company.objects.filter(id=com_id)[0]
        onefavor = favor(who=req.user, which_id=com_id)
        onefavor.save()
       
        a = {"message":"true"}
            
        json = simplejson.dumps(a,ensure_ascii=False)
        return HttpResponse(json,mimetype='application/javascript')
    
@csrf_exempt
def rmfavor(req):
    if req.method == 'POST':
        com_id = req.POST.get('myid', '')
        #print req.user.username
        print com_id
        #mycom = company.objects.filter(id=com_id)[0]
        onefavor = favor.objects.get(who_id=req.user.id, which_id=com_id)
        onefavor.delete()
       
        a = {"message":"true"}
            
        json = simplejson.dumps(a,ensure_ascii=False)
        return HttpResponse(json,mimetype='application/javascript')
    
def SplitKeyword(req):
    mmseg.dict_load_defaults()
    com_list = company.objects.filter()
    for com in com_list:
        words = com.Company_Name.encode("utf-8")
        algor = mmseg.Algorithm(words)
        for tok in algor:
            word = tok.text.decode("utf-8")
            print word
            keytable = keyword(word=word, mycom = com)
            keytable.save()
    
    return HttpResponse("split end")


@csrf_exempt
def search(req):
    if req.method == 'POST':
        words = req.POST.get('keywords', '')
        #print words
        com_count = {}
        cont = {}
        #分词
        mmseg.dict_load_defaults()
        #print words.encode("utf-8")
        algor = mmseg.Algorithm(words.encode("utf-8"))
        for tok in algor:
            word = tok.text.decode("utf-8")
            print word
            res = keyword.objects.filter(word = word)
            for item in res:
                print "get............."
                try:
                    com_count[str(item.mycom.id)] += 1
                except:
                    com_count[str(item.mycom.id)] = 1
                    cont[str(item.mycom.id)] = item.mycom
        
        sortres = sorted(com_count.iteritems(),key=lambda asd:asd[1], reverse=True)
        resultlist = []
        for each in sortres:
            eachres = {}
            eachres['id'] = str(each[0])
            eachres['count'] = str(each[1])
            eachres['Company_Name'] = cont[str(each[0])].Company_Name
            eachres['company_id'] = cont[str(each[0])].id
            resultlist.append(cont[str(each[0])])
            
        a={}
        if not resultlist:
            resultlist = company.objects.filter()
            
        test=[]
        favor_com = favor.objects.filter(who_id=req.user.id)
        for item in favor_com:
            test.append(item.which_id)
        
        for item in resultlist:
            if item.id in test:
                item.is_in_attention = True
            else:
                item.is_in_attention = False
            
        a["result"] = resultlist
        
        if req.user.is_authenticated():
            req.user.is_authenticated = True
            a['user'] = req.user
        
        a["keyword"] = words
        return render_to_response("search.html",a)
    else:
        a={}
     
        resultlist = company.objects.filter()
              
        a["result"] = resultlist
        
        favor_com = favor.objects.filter(who_id=req.user.id)
        test=[]
        for item in favor_com:
            test.append(item.which_id)
            
        for item in resultlist:
            if item.id in test:
                item.is_in_attention = True
            else:
                item.is_in_attention = False
        
        if req.user.is_authenticated():
            req.user.is_authenticated = True
            a['user'] = req.user
        return render_to_response("search.html",a)

def attention(req):
    infor = favor.objects.filter(who_id=req.user.id)
    a = {}
    #print infor
    a['favor_companys'] = infor
    if req.user.is_authenticated():
        req.user.is_authenticated = True
        a['user'] = req.user
    return render_to_response("home.html",a)

def logout(req):
    auth.logout(req)
    return render_to_response("index.html")
