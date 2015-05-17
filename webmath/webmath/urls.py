from django.conf.urls import patterns, include, url
from django.contrib import admin 

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('quiz.urls', namespace='quiz')),
    url(r'^common/', include('common.urls', namespace="common")),
    url(r'^permission/', include('permission.urls', namespace="permission")),
)