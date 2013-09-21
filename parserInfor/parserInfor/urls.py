from django.conf.urls import patterns, include, url
from myparser.views import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^register', register),
    url(r'^search', search),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^doparser/(?P<parser_id>\d+)/$', doparser),
    url(r'^zhaopin', zhaopin),
    url(r'^addfavor', addfavor),
    url(r'^rmfavor', rmfavor),
    url(r'^split', SplitKeyword),
    url(r'^attention', attention),
	#deal with the url: http://www.wuluostudio.com/register/
	url(r'^company/(?P<company_id>\d+)/$',company_browse),
    url(r'^jobs/(?P<job_id>\d+)/$',job_browse),
    #url(r'^search', search),
    url(r'^companys/(?P<page>\d+)/$', company_list),
    url(r'^alljobs/(?P<page>\d+)/$', jobs_list),
    url(r'^about', about),
    url(r'^company/(?P<company_id>\d+)/jobs/(?P<page>\d+)/',companyJobs_browse),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'luoyongqian.views.home', name='home'),
    # url(r'^luoyongqian/', include('luoyongqian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
