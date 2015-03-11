from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
        
    class Meta:
        abstract = True

class Teacher(BaseProfile):

    def __str__(self):
        return "Professeur {0}".format(self.user.username)

class Student(BaseProfile):

    def __str__(self):
        return "Etudiant {0}".format(self.user.username)
