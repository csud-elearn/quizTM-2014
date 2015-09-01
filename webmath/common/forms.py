from django import forms
from django.forms.extras.widgets import *
from common.models import Class

# pour supprimer les doubles points dans les formulaires générés, : https://github.com/torchbox/wagtail/issues/130

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget= forms.TextInput(attrs={'class' : 'form-control bottom-space'}), max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class' : 'form-control bottom-space'}))


class RegisterFormAllowTeachers(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget= forms.TextInput(attrs={'class' : 'form-control bottom-space'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class' : 'form-control bottom-space'}))
    mail = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class' : 'form-control bottom-space'}))
    account_type = forms.ChoiceField(label='Type de compte', choices=(
        ("teacher", "Professeur"),
        ("student", "Étudiant"),
        ), widget=forms.Select(attrs={'class' : 'form-control bottom-space'}))

class RegisterStudentForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget= forms.TextInput(attrs={'class' : 'form-control bottom-space'}))
    firstname  = forms.CharField(label="Prénom", widget= forms.TextInput(attrs={'class' : 'form-control bottom-space'}))
    lastname = forms.CharField(label="Nom", widget= forms.TextInput(attrs={'class' : 'form-control bottom-space'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class' : 'form-control bottom-space'}))
    mail = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class' : 'form-control bottom-space'}))
    class_group_id = forms.ModelMultipleChoiceField(
        label="Groupe", queryset=Class.objects.all(),
        help_text='Choisissez <strong>TOUTES</strong> les classes auxquelles vous appartenez! '
    )

    