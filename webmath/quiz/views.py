from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from quiz.utils.save import SaveQuiz
from quiz.utils.submit import QuizForms
from quiz.utils.correct import CorrectQuiz
from quiz.forms import TextForm, CheckboxForm, RadioForm, SelectForm
from quiz.models import Quiz, QuizDraft, CompletedQuiz, SqSubmit, QcmSubmitMulti, QcmSubmitOne
from common.auth_utils import *
from django.contrib.auth.decorators import login_required, user_passes_test
import json

def index(request):
    print("utilisateur : " + str(request.user))
    print(request.user.groups.all())
    return render(request, 'quiz/index.html')

@login_required
@user_passes_test(is_teacher)
def create(request):
    if request.method == 'POST':
        json_string = request.POST['json'] #Chaîne json contenant toutes les données des questions du quiz
        title = request.POST['title']
        quizcode = request.POST['quizcode'] #Code (format texte) du quiz
        
        questions_list = json.loads(json_string) #Parsing du json
        
        quiz = SaveQuiz(title, questions_list, quizcode) #Sauvegarde du quiz dans la db
        
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
            
            completed = quizforms.save_answers() #Les réponses sont enregistrées dans la db
            
            return HttpResponseRedirect(reverse("quiz:correct", args=[completed.pk]))

    # Si la requête est de type GET, on affiche un formulaire vide
    else:
        quiz = get_object_or_404(Quiz, id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz)
            
        return render(request, 'quiz/complete.html', {'quiz': quiz, 'l_forms': quizforms.get_forms()})
        
def find(request):
    return render(request, 'quiz/find.html', {'l_quiz' : Quiz.objects.order_by('-creation_date')[:5]})
    
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
    
def savedraft(request):
    if request.method == "POST":
        title = request.POST["title"]
        code = request.POST["code"]
        
        draft = QuizDraft(title=title, code=code)
        draft.save()
        
        return HttpResponse(str(draft.pk))
        
def listdrafts(request): # Permet de récupérer la liste des brouillons en json
    if request.method == "GET":
        drafts = QuizDraft.objects.all()
        
        if len(drafts) > 0:
            list_drafts = [] # Liste qui sera sérializée
            
            for d in drafts:
                list_drafts.append({
                    "title" : d.title,
                    "id" : d.pk,
                })
                
            json_string = json.dumps(list_drafts)
        
            return HttpResponse(json_string)
        
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