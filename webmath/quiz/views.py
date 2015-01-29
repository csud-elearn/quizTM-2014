from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
import json
from quiz.utils.save import SaveQuiz
from quiz.utils.submit import QuizForms
from quiz.forms import TextForm, CheckboxForm, RadioForm, SelectForm
from quiz.models import Quiz

# Create your views here.

def index(request):
    return render(request, 'quiz/index.html')

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
        
def complete(request, n_quiz):
    # Si la requête est de type POST, on créer un nouveau formulaire et on le remplit avec les données de requête
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz, data=request.POST)
        
        #On controle que les formulaires sont valides
        if quizforms.are_valid():
            
            quizforms.save_answers() #Les réponses sont enregistrées dans la db
            
            return HttpResponseRedirect(reverse("quiz:index"))

    # Si la requête est de type GET, on affiche un formulaire vide
    else:
        quiz = get_object_or_404(Quiz, id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz)
            
        return render(request, 'quiz/complete.html', {'quiz': quiz, 'l_forms': quizforms.get_forms()})
        
def find(request):
    return render(request, 'quiz/find.html', {'l_quiz' : Quiz.objects.order_by('-creation_date')[:5]})
    
def findquiz(request):
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