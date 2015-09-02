from django.conf.urls import patterns, url

from quiz.views import *

urlpatterns = patterns('',
    # URL des pages de l'application
    url(r'^$', root, name="root"),
    url(r'^find/$', find, name="find"),
    url(r'^create/$', create, name="create"),
    url(r'^(\d+)/complete/', complete, name="complete"),
    url(r'^(\d+)/correct/', correct, name="correct"),
    url(r'^completed-quizzes/', completed_quizzes, name="completed-quizzes"),
    url(r'^created-quizzes/', created_quizzes, name="created-quizzes"),
    url('^(\d+)/advanced-stats/', advanced_stats, name="advanced-stats"),
    # URL destinées à l'Ajax
    url(r'^findquiz/', findquiz, name="findquiz"),
    url(r'^savedraft/', savedraft, name="savedraft"),
    url(r'^listdrafts/', listdrafts, name="listdrafts"),
    url(r'^getdraft/', getdraft, name="getdraft"),
    url(r'^add-correct-answer/', add_correct_answer, name="add-correct-answer"),

    # gestion des classes
    url(r'^classes/$', class_members, name="classes"),
    url(r'^classes/(?P<class_id>\d+)$', class_members, name="class_members"),

)