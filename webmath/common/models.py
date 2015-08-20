from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

# context processor to pass profile to the template
# def profile(request):
#     return {'profile': request.user.
    
def is_member(self, group):
    return self.groups.filter(name=group).exists()

auth.models.User.add_to_class('is_member', is_member)
auth.models.User.add_to_class('is_student', lambda self: self.is_member('students'))
auth.models.User.add_to_class('is_teacher', lambda self: self.is_member('teachers'))
auth.models.User.add_to_class('is_admin', lambda self: self.is_member('admins'))

class BaseProfile(models.Model):
    
    user = models.OneToOneField(User, related_name="profile")
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")

    
class Admin(BaseProfile):
    
    def __str__(self):
        return "Admin {0}".format(self.user.username)

class Teacher(BaseProfile):

    def __str__(self):
        return "Professeur {0}".format(self.user.username)

class Student(BaseProfile):

    def __str__(self):
        return "Etudiant {0}".format(self.user.username)


class Classes(models.Model):
    # nom du groupe, par exemple 1ecg3
    name = models.CharField(max_length=15)
    
    # détermine si le groupe est actif ou non
    is_active = models.BooleanField(default=True)
    
    # date de création du groupe
    creation_datetime = models.DateTimeField(auto_now_add=True)
    
    # administrateur du groupe
    owner = models.ForeignKey(Teacher)
    
    # participants au groupe
    # http://stackoverflow.com/questions/9352662/how-to-use-the-reverse-of-a-django-manytomany-relationship
    members = models.ManyToManyField(Student, related_name='classes')
    
    #