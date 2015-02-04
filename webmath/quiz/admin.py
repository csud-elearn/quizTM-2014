from django.contrib import admin
from quiz.models import *

# Register your models here.
admin.site.register(Quiz)
admin.site.register(CompletedQuiz)
admin.site.register(Qcm)
admin.site.register(SimpleQuestion)
admin.site.register(QcmChoice)
admin.site.register(SqAnswer)
admin.site.register(QcmSubmitMulti)
admin.site.register(QcmSubmitOne)
admin.site.register(QuizDraft)