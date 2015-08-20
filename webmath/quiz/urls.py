from django.conf.urls import patterns, url

from quiz.views import *

urlpatterns = patterns('',
    # URL des pages de l'application
    url(r'^$', find, name="find"),
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
    url(r'^classes/', ls_classes, name="classes"),
)