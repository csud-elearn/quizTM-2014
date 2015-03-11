from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.forms import LoginForm, RegisterForm
from django.core.urlresolvers import reverse
from common.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.models import Group

def connexion(request):
    erreur = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                erreur = True
    else:
        form = LoginForm()
        
    return render(request, "common/login.html", locals())
    
def deconnexion(request):
    logout(request)
    return redirect('common:connexion')
    
    
def register(request):
    if request.method == "POST":
        registerform = RegisterForm(data=request.POST)
        
        if registerform.is_valid():
            username = registerform.cleaned_data["username"]
            password = registerform.cleaned_data["password"]
            mail = registerform.cleaned_data["mail"]
            
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                account_model = None # Modèle à instancier pour créer le compte
                
                if registerform.cleaned_data["account_type"] == "student":
                    account_model = Student # Le modèle à utiliser est Student
                    group_name = "students"
                    
                elif registerform.cleaned_data["account_type"] == "teacher":
                    account_model = Teacher # Le modèle à utiliser est Teacher
                    group_name = "teachers"
                    
                user = User.objects.create_user(username, mail, password)
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                user.save()
                    
                account = account_model() # Instanciation du modèle
                account.user = user # Liaison au compte user
                account.save()
                
                return redirect('common:connexion')
            except Exception as e:
                return HttpResponse("Erreur non gérée : {}".format(str(e)))

    else:
        registerform = RegisterForm()
        
    return render(request, "common/register.html", {'registerform' : registerform})