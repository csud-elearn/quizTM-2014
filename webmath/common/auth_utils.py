from django.contrib.auth.decorators import login_required, user_passes_test

def is_teacher(user):
    return user.groups.filter(name='teachers').exists()
    
def is_student(user):
    return user.groups.filter(name='students').exists()
    
def teacher_required(view):
    return user_passes_test(login_required(view), is_teacher)
    
def student_required(view):
    return user_passes_test(login_required(view), is_student)