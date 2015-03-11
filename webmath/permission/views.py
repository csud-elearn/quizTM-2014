from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from common.auth_utils import *

@login_required
def home(request):
    return render(request, 'permission/home.html', locals())

@login_required
@user_passes_test(is_teacher)
def teachers(request):
    return render(request, 'permission/teachers.html')
 
@login_required
@user_passes_test(is_student)
def students(request):
    return render(request, 'permission/students.html')

@teacher_required
def teachers2(request):
    return render(request, 'permission/teachers.html')