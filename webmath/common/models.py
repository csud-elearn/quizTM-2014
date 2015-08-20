from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    
    STUDENT = 'S'
    PROF = 'P'
    ADMIN = 'A'
    TYPE_CHOICES = (
        (STUDENT, 'Étudiant'),
        (PROF, 'Professeur'),
        (ADMIN, 'Administrateur'),
    )
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    
    # déterminer s'il s'agit d'un prof ou d'un étudiant. Ce champ est un peu redondant 
    # il est probablement possible de déterminer le type de compte en regardant l'instance de la classe
    # puisque ce modèle n'est jamais implémenté tel quel (abstract = True)
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=STUDENT
    )
                                      
    class Meta:
        abstract = True
        
    
class Admin(BaseProfile):
    
    def __str__(self):
        return "Admin {0}".format(self.user.username)

class Teacher(BaseProfile):

    def __str__(self):
        return "Professeur {0}".format(self.user.username)

class Student(BaseProfile):

    def __str__(self):
        return "Etudiant {0}".format(self.user.username)


class Group(models.Model):
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
    members = models.ManyToManyField(Student, related_name='groups')