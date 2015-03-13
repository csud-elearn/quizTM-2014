from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from quiz.utils.save import SaveQuiz
from quiz.utils.submit import QuizForms
from quiz.utils.correct import CorrectQuiz
from quiz.forms import TextForm, CheckboxForm, RadioForm, SelectForm
from quiz.models import Quiz, QuizDraft, CompletedQuiz, SqSubmit, QcmSubmitMulti, QcmSubmitOne
from common.models import Teacher, Student
from common.auth_utils import *
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import time

def index(request):
    return render(request, 'quiz/index.html')

@login_required
@user_passes_test(is_teacher)
def create(request):
    if request.method == 'POST':
        json_string = request.POST['json'] #Chaîne json contenant toutes les données des questions du quiz
        title = request.POST['title']
        quizcode = request.POST['quizcode'] #Code (format texte) du quiz
        
        questions_list = json.loads(json_string) #Parsing du json
        
        teacher_account = Teacher.objects.get(user=request.user) #Compte prof correspondant à l'user
        
        quiz = SaveQuiz(title, questions_list, quizcode, teacher_account) #Sauvegarde du quiz dans la db
        
        return HttpResponseRedirect(reverse("quiz:complete", args=[quiz.get_id()]))
    else:
        return render(request, 'quiz/create.html')

@login_required
def complete(request, n_quiz):
    # Si la requête est de type POST, on créer un nouveau formulaire et on le remplit avec les données de requête
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz, data=request.POST)
        
        #On controle que les formulaires sont valides
        if quizforms.are_valid():
            
            completed = quizforms.save_answers(request.user) #Les réponses sont enregistrées dans la db
            
            return HttpResponseRedirect(reverse("quiz:correct", args=[completed.pk]))

    # Si la requête est de type GET, on affiche un formulaire vide
    else:
        quiz = get_object_or_404(Quiz, id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz)
            
        return render(request, 'quiz/complete.html', {'quiz': quiz, 'l_forms': quizforms.get_forms()})
        
def find(request):
    return render(request, 'quiz/find.html', {'l_quiz' : Quiz.objects.order_by('-creation_date')[:5]})

@login_required
def findquiz(request):
    if request.method == "GET":
        n_quiz = request.GET['quiz']
        
        try:
            quiz = Quiz.objects.get(id=n_quiz)
        except: #Si le quiz n'existe pas
            return HttpResponse("")
        else:
            url = reverse("quiz:complete", args=[n_quiz])
            json_dict = {"url" : url, "title" : quiz.title}
            json_string = json.dumps(json_dict)
            
        return HttpResponse(json_string)
    else:
        return HttpResponse("")

@login_required
@user_passes_test(is_teacher)
def savedraft(request):
    if request.method == "POST":
        title = request.POST["title"]
        code = request.POST["code"]
        user = Teacher.objects.get(user=request.user)
        
        draft = QuizDraft(title=title, code=code, id_teacher=user)
        draft.save()
        
        return HttpResponse(str(draft.pk))
        
@login_required
@user_passes_test(is_teacher)
def listdrafts(request): # Permet de récupérer la liste des brouillons en json
    if request.method == "GET":
        teacher_account = Teacher.objects.get(user=request.user)
        drafts = QuizDraft.objects.filter(id_teacher=teacher_account)
        
        list_drafts = [] # Liste qui sera sérializée
        
        for d in drafts:
            list_drafts.append({
                "title" : d.title,
                "id" : d.pk,
            })
            
        json_string = json.dumps(list_drafts)
    
        return HttpResponse(json_string)

@login_required
@user_passes_test(is_teacher)
def getdraft(request): # Permet de récupérer le titre et le code d'un brouillon en json
    if request.method == "GET":
        n_draft = request.GET['draft']
        
        quiz = get_object_or_404(QuizDraft, pk=n_draft)
        
        json_dict = {
            "title" : quiz.title,
            "code" : quiz.code,
        }
        json_string = json.dumps(json_dict)
        
        return HttpResponse(json_string)
        
def correct(request, n_completed):
    """
    Corrige les réponses soumises par un étudiant
    """
    completed = get_object_or_404(CompletedQuiz, pk=n_completed)
    
    correctquiz = CorrectQuiz(completed)
        
    return render(request, 'quiz/correct.html', {'correctquiz' : correctquiz, 'quiz' : completed.id_quiz})

@login_required
def completed_quizzes(request):
    """
    Affiche la liste des résolutions de quiz de l'élève
    """
    # Récupération des résolutions de l'élève dans la db
    l_completed = CompletedQuiz.objects.filter(id_user=request.user)
    
    return render(request, 'quiz/completed-quizzes.html', {'l_completed' : l_completed})

@login_required
@user_passes_test(is_teacher)
def created_quizzes(request):
    """
    Affiche la liste des quiz créés par le prof
    """
    # Récupération des quiz créés par le prof dans la db
    teacher = Teacher.objects.get(user=request.user)
    l_created = Quiz.objects.filter(id_teacher=teacher)
    
    return render(request, 'quiz/created-quizzes.html', {'l_created' : l_created})
    
@login_required
@user_passes_test(is_teacher)
def advanced_stats(request, n_quiz):
    """
    Affiche les statistiques avancées du quiz en argument
    """
    quiz = get_object_or_404(Quiz, pk=n_quiz)
    
    return render(request, 'quiz/advanced_stats.html')