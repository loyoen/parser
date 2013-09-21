# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class jobsite(models.Model):
    Site_Name = models.CharField(max_length = 128)
    Site_Url  = models.CharField(max_length = 1024) 
    
class company(models.Model):
    Company_Code = models.CharField(max_length = 1024)
    #Company_Url = models.CharField(max_length = 1024)
    Company_Name = models.CharField(max_length = 128)
    AddDate = models.DateTimeField(max_length = 128)
    Description = models.CharField(max_length = 8192)
    Profession = models.CharField(max_length = 128)
    Category = models.CharField(max_length = 20)
    Company_Size = models.CharField(max_length = 20)
    DataFrom = models.ForeignKey(jobsite)
    UpDate = models.DateTimeField(max_length = 128)

class favor(models.Model):
    who = models.ForeignKey(User)
    which = models.ForeignKey(company)

class keyword(models.Model):
    word = models.CharField(max_length = 128)
    mycom = models.ForeignKey(company)
    
class recruit(models.Model):
    url = models.CharField(max_length = 1024)
    position = models.CharField(max_length = 128)
    description = models.CharField(max_length = 8192)
    requirement =models.CharField(max_length = 2048)
    numneeded = models.CharField(max_length = 10)
    categoryOfWork = models.CharField(max_length = 20)
    yearsForWork = models.CharField(max_length = 20)
    degree = models.CharField(max_length = 20)
    startdate = models.CharField(max_length = 20)
    enddate = models.CharField(max_length = 20)
    location = models.CharField(max_length = 20)
    department = models.CharField(max_length = 128)
    companyname = models.ForeignKey(company)

class hotel(models.Model):
    url = models.CharField(max_length = 1024)
    address = models.CharField(max_length = 1024)
    name = models.CharField(max_length = 128)
    image_url = models.CharField(max_length = 1024)
    DataFrom = models.ForeignKey(jobsite)
    
class room(models.Model):
    
    name = models.CharField(max_length = 128)
    image_url = models.CharField(max_length = 2048)
    area = models.CharField(max_length = 1024)
    bed = models.CharField(max_length = 1024)
    net = models.CharField(max_length = 128)
    price = models.CharField(max_length = 128)
    
    hotelFrom = models.ForeignKey(hotel)
    
class comment(models.Model):
    date = models.CharField(max_length = 128)
    content = models.CharField(max_length = 2048)
    roomtype = models.CharField(max_length = 128)
    hotelFrom = models.ForeignKey(hotel)
    
class weibo(models.Model):
    author = models.CharField(max_length = 128)
    isV = models.CharField(max_length = 2)
    url = models.CharField(max_length = 1024)
    content = models.CharField(max_length = 2048)
    smimg = models.CharField(max_length = 1024)
    mdimg = models.CharField(max_length = 1024)
    bgimg = models.CharField(max_length = 1024)
    adddate = models.DateTimeField(max_length = 128)
    publish_date = models.CharField(max_length = 128)
    companyname = models.ForeignKey(company)

class atlist(models.Model):
    name = models.CharField(max_length = 128)
    url  = models.CharField(max_length = 1024)
    blong = models.ForeignKey(weibo)
    
class record(models.Model):
    update = models.DateTimeField(max_length = 128)
    parsertype = models.CharField(max_length = 128)
    res = models.CharField(max_length = 128)
    name = models.ForeignKey(company)
    
class news(models.Model):
    newsTitle = models.CharField(max_length = 1024)
    newsContent = models.CharField(max_length = 2048)
    newsUrl = models.CharField(max_length = 1024)
    newsDate = models.CharField(max_length = 1024)
    imgUrl = models.CharField(max_length = 1024)
    DataFrom = models.ForeignKey(jobsite)
    companyname = models.ForeignKey(company)
